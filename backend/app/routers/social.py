from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.direct_message import DirectMessage
from app.models.friend_connection import FriendConnection
from app.models.user import User

async def _learner_only(current_user: User = Depends(get_current_user)) -> None:
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Social features are available to learners only")


router = APIRouter(
    prefix="/api/social",
    tags=["social"],
    dependencies=[Depends(_learner_only)],
)


class FriendRequest(BaseModel):
    user_id: int


class MessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


def _profile(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name,
        "avatar": user.avatar,
        "native_language": user.native_language,
        "target_language": user.target_language,
        "bio": user.bio,
    }


async def _accepted(db: AsyncSession, user_id: int, other_id: int) -> bool:
    result = await db.execute(
        select(FriendConnection.id).where(
            FriendConnection.status == "accepted",
            or_(
                and_(
                    FriendConnection.requester_id == user_id,
                    FriendConnection.addressee_id == other_id,
                ),
                and_(
                    FriendConnection.requester_id == other_id,
                    FriendConnection.addressee_id == user_id,
                ),
            )
        )
    )
    return result.scalar_one_or_none() is not None


@router.get("/friends")
async def list_friends(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FriendConnection).where(
            FriendConnection.status == "accepted",
            or_(
                FriendConnection.requester_id == current_user.id,
                FriendConnection.addressee_id == current_user.id,
            ),
        )
    )
    rows = result.scalars().all()
    ids = [
        row.addressee_id if row.requester_id == current_user.id else row.requester_id
        for row in rows
    ]
    if not ids:
        return []
    users = (
        await db.execute(
            select(User).where(User.id.in_(ids), User.is_active.is_(True), User.role == "user")
        )
    ).scalars().all()
    return [_profile(user) for user in users]


@router.get("/requests")
async def friend_requests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    incoming = (
        await db.execute(
            select(FriendConnection).where(
                FriendConnection.addressee_id == current_user.id,
                FriendConnection.status == "pending",
            )
        )
    ).scalars().all()
    outgoing = (
        await db.execute(
            select(FriendConnection).where(
                FriendConnection.requester_id == current_user.id,
                FriendConnection.status == "pending",
            )
        )
    ).scalars().all()
    ids = [row.requester_id for row in incoming] + [row.addressee_id for row in outgoing]
    users = (
        await db.execute(select(User).where(User.id.in_(ids), User.role == "user"))
    ).scalars().all() if ids else []
    by_id = {user.id: user for user in users}
    return {
        "incoming": [{"id": row.id, "user": _profile(by_id[row.requester_id])} for row in incoming if row.requester_id in by_id],
        "outgoing": [{"id": row.id, "user": _profile(by_id[row.addressee_id])} for row in outgoing if row.addressee_id in by_id],
    }


@router.get("/users")
async def search_users(
    q: str = Query(default="", max_length=80),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    term = q.strip()
    if len(term) < 2:
        return []
    users = (
        await db.execute(
            select(User)
            .where(
                User.id != current_user.id,
                User.role == "user",
                User.is_active.is_(True),
                or_(User.username.ilike(f"%{term}%"), User.display_name.ilike(f"%{term}%")),
            )
            .order_by(func.lower(User.display_name), User.id)
            .limit(20)
        )
    ).scalars().all()
    return [_profile(user) for user in users]


@router.post("/requests")
async def send_friend_request(
    data: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot add yourself")
    target = await db.get(User, data.user_id)
    if not target or not target.is_active or target.role != "user":
        raise HTTPException(status_code=404, detail="Learner not found")

    existing = await db.execute(
        select(FriendConnection).where(
            or_(
                and_(
                    FriendConnection.requester_id == current_user.id,
                    FriendConnection.addressee_id == target.id,
                ),
                and_(
                    FriendConnection.requester_id == target.id,
                    FriendConnection.addressee_id == current_user.id,
                ),
            )
        )
    )
    connection = existing.scalar_one_or_none()
    if connection:
        if connection.status == "accepted":
            raise HTTPException(status_code=409, detail="Already friends")
        if connection.status == "pending":
            raise HTTPException(status_code=409, detail="Friend request already pending")
        connection.requester_id = current_user.id
        connection.addressee_id = target.id
        connection.pair_key = f"{min(current_user.id, target.id)}:{max(current_user.id, target.id)}"
        connection.status = "pending"
        connection.updated_at = datetime.now(UTC).replace(tzinfo=None)
    else:
        connection = FriendConnection(
            requester_id=current_user.id,
            addressee_id=target.id,
            pair_key=f"{min(current_user.id, target.id)}:{max(current_user.id, target.id)}",
            status="pending",
        )
        db.add(connection)
    await db.commit()
    return {"id": connection.id, "status": connection.status}


@router.post("/requests/{request_id}/accept")
async def accept_friend_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    connection = await db.get(FriendConnection, request_id)
    if not connection or connection.addressee_id != current_user.id or connection.status != "pending":
        raise HTTPException(status_code=404, detail="Friend request not found")
    connection.status = "accepted"
    connection.updated_at = datetime.now(UTC).replace(tzinfo=None)
    await db.commit()
    return {"status": "accepted"}


@router.delete("/friends/{user_id}")
async def remove_friend(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FriendConnection).where(
            FriendConnection.status == "accepted",
            or_(
                and_(FriendConnection.requester_id == current_user.id, FriendConnection.addressee_id == user_id),
                and_(FriendConnection.requester_id == user_id, FriendConnection.addressee_id == current_user.id),
            )
        )
    )
    connection = result.scalar_one_or_none()
    if not connection:
        raise HTTPException(status_code=404, detail="Friendship not found")
    await db.delete(connection)
    await db.commit()
    return {"status": "removed"}


@router.get("/messages/{user_id}")
async def list_messages(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not await _accepted(db, current_user.id, user_id):
        raise HTTPException(status_code=403, detail="You can only message accepted friends")
    result = await db.execute(
        select(DirectMessage)
        .where(
            or_(
                and_(DirectMessage.sender_id == current_user.id, DirectMessage.recipient_id == user_id),
                and_(DirectMessage.sender_id == user_id, DirectMessage.recipient_id == current_user.id),
            )
        )
        .order_by(DirectMessage.created_at.asc(), DirectMessage.id.asc())
        .limit(200)
    )
    messages = result.scalars().all()
    return [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "recipient_id": message.recipient_id,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }
        for message in messages
    ]


@router.post("/messages/{user_id}")
async def send_message(
    user_id: int,
    data: MessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    content = data.content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="Message cannot be empty")
    if not await _accepted(db, current_user.id, user_id):
        raise HTTPException(status_code=403, detail="You can only message accepted friends")
    recipient = await db.get(User, user_id)
    if not recipient or not recipient.is_active or recipient.role != "user":
        raise HTTPException(status_code=404, detail="Learner not found")
    message = DirectMessage(sender_id=current_user.id, recipient_id=user_id, content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return {
        "id": message.id,
        "sender_id": message.sender_id,
        "recipient_id": message.recipient_id,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
    }
