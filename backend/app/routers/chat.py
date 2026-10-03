import json
from datetime import UTC, date, datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_logger import get_logger
from app.core.database import get_db
from app.core.deps import get_current_user, get_active_study_plan_optional, require_not_maintenance, require_learner
from app.core.limiter import limiter
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.progress import Progress
from app.models.user import User
from app.schemas.chat import ChatHistoryResponse, ChatRequest, ConversationCreate, ConversationResponse
from app.services.feature_quota_service import reserve, settle
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import LLMError, LLMStreamReset, LLMTimeoutError, LLMToolResultEvent, LLMUnavailableError, llm_adapter
from app.services.memory_service import build_memory_context, build_save_user_memory_tool, execute_save_user_memory, get_user_memories
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.tutor import build_tutor_system_prompt
from app.utils.db import db_session

router = APIRouter(prefix="/api/chat", tags=["chat"], dependencies=[Depends(require_learner)])
logger = get_logger(__name__)
MAX_HISTORY = 30
DEFAULT_CEFR = "A2"
DEFAULT_TARGET_LANG = "en-GB"


def _build_tutor_system_prompt(**kwargs) -> str:
    return build_tutor_system_prompt(**kwargs)


async def _resolve_chat_context(db: AsyncSession, user: User) -> tuple[str, str, int | None]:
    from app.services.user_language_service import get_active_language
    plan = await get_active_study_plan_optional(user, db)
    if plan:
        return plan.cefr_level, plan.target_language, plan.id
    language = await get_active_language(db, user.id)
    return DEFAULT_CEFR, language.target_language if language else DEFAULT_TARGET_LANG, None


