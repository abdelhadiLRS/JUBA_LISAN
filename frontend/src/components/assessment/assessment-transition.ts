import type { AssessmentQuestion, CEFRLevel } from '@/data/types'

/** Preserve the adaptive policy while always evaluating the just-recorded answer. */
export function resolveAssessmentTransition<T>(
  bank:AssessmentQuestion[],
  usedIds:ReadonlySet<string>,
  level:CEFRLevel,
  answers:T[],
  maxQuestions:number,
  random:()=>number=Math.random,
):{kind:'question';question:AssessmentQuestion}|{kind:'evaluate';answers:T[]}{
  if(answers.length>=maxQuestions)return {kind:'evaluate',answers}
  const available=bank.filter(question=>!usedIds.has(question.id)&&question.difficulty===level)
  if(!available.length)return {kind:'evaluate',answers}
  const sample=Math.max(0,Math.min(.999999999,random()))
  return {kind:'question',question:available[Math.floor(sample*available.length)]}
}
