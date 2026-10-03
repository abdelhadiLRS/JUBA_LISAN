import { describe, expect, it } from 'vitest'
import type { AssessmentQuestion } from '@/data/types'
import { resolveAssessmentTransition } from './assessment-transition'
const question={id:'q1',skill:'grammar',difficulty:'A2',question:'Choose.',options:['one','two'],correct:'one'} as AssessmentQuestion
const recorded=[{question_id:'q1',correct:true}]
describe('assessment transition',()=>{
  it('includes the final recorded answer when the current level bank is exhausted',()=>{
    const result=resolveAssessmentTransition([question],new Set(['q1']),'A2',recorded,15)
    expect(result).toEqual({kind:'evaluate',answers:recorded})
    if(result.kind==='evaluate')expect(result.answers).toBe(recorded)
  })
  it('evaluates at the question limit even when more questions exist',()=>{
    expect(resolveAssessmentTransition([{...question,id:'q2'}],new Set(),'A2',recorded,1)).toEqual({kind:'evaluate',answers:recorded})
  })
  it('chooses only unused questions at the current difficulty',()=>{
    const next={...question,id:'q2'}
    const result=resolveAssessmentTransition([question,next,{...question,id:'q3',difficulty:'B1'}],new Set(['q1']),'A2',recorded,15,()=>0)
    expect(result).toEqual({kind:'question',question:next})
  })
  it('does not mutate the set of questions already used',()=>{
    const used=new Set<string>()
    resolveAssessmentTransition([question],used,'A2',[],15,()=>0)
    expect(used.size).toBe(0)
  })
})
