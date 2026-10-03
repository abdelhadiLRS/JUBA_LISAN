'use client'

import { useTranslations } from 'next-intl'
import type { AssessmentQuestion } from '@/data/types'
import { TargetLanguageText } from '@/components/TargetLanguageText'
interface Props{question:AssessmentQuestion;questionNumber:number;totalQuestions:number;onAnswer:(answer:string)=>void;languageCode?:string|null}
export default function AdaptiveQuizCard({question,questionNumber,totalQuestions,onAnswer,languageCode}:Props){
  const t=useTranslations('assessment')
  const progress=totalQuestions>0?Math.max(0,Math.min(100,Math.round(questionNumber/totalQuestions*100))):0
  const skillLabelMap:Record<string,string>={grammar:t('skills.grammar'),vocabulary:t('skills.vocabulary'),reading:t('skills.reading')}
  return <section className="reference-adaptive-quiz">
    <style>{`
      .juba-app-shell .reference-adaptive-quiz{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-adaptive-quiz>header{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:16px;border-block-end:1px solid var(--juba-border);font-size:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-adaptive-quiz>header>div{display:flex;align-items:center;gap:8px;}
      .juba-app-shell .reference-adaptive-tag{padding:4px 8px;border-radius:4px;background:var(--juba-green-soft);color:var(--juba-green-dark);font-size:11px;}
      .juba-app-shell .reference-adaptive-progress{height:4px;background:var(--juba-soft);overflow:hidden;}
      .juba-app-shell .reference-adaptive-progress>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .reference-adaptive-question{padding:24px 16px;font-size:18px;line-height:1.7;color:var(--juba-ink);}
      .juba-app-shell .reference-adaptive-question p{margin:0;overflow-wrap:anywhere;}
      .juba-app-shell .reference-adaptive-options{display:flex;flex-direction:column;padding:0 16px 16px;gap:12px;}
      .juba-app-shell .reference-adaptive-options button{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;min-height:48px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-ink);text-align:start;font-size:14px;line-height:1.6;}
      .juba-app-shell .reference-adaptive-options button:hover{border-color:var(--juba-green);background:var(--juba-green-soft);}
      .juba-app-shell .reference-adaptive-option-key{display:grid;place-items:center;width:24px;height:24px;flex:none;border-radius:4px;background:var(--juba-soft);color:var(--juba-muted);font-size:11px;}
    `}</style>
    <header><span>{t('step2',{questionNumber,totalQuestions})}</span><div><span className="reference-adaptive-tag">{question.difficulty}</span><span className="reference-adaptive-tag">{skillLabelMap[question.skill]??question.skill}</span></div></header><div className="reference-adaptive-progress" role="progressbar" aria-label={t('step2',{questionNumber,totalQuestions})} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{width:progress+'%'}}/></div><div className="reference-adaptive-question"><TargetLanguageText as="p" languageCode={languageCode} dir="auto">{question.question}</TargetLanguageText></div><div className="reference-adaptive-options">{question.options.map((option,index)=><button key={option} onClick={()=>onAnswer(option)}><span className="reference-adaptive-option-key" aria-hidden="true">{String.fromCharCode(65+index)}</span><TargetLanguageText languageCode={languageCode} dir="auto">{option}</TargetLanguageText></button>)}</div>
  </section>
}
