import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import type { AssessmentQuestion } from '@/data/types'
import AdaptiveQuizCard from './AdaptiveQuizCard'

vi.mock('next-intl',()=>({useTranslations:()=> (key:string)=>key}))
vi.mock('@/components/TargetLanguageText',()=>({TargetLanguageText:({children,as:Tag='span',languageCode:_languageCode,...props}: {children:React.ReactNode;as?:'p'|'span';languageCode?:string|null;dir?:string})=><Tag {...props}>{children}</Tag>}))
afterEach(cleanup)
const question={id:'q1',skill:'grammar',difficulty:'A2',question:'Choose the correct word.',options:['First','Second'],correct:'First'} as AssessmentQuestion

describe('AdaptiveQuizCard answer guard',()=>{
  it('accepts only one answer while the question stays mounted',()=>{
    const onAnswer=vi.fn()
    render(<AdaptiveQuizCard question={question} questionNumber={1} totalQuestions={15} onAnswer={onAnswer}/>)
    const option=screen.getByRole('button',{name:/First/})
    fireEvent.click(option)
    fireEvent.click(option)
    fireEvent.click(screen.getByRole('button',{name:/Second/}))
    expect(onAnswer).toHaveBeenCalledTimes(1)
    expect(onAnswer).toHaveBeenCalledWith('First')
    expect((option as HTMLButtonElement).disabled).toBe(true)
  })
  it('allows an answer for a new question without remounting',()=>{
    const onAnswer=vi.fn()
    const {rerender}=render(<AdaptiveQuizCard question={question} questionNumber={1} totalQuestions={15} onAnswer={onAnswer}/>)
    fireEvent.click(screen.getByRole('button',{name:/First/}))
    rerender(<AdaptiveQuizCard question={{...question,id:'q2'}} questionNumber={2} totalQuestions={15} onAnswer={onAnswer}/>)
    fireEvent.click(screen.getByRole('button',{name:/Second/}))
    expect(onAnswer).toHaveBeenCalledTimes(2)
    expect(onAnswer).toHaveBeenLastCalledWith('Second')
  })
  it('allows the same bank question in a new assessment session',()=>{
    const onAnswer=vi.fn()
    const {rerender}=render(<AdaptiveQuizCard question={question} questionNumber={2} totalQuestions={15} onAnswer={onAnswer}/>)
    fireEvent.click(screen.getByRole('button',{name:/First/}))
    rerender(<AdaptiveQuizCard question={question} questionNumber={1} totalQuestions={15} onAnswer={onAnswer}/>)
    fireEvent.click(screen.getByRole('button',{name:/First/}))
    expect(onAnswer).toHaveBeenCalledTimes(2)
  })
})
