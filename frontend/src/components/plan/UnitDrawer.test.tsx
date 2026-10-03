import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import type { CurriculumUnit } from '@/data/curriculum'
import UnitDrawer from './UnitDrawer'
vi.mock('next-intl',()=>({useLocale:()=> 'en',useTranslations:()=> (key:string)=>key}))
afterEach(cleanup)
const unit:CurriculumUnit={id:'u1',level:'A1',unit_number:1,title:'First unit',default_weeks:1,grammar_points:['Present tense'],vocabulary_set_ids:[],lesson_types:['grammar'],competency_checklist:[]}
const lesson={id:42,title:'First lesson',lesson_type:'grammar',week:1,day:1,completed:false,action:'start' as const}
describe('UnitDrawer start action',()=>{
  it('starts an actionable lesson when the caller has no unit callback',()=>{
    const onStartLesson=vi.fn()
    render(<UnitDrawer unit={unit} lessons={[lesson]} onClose={vi.fn()} onStartLesson={onStartLesson}/>)
    fireEvent.click(screen.getByRole('button',{name:'start',exact:true}))
    expect(onStartLesson).toHaveBeenCalledWith(42)
  })
  it('honors an explicit onStartUnit callback',()=>{
    const onStartUnit=vi.fn()
    const onStartLesson=vi.fn()
    render(<UnitDrawer unit={unit} lessons={[lesson]} onClose={vi.fn()} onStartLesson={onStartLesson} onStartUnit={onStartUnit}/>)
    fireEvent.click(screen.getByRole('button',{name:'start',exact:true}))
    expect(onStartUnit).toHaveBeenCalledTimes(1)
    expect(onStartLesson).not.toHaveBeenCalled()
  })
  it('does not invent a start action for a locked lesson',()=>{
    render(<UnitDrawer unit={unit} lessons={[{...lesson,action:undefined}]} onClose={vi.fn()} onStartLesson={vi.fn()}/>)
    expect(screen.queryByRole('button',{name:'start',exact:true})).toBeNull()
  })
  it('closes on Escape and exposes a labeled dialog',()=>{
    const onClose=vi.fn()
    render(<UnitDrawer unit={unit} lessons={[lesson]} onClose={onClose} onStartLesson={vi.fn()}/>)
    expect(screen.getByRole('dialog',{name:'First unit'})).toBeTruthy()
    fireEvent.keyDown(document,{key:'Escape'})
    expect(onClose).toHaveBeenCalledTimes(1)
  })
})
