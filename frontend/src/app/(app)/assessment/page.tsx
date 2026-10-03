'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { ClipboardCheck, CheckCircle2, Mic, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import BeginnerGate from '@/components/assessment/BeginnerGate'
import AdaptiveQuizCard from '@/components/assessment/AdaptiveQuizCard'
import DurationSelector, { DURATION_OPTIONS, type DurationOption } from '@/components/assessment/DurationSelector'
import { type AssessmentQuestion, type CEFRLevel } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import '../resource-reference.css'

interface AnswerRecord{question_id:string;skill:string;difficulty:string;correct:boolean}
interface AssessmentResult{cefr_level:string;score:number;skill_profile:Record<string,number>;strengths:string[];weaknesses:string[]}
interface ExistingPlan{cefr_level:string;created_at:string}
interface VoiceTrialOffer{available:boolean;token?:string;duration_seconds?:number}
interface AssessmentCompleteResponse{plan_id:number;cefr_level:string;voice_trial?:VoiceTrialOffer}
type FlowStep='checking'|'existing'|'beginner-gate'|'quiz'|'result'|'duration'|'voice-trial-offer'
const MAX_QUESTIONS=15
const CORRECT_STREAK_TO_UP=2
const WRONG_STREAK_TO_DOWN=2
const START_LEVEL:CEFRLevel='A2'
function pickNextQuestion(bank:AssessmentQuestion[],usedIds:Set<string>,currentLevel:CEFRLevel):AssessmentQuestion|null{const available=bank.filter(question=>!usedIds.has(question.id)&&question.difficulty===currentLevel);if(!available.length)return null;return available[Math.floor(Math.random()*available.length)]}
function adjustLevel(current:CEFRLevel,direction:'up'|'down'):CEFRLevel{const index=CEFR_LEVELS.indexOf(current);if(direction==='up'&&index<CEFR_LEVELS.length-1)return CEFR_LEVELS[index+1];if(direction==='down'&&index>0)return CEFR_LEVELS[index-1];return current}
export default function AssessmentPage(){
  const t=useTranslations('assessment')
  const tCommon=useTranslations('common')
  const locale=useLocale()
  const rtl=locale==='ar'
  const router=useRouter()
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const user=useAuthStore(s=>s.user)
  const stripeEnabled=useConfigStore(s=>s.stripeEnabled)
  const configLoaded=useConfigStore(s=>s.loaded)
  const loadConfig=useConfigStore(s=>s.load)
  const [step,setStep]=useState<FlowStep>('checking')
  const [existingPlan,setExistingPlan]=useState<ExistingPlan|null>(null)
  const [error,setError]=useState('')
  const [bank,setBank]=useState<AssessmentQuestion[]>([])
  const [currentQuestion,setCurrentQuestion]=useState<AssessmentQuestion|null>(null)
  const [questionNumber,setQuestionNumber]=useState(0)
  const [answers,setAnswers]=useState<AnswerRecord[]>([])
  const [usedIds]=useState<Set<string>>(()=>new Set())
  const [currentLevel,setCurrentLevel]=useState<CEFRLevel>(START_LEVEL)
  const [correctStreak,setCorrectStreak]=useState(0)
  const [wrongStreak,setWrongStreak]=useState(0)
  const [result,setResult]=useState<AssessmentResult|null>(null)
  const [selectedLevel,setSelectedLevel]=useState<CEFRLevel>('A1')
  const [evaluating,setEvaluating]=useState(false)
  const [durationOption,setDurationOption]=useState<DurationOption>(DURATION_OPTIONS[2])
  const [selectedGoals,setSelectedGoals]=useState<string[]>(['grammar','vocabulary'])
  const [submitting,setSubmitting]=useState(false)
  const [trialLoading,setTrialLoading]=useState(false)
  const [createdPlanId,setCreatedPlanId]=useState<number|null>(null)
  const [voiceTrial,setVoiceTrial]=useState<VoiceTrialOffer|null>(null)
  const [showStartWarning,setShowStartWarning]=useState(false)
  useEffect(()=>{void loadConfig()},[loadConfig])
  useEffect(()=>{
    async function check(){
      try{
        const lang=activeLanguage?.code??'en-GB'
        const [planRes,bankRes]=await Promise.all([apiFetch('/api/study-plan/current'),apiFetch(`/api/assessment/bank?language=${lang}`)])
        if(bankRes.ok){const bankData=await bankRes.json() as {questions:AssessmentQuestion[]};setBank(bankData.questions)}
        if(planRes.ok){const plan=await planRes.json();if(plan?.cefr_level){setExistingPlan(plan as ExistingPlan);setStep('existing');return}}
      }catch{/* Preserve no-plan fallback. */}
      setStep('beginner-gate')
    }
    void check()
  },[activeLanguage?.code])
  const canOfferVoiceTrial=configLoaded&&stripeEnabled&&user!==null&&!isSubscribed(user,stripeEnabled)&&!user.assessment_voice_trial_used
  function loadNextQuestion(level:CEFRLevel,usedSet:Set<string>){const question=pickNextQuestion(bank,usedSet,level);if(question){usedSet.add(question.id);setCurrentQuestion(question)}else void evaluateQuiz([...answers])}
  function startQuiz(){
    if(!bank.length){setError(tCommon('error'));return}
    setError('');usedIds.clear();setAnswers([]);setCurrentLevel(START_LEVEL);setCorrectStreak(0);setWrongStreak(0)
    const question=pickNextQuestion(bank,usedIds,START_LEVEL)
    if(question){usedIds.add(question.id);setCurrentQuestion(question);setQuestionNumber(1);setStep('quiz')}
  }
  function handleAnswer(chosen:string){
    if(!currentQuestion)return
    const isCorrect=chosen===currentQuestion.correct
    const record:AnswerRecord={question_id:currentQuestion.id,skill:currentQuestion.skill,difficulty:currentQuestion.difficulty,correct:isCorrect}
    const newAnswers=[...answers,record];setAnswers(newAnswers)
    let newCorrect=correctStreak;let newWrong=wrongStreak;let newLevel=currentLevel
    if(isCorrect){newCorrect+=1;newWrong=0;if(newCorrect>=CORRECT_STREAK_TO_UP){newLevel=adjustLevel(currentLevel,'up');newCorrect=0}}
    else{newWrong+=1;newCorrect=0;if(newWrong>=WRONG_STREAK_TO_DOWN){newLevel=adjustLevel(currentLevel,'down');newWrong=0}}
    setCorrectStreak(newCorrect);setWrongStreak(newWrong)
    if(newAnswers.length>=MAX_QUESTIONS){void evaluateQuiz(newAnswers);return}
    setCurrentLevel(newLevel);setQuestionNumber(value=>value+1);setTimeout(()=>loadNextQuestion(newLevel,usedIds),150)
  }
  async function evaluateQuiz(answersToSend:AnswerRecord[]){
    setEvaluating(true);setCurrentQuestion(null);setError('')
    try{
      const res=await apiFetch('/api/assessment/evaluate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({answers:answersToSend})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentResult;setResult(data);setSelectedLevel(data.cefr_level as CEFRLevel);setStep('result')
    }catch(err){const msg=err instanceof Error?err.message:'';setError(msg==='ai_service_error'||msg==='ai_service_unavailable'?tCommon('error'):msg||tCommon('error'))}finally{setEvaluating(false)}
  }
  async function handleComplete(){
    if(!result)return
    setSubmitting(true);setError('')
    try{
      const res=await apiFetch('/api/assessment/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cefr_level:selectedLevel,skill_profile:result.skill_profile,strengths:result.strengths,weaknesses:result.weaknesses,duration_weeks:durationOption.weeks,days_per_week:durationOption.daysPerWeek,goals:selectedGoals,target_language:activeLanguage?.code??undefined})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentCompleteResponse;setCreatedPlanId(data.plan_id)
      if(data.voice_trial?.available&&data.voice_trial.token){setVoiceTrial(data.voice_trial);setStep('voice-trial-offer');setSubmitting(false);return}
      router.push('/plan')
    }catch(err){const msg=err instanceof Error?err.message:'';setError(msg==='ai_service_error'||msg==='ai_service_unavailable'?tCommon('error'):msg||tCommon('error'));setSubmitting(false)}
  }
  function startVoiceTrial(){
    if(!voiceTrial?.token)return
    sessionStorage.setItem('assessment_voice_trial',JSON.stringify({token:voiceTrial.token,durationSeconds:voiceTrial.duration_seconds??300,cefrLevel:selectedLevel,planId:createdPlanId,targetLanguage:activeLanguage?.code}))
    router.push('/conversation')
  }
  async function requestVoiceTrial(){
    if(!existingPlan)return
    setTrialLoading(true);setError('')
    try{
      const res=await apiFetch('/api/assessment/voice-trial',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_language:activeLanguage?.code})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as AssessmentCompleteResponse
      if(data.voice_trial?.available&&data.voice_trial.token){setCreatedPlanId(data.plan_id);setSelectedLevel(data.cefr_level as CEFRLevel);setVoiceTrial(data.voice_trial);setStep('voice-trial-offer');return}
      setError(tCommon('error'))
    }catch(err){setError(err instanceof Error?err.message:tCommon('error'))}finally{setTrialLoading(false)}
  }
  const Forward=rtl?ChevronLeft:ChevronRight
  const Back=rtl?ChevronRight:ChevronLeft
  const score=result?Math.round(result.score*100):0
  return <div className="juba-page-shell reference-resource-page reference-assessment" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-assessment-body{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-assessment-status{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;border:1px solid var(--juba-border);border-radius:6px;font-size:13px;color:var(--juba-muted);}
      .juba-app-shell .reference-assessment-status strong{font-weight:650;color:var(--juba-green-dark);}
      .juba-app-shell .reference-assessment-grid{display:grid;grid-template-columns:minmax(0,1fr) 264px;gap:24px;align-items:start;}
      .juba-app-shell .reference-assessment-grid>div{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-assessment-level{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:16px;}
      .juba-app-shell .reference-assessment-level>strong{display:grid;place-items:center;width:64px;height:72px;border-radius:6px;background:var(--juba-green-soft);color:var(--juba-green-dark);font-size:28px;font-weight:650;}
      .juba-app-shell .reference-assessment-level p{margin:4px 0;font-size:13px;line-height:1.7;color:var(--juba-muted);}
      .juba-app-shell .reference-assessment-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:16px;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .reference-assessment-actions :is(a,button){padding-inline:16px;}
      .juba-app-shell .reference-assessment-score{padding:16px;}
      .juba-app-shell .reference-assessment-score>strong{display:block;font-size:28px;font-weight:650;margin-block-end:12px;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-assessment-track{height:8px;border-radius:3px;overflow:hidden;background:var(--juba-soft);}
      .juba-app-shell .reference-assessment-track>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .reference-assessment-level-picker{display:flex;flex-wrap:wrap;gap:8px;}
      .juba-app-shell .reference-assessment-level-picker button{min-height:40px;padding:8px 12px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-muted);font-size:13px;}
      .juba-app-shell .reference-assessment-level-picker button[aria-pressed="true"]{background:var(--juba-green-soft);color:var(--juba-green-dark);border-color:var(--juba-green);}
      .juba-app-shell .reference-assessment-tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:16px;margin:0;}
      .juba-app-shell .reference-assessment-tags li{padding:6px 10px;border-radius:4px;font-size:12px;background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .reference-assessment-tags[data-warning="true"] li{background:var(--juba-soft);color:var(--juba-muted);}
      .juba-app-shell .reference-assessment-error{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;color:var(--duo-red);font-size:13px;}
      .juba-app-shell .reference-assessment-error button{padding-inline:12px;}
      @media(max-width:1000px){.juba-app-shell .reference-assessment-grid{grid-template-columns:1fr;}}
      @media(max-width:640px){.juba-app-shell .reference-assessment-body,.juba-app-shell .reference-assessment-grid>div{gap:16px;}.juba-app-shell .reference-assessment-level-picker button{min-height:44px;}}
    `}</style>
    <header className="reference-resource-heading"><ClipboardCheck size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{step==='result'?t('resultStep'):step==='voice-trial-offer'?t('voiceTrialLabel'):t('cefrLevel')}</p></div></header>
    {error&&<div className="reference-assessment-error" role="alert"><span>{error}</span>{step==='quiz'&&!currentQuestion&&!evaluating&&<button className="juba-secondary-button" onClick={()=>void evaluateQuiz(answers)}>{tCommon('retry')}</button>}</div>}
    <div className="reference-assessment-body">
      {step==='checking'||(step==='quiz'&&(evaluating||!currentQuestion)&&!error)?<PageLoading label={evaluating?t('evaluating'):tCommon('loading')}/>:null}
      {step==='existing'&&existingPlan&&<div className="reference-assessment-grid"><div><section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('currentLevel')}</h2></header><div className="reference-assessment-level"><strong>{existingPlan.cefr_level}</strong><div><p>{t('assessedOn')}</p><p>{new Date(existingPlan.created_at).toLocaleDateString(locale,{year:'numeric',month:'long',day:'numeric'})}</p></div></div><div className="reference-resource-body"><p>{t('alreadyHasPlan')}</p></div><div className="reference-assessment-actions"><button className="juba-secondary-button" onClick={()=>router.push('/dashboard')}><Back size={16}/>{tCommon('backToDashboard')}</button><button className="juba-primary-button" onClick={()=>setStep('beginner-gate')}>{t('retake')}</button></div></section></div>{canOfferVoiceTrial&&<aside className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('voiceTrialTitle')}</h2><Mic size={18}/></header><div className="reference-resource-body"><p>{t('voiceTrialDesc',{minutes:5})}</p></div><div className="reference-assessment-actions"><button className="juba-primary-button" onClick={()=>void requestVoiceTrial()} disabled={trialLoading}>{trialLoading?'…':t('voiceTrialStart')}<Forward size={16}/></button></div></aside>}</div>}
      {step==='beginner-gate'&&<><BeginnerGate languageCode={activeLanguage?.iso639??''} onBeginner={()=>{setResult({cefr_level:'A1',score:0,skill_profile:{},strengths:[],weaknesses:[]});setSelectedLevel('A1');setAnswers([]);setStep('duration')}} onHasExperience={()=>setShowStartWarning(true)}/><ConfirmDialog open={showStartWarning} title={t('startWarningTitle')} message={t('startWarningMessage')} confirmLabel={t('startWarningConfirm')} onConfirm={()=>{setShowStartWarning(false);startQuiz()}} onCancel={()=>setShowStartWarning(false)}/></>}
      {step==='quiz'&&currentQuestion&&<><section className="reference-assessment-status"><strong>{currentLevel}</strong><span>{questionNumber}/{MAX_QUESTIONS}</span></section><div className="reference-assessment-track" role="progressbar" aria-label={t('title')} aria-valuemin={0} aria-valuemax={MAX_QUESTIONS} aria-valuenow={Math.min(questionNumber,MAX_QUESTIONS)}><span style={{width:Math.min(100,questionNumber/MAX_QUESTIONS*100)+'%'}}/></div><AdaptiveQuizCard question={currentQuestion} questionNumber={questionNumber} totalQuestions={MAX_QUESTIONS} onAnswer={handleAnswer} languageCode={activeLanguage?.code}/></>}
      {step==='result'&&result&&<div className="reference-assessment-grid"><div><section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('cefrLevel')}</h2><CheckCircle2 size={18}/></header><div className="reference-assessment-level"><strong>{result.cefr_level}</strong><div><p>{t('overrideLevel')}</p><div className="reference-assessment-level-picker" role="group" aria-label={t('overrideLevel')}>{CEFR_LEVELS.map(level=><button key={level} aria-pressed={selectedLevel===level} onClick={()=>setSelectedLevel(level)}>{level}</button>)}</div></div></div>{selectedLevel!==result.cefr_level&&<div className="reference-resource-body"><p>{t('suggestedLevel',{aiLevel:result.cefr_level,selectedLevel})}</p></div>}<div className="reference-assessment-actions"><button className="juba-primary-button" onClick={()=>setStep('duration')}>{t('createPlan')}<Forward size={16}/></button></div></section>{result.strengths.length>0&&<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('strengths')}</h2></header><ul className="reference-assessment-tags">{result.strengths.map(strength=><li key={strength} dir="auto">{strength}</li>)}</ul></section>}{result.weaknesses.length>0&&<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('needsWork')}</h2></header><ul className="reference-assessment-tags" data-warning="true">{result.weaknesses.map(weakness=><li key={weakness} dir="auto">{weakness}</li>)}</ul></section>}</div><aside className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{tCommon('score')}</h2></header><div className="reference-assessment-score"><strong>{score}%</strong><div className="reference-assessment-track" role="progressbar" aria-label={tCommon('score')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.max(0,Math.min(100,score))}><span style={{width:Math.max(0,Math.min(100,score))+'%'}}/></div></div></aside></div>}
      {step==='duration'&&<DurationSelector selectedWeeks={durationOption.weeks} selectedGoals={selectedGoals} onSelectDuration={setDurationOption} onToggleGoal={goal=>setSelectedGoals(previous=>previous.includes(goal)?previous.filter(item=>item!==goal):[...previous,goal])} onConfirm={handleComplete} onBack={()=>{const isBeginner=result?.score===0&&result?.cefr_level==='A1'&&answers.length===0;setStep(isBeginner?'beginner-gate':'result')}} cefr_level={selectedLevel} loading={submitting}/>}
      {step==='voice-trial-offer'&&<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('voiceTrialLabel')}</h2><Mic size={20}/></header><div className="reference-assessment-level"><strong>{selectedLevel}</strong><div><p>{t('cefrLevel')}</p><p>{t('voiceTrialTitle')}</p></div></div><div className="reference-resource-body"><p>{t('voiceTrialDesc',{minutes:Math.round((voiceTrial?.duration_seconds??300)/60)})}</p></div><div className="reference-assessment-actions"><button className="juba-primary-button" onClick={startVoiceTrial}>{t('voiceTrialStart')}<Forward size={16}/></button><button className="juba-secondary-button" onClick={()=>router.push('/plan')}>{t('voiceTrialSkip')}</button></div></section>}
    </div>
  </div>
}