@router.get("/conversations", response_model=list[ConversationResponse])
@limiter.limit("60/minute")
async def list_conversations(request: Request, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.services.user_language_service import get_active_language
    language = await get_active_language(db, current_user.id)
    if not language:
        return []
    return (await db.execute(select(Conversation).where(Conversation.user_id == current_user.id, Conversation.target_language == language.target_language).order_by(Conversation.updated_at.desc()))).scalars().all()


@router.post("/conversations", response_model=ConversationResponse)
@limiter.limit("60/minute")
async def create_conversation(request: Request, data: ConversationCreate, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    _, target, plan_id = await _resolve_chat_context(db, current_user)
    conv = Conversation(user_id=current_user.id, title=data.title or "New conversation", study_plan_id=plan_id, target_language=target)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def delete_conversation(request: Request, conversation_id: int, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.services.user_language_service import get_active_language
    conv = await db.get(Conversation, conversation_id)
    language = await get_active_language(db, current_user.id)
    if not conv or conv.user_id != current_user.id or (language and conv.target_language and conv.target_language != language.target_language):
        raise HTTPException(status_code=404, detail="Conversation not found")
    await db.delete(conv)
    await db.commit()


@router.get("/conversations/{conversation_id}/messages", response_model=ChatHistoryResponse)
@limiter.limit("60/minute")
async def get_conversation_messages(request: Request, conversation_id: int, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.services.user_language_service import get_active_language
    conv = await db.get(Conversation, conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    language = await get_active_language(db, current_user.id)
    if not language:
        return ChatHistoryResponse(messages=[])
    rows = (await db.execute(select(ChatHistory).where(ChatHistory.conversation_id == conversation_id, ChatHistory.user_id == current_user.id, ChatHistory.target_language == language.target_language).order_by(ChatHistory.created_at.asc()).limit(MAX_HISTORY))).scalars().all()
    return ChatHistoryResponse(messages=[{"role": item.role, "content": item.content} for item in rows])


@router.get("/history", response_model=ChatHistoryResponse)
@limiter.limit("60/minute")
async def get_chat_history(request: Request, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.services.user_language_service import get_active_language
    language = await get_active_language(db, current_user.id)
    if not language:
        return ChatHistoryResponse(messages=[])
    rows = (await db.execute(select(ChatHistory).where(ChatHistory.user_id == current_user.id, ChatHistory.target_language == language.target_language).order_by(ChatHistory.created_at.asc()).limit(MAX_HISTORY))).scalars().all()
    return ChatHistoryResponse(messages=[{"role": item.role, "content": item.content} for item in rows])


@router.post("")
@limiter.limit("30/minute")
async def chat(request: Request, request_data: ChatRequest, _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not request_data.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty")
    if current_user.monthly_tokens_limit > 0:
        from app.services.quota_service import check_monthly_tokens
        allowed, used, limit = await check_monthly_tokens(db, current_user.id, current_user.monthly_tokens_limit)
        if not allowed:
            raise HTTPException(status_code=429, detail=f"Monthly token limit reached ({used}/{limit} tokens)")
    cefr, target, plan_id = await _resolve_chat_context(db, current_user)
    if request_data.conversation_id:
        conv = await db.get(Conversation, request_data.conversation_id)
        if not conv or conv.user_id != current_user.id or (conv.target_language and conv.target_language != target):
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        title = request_data.message[:60].replace("\n", " ").replace("\r", "").strip()
        if len(request_data.message) > 60:
            title += "..."
        conv = Conversation(user_id=current_user.id, title=title, study_plan_id=plan_id, target_language=target)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
    conversation_id = conv.id
    prog = None
    total_xp = 0
    if plan_id:
        prog = (await db.execute(select(Progress).where(Progress.study_plan_id == plan_id, Progress.date == date.today()))).scalar_one_or_none()
        total_xp = sum(item.xp_earned for item in (await db.execute(select(Progress).where(Progress.study_plan_id == plan_id))).scalars().all())
    context = []
    if current_user.learning_goals:
        try:
            goals = json.loads(current_user.learning_goals)
            if goals:
                context.append(f"Learning goals: {', '.join(goals)}")
        except (ValueError, TypeError):
            pass
    if current_user.bio and current_user.bio.strip():
        context.append(f"About the student: {current_user.bio.strip()}")
    try:
        async with db_session() as memory_db:
            memories = await get_user_memories(memory_db, current_user.id)
        memory_context = build_memory_context(memories)
    except Exception:
        logger.exception("Failed to load chat memories")
        memory_context = ""
    native_name = get_native_language_name(current_user.native_language)
    prompt_args = dict(student_name=current_user.display_name, cefr_level=cefr, native_language=native_name,
                       target_language_name=get_language_name(target), total_xp=total_xp,
                       streak=prog.streak_day if prog else 0, lessons_today=prog.lessons_completed if prog else 0,
                       skills=", ".join(f"{key}: {round(value * 100)}%" for key, value in (prog.skills or {}).items()) if prog and prog.skills else "none yet",
                       user_context="\nStudent context:\n" + "\n".join(f"- {item}" for item in context) + "\n" if context else "",
                       memory_context=memory_context, language_prompt_overlay=get_language_prompt_overlay(target))
    system_prompt = _build_tutor_system_prompt(**prompt_args)
    fallback_prompt = _build_tutor_system_prompt(**prompt_args, memory_tools_enabled=False)
    reservation = await reserve(current_user, "chat")
    try:
        db.add(ChatHistory(user_id=current_user.id, conversation_id=conversation_id, role="user", content=request_data.message, study_plan_id=plan_id, target_language=target))
        await db.commit()
        rows = list((await db.execute(select(ChatHistory).where(ChatHistory.user_id == current_user.id, ChatHistory.conversation_id == conversation_id).order_by(ChatHistory.created_at.desc()).limit(MAX_HISTORY))).scalars().all())
        history = [{"role": item.role, "content": item.content} for item in reversed(rows)]
        messages = [{"role": "system", "content": system_prompt}] + history
        fallback_messages = [{"role": "system", "content": fallback_prompt}] + history
    except BaseException:
        await settle(reservation, success=False)
        raise

    async def event_stream():
        full_response = ""
        memory_updated_sent = False
        charged = False
        try:
            yield f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"
            async def execute_memory_tool(call):
                async with db_session() as memory_db:
                    return await execute_save_user_memory(memory_db, current_user.id, call, "chat", study_plan_id=plan_id)
            stream = await llm_adapter.chat(messages, stream=True, tools=[build_save_user_memory_tool(native_name)], tool_executor=execute_memory_tool, fallback_messages=fallback_messages)
            async for chunk in stream:
                if isinstance(chunk, LLMToolResultEvent):
                    if chunk.result.content.get("saved") is True and not memory_updated_sent:
                        memory_updated_sent = True
                        yield f"data: {json.dumps({'memory_updated': True})}\n\n"
                    continue
                if isinstance(chunk, LLMStreamReset):
                    full_response = ""
                    yield f"data: {json.dumps({'response_reset': True})}\n\n"
                    continue
                token = chunk if isinstance(chunk, str) else getattr(getattr(chunk.choices[0], "delta", None), "content", None)
                if token:
                    full_response += token
                    yield f"data: {json.dumps({'token': token})}\n\n"
            if not full_response.strip():
                raise LLMError("Tutor returned no response")
            if any(result.content.get("saved") is True for result in getattr(stream, "tool_results", [])) and not memory_updated_sent:
                yield f"data: {json.dumps({'memory_updated': True})}\n\n"
            db.add(ChatHistory(user_id=current_user.id, conversation_id=conversation_id, role="assistant", content=full_response, study_plan_id=plan_id, target_language=target))
            conv.updated_at = datetime.now(UTC).replace(tzinfo=None)
            await db.commit()
            await settle(reservation, success=True)
            charged = True
            yield f"data: {json.dumps({'done': True})}\n\n"
        except (LLMTimeoutError, LLMUnavailableError, LLMError) as exc:
            logger.exception("Chat generation failed")
            yield f"data: {json.dumps({'error': str(exc) or 'The tutor is temporarily unavailable.'})}\n\n"
        except Exception:
            logger.exception("Chat stream failed")
            yield f"data: {json.dumps({'error': 'The tutor is temporarily unavailable.'})}\n\n"
        finally:
            if not charged:
                await settle(reservation, success=False)
    return StreamingResponse(event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})
