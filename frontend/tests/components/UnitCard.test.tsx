import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import React from 'react'
import UnitCard from '@/components/plan/UnitCard'
import UnitDrawer from '@/components/plan/UnitDrawer'
import type { CurriculumUnit } from '@/data/curriculum'
vi.mock('next-intl',()=>({useLocale:()=> 'en',useTranslations:()=> (key:string)=>key}))
vi.mock('next/image',()=>({default:({unoptimized:_unoptimized,priority:_priority,...props}:React.ImgHTMLAttributes<HTMLImageElement>&{unoptimized?:boolean;priority?:boolean})=>React.createElement('img',props)}))
afterEach(cleanup)
beforeEach(()=>vi.clearAllMocks())
type UnitStatus={completed:boolean;active:boolean;locked:boolean;isLevelTest:boolean}
const defaultStatus:UnitStatus={completed:false,active:false,locked:false,isLevelTest:false}
function renderUnitCard(overrides:Partial<{title:string;index:number;lessonCount:number;grammarCount:number;competency:number;status:Partial<UnitStatus>;onClick:()=>void;onStartLesson:()=>void}>={}){
  const props={title:overrides.title??'Basic Greetings',index:overrides.index??0,lessonCount:overrides.lessonCount??5,grammarCount:overrides.grammarCount??2,competency:overrides.competency??.6,status:{...defaultStatus,...overrides.status},onClick:overrides.onClick??vi.fn(),onStartLesson:overrides.onStartLesson}
  return {...render(<UnitCard {...props}/>),props}
}
describe('UnitCard',()=>{
  it('renders completed unit with checkmark',()=>{const {container}=renderUnitCard({status:{completed:true},competency:1});expect(container.querySelector('svg.lucide-check')).toBeInTheDocument()})
  it('renders active unit with play icon',()=>{const {container}=renderUnitCard({status:{active:true}});expect(container.querySelector('svg[class*="play"]')).toBeInTheDocument()})
  it('renders locked unit with lock and locked styling',()=>{const {container}=renderUnitCard({status:{locked:true}});expect(container.querySelector('svg.lucide-lock')).toBeInTheDocument();expect((container.firstChild as HTMLElement).className).toContain('juba-ff-unit-locked')})
  it('renders level test icon and badge',()=>{const {container}=renderUnitCard({status:{isLevelTest:true}});expect(container.querySelector('svg.lucide-ribbon')).toBeInTheDocument();expect(screen.getByText('levelTestLabel')).toBeInTheDocument()})
  it('renders default hollow circle',()=>{const {container}=renderUnitCard();expect(container.querySelector('svg.lucide-circle')).toBeInTheDocument()})
  it('renders padded index',()=>{renderUnitCard({index:3});expect(screen.getByText('04')).toBeInTheDocument()})
  it('renders title',()=>{renderUnitCard({title:'Past Tenses'});expect(screen.getByText('Past Tenses')).toBeInTheDocument()})
  it('renders lesson count',()=>{renderUnitCard();expect(screen.getByText('nLessons')).toBeInTheDocument()})
  it('renders nonzero grammar count',()=>{renderUnitCard({grammarCount:3});expect(screen.getByText('nGrammar')).toBeInTheDocument()})
  it('omits zero grammar count',()=>{renderUnitCard({grammarCount:0});expect(screen.queryByText('nGrammar')).toBeNull()})
  it.each([{value:0,percent:'0%'},{value:.42,percent:'42%'},{value:1,percent:'100%'}])('renders $percent mastery',({value,percent})=>{const {container}=renderUnitCard({competency:value});expect(screen.getByText(percent)).toBeInTheDocument();const track=container.querySelector('.juba-ff-unit-progress') as HTMLElement;expect(track).toBeInTheDocument();expect((track.firstElementChild as HTMLElement).style.width).toBe(percent)})
  it('omits progress for locked units',()=>{const {container}=renderUnitCard({status:{locked:true}});expect(container.querySelector('.juba-ff-unit-progress')).toBeNull();expect(screen.queryByText(/%$/)).toBeNull()})
  it('calls onClick on header activation',()=>{const onClick=vi.fn();renderUnitCard({onClick});fireEvent.click(screen.getByLabelText('unitAriaLabel'));expect(onClick).toHaveBeenCalledTimes(1)})
  it('disables locked header',()=>{const onClick=vi.fn();renderUnitCard({onClick,status:{locked:true}});const button=screen.getByLabelText('unitAriaLabel');expect(button).toBeDisabled();fireEvent.click(button);expect(onClick).not.toHaveBeenCalled()})
  it('shows and activates start for actionable active units',()=>{const onStartLesson=vi.fn();renderUnitCard({status:{active:true},onStartLesson});fireEvent.click(screen.getByRole('button',{name:/start/}));expect(onStartLesson).toHaveBeenCalledTimes(1)})
  it('omits start without callback',()=>{renderUnitCard({status:{active:true}});expect(screen.queryByRole('button',{name:/start/})).toBeNull()})
  it('omits start for inactive units',()=>{renderUnitCard({onStartLesson:vi.fn()});expect(screen.queryByRole('button',{name:/start/})).toBeNull()})
  it('omits start for locked units',()=>{renderUnitCard({status:{locked:true},onStartLesson:vi.fn()});expect(screen.queryByRole('button',{name:/start/})).toBeNull()})
})
const mockUnit:CurriculumUnit={id:'unit-a1-1',level:'A1',unit_number:1,title:'Greetings & Introductions',default_weeks:2,grammar_points:['presente de indicativo','verbos ser/estar'],vocabulary_set_ids:['v1','v2'],lesson_types:['grammar','vocabulary','reading'],competency_checklist:['Can greet people','Can introduce oneself']}
const mockLessons=[{id:1,title:'Verb Conjugation',lesson_type:'grammar',week:1,day:1,completed:true,action:'review' as const},{id:2,title:'Common Phrases',lesson_type:'vocabulary',week:1,day:2,completed:false,action:'continue' as const},{id:3,title:'Reading Comprehension',lesson_type:'reading',week:2,day:1,completed:false,action:'start' as const}]
function renderUnitDrawer(overrides:Partial<{unit:CurriculumUnit;lessons:Array<{id:number|null;title:string;lesson_type:string;week:number;day:number;completed:boolean;action?:'start'|'continue'|'review'}>;onClose:()=>void;onStartLesson:(id:number)=>void;onStartUnit:()=>void}>={}){
  const props={unit:overrides.unit??mockUnit,lessons:overrides.lessons??mockLessons,onClose:overrides.onClose??vi.fn(),onStartLesson:overrides.onStartLesson??vi.fn(),onStartUnit:overrides.onStartUnit??vi.fn()}
  return {...render(<UnitDrawer {...props}/>),props}
}
describe('UnitDrawer',()=>{
  it('renders level label and named dialog',()=>{renderUnitDrawer();expect(screen.getByText(/A1/)).toBeInTheDocument();expect(screen.getByText(/unitLabel/)).toBeInTheDocument();expect(screen.getByRole('dialog',{name:mockUnit.title})).toBeInTheDocument()})
  it('renders grammar content',()=>{renderUnitDrawer();expect(screen.getByText('grammarCovered')).toBeInTheDocument();expect(screen.getByText('presente de indicativo')).toBeInTheDocument();expect(screen.getByText('verbos ser/estar')).toBeInTheDocument()})
  it('omits empty grammar section',()=>{renderUnitDrawer({unit:{...mockUnit,grammar_points:[]}});expect(screen.queryByText('grammarCovered')).toBeNull()})
  it('renders all lesson titles and section heading',()=>{renderUnitDrawer();expect(screen.getByRole('heading',{name:'lessonsHeader'})).toBeInTheDocument();mockLessons.forEach(lesson=>expect(screen.getByText(lesson.title)).toBeInTheDocument())})
  it('marks completed lessons with a completed node without hiding their titles',()=>{const {container}=renderUnitDrawer();const node=screen.getByText('Verb Conjugation').closest('li')?.querySelector('[data-done="true"]');expect(node).toBeTruthy();expect(node?.querySelector('svg.lucide-check')).toBeTruthy();expect(container.querySelectorAll('svg.lucide-circle')).toHaveLength(2)})
  it('renders lesson type and week/day info',()=>{renderUnitDrawer();expect(screen.getByText(/lessonTypes\.grammar/)).toBeInTheDocument();expect(screen.getByText(/lessonTypes\.vocabulary/)).toBeInTheDocument();expect(screen.getByText(/lessonTypes\.reading/)).toBeInTheDocument();expect(screen.getAllByText(/weekDay/)).toHaveLength(3)})
  it('renders empty lesson state',()=>{renderUnitDrawer({lessons:[]});expect(screen.getByText('noLessons')).toBeInTheDocument()})
  it('exposes semantic lesson actions',()=>{renderUnitDrawer();expect(screen.getByRole('button',{name:'reviewLesson'})).toBeInTheDocument();expect(screen.getByRole('button',{name:'resume'})).toBeInTheDocument();expect(screen.getByRole('button',{name:'startLearning'})).toBeInTheDocument()})
  it('does not offer a lesson action without an ID',()=>{renderUnitDrawer({lessons:[{id:null,title:'Pending Content',lesson_type:'review',week:3,day:1,completed:false},{id:4,title:'Final Test',lesson_type:'review',week:3,day:2,completed:false,action:'start'}]});expect(screen.getAllByRole('button',{name:'startLearning'})).toHaveLength(1)})
  it('resumes the correct lesson',()=>{const onStartLesson=vi.fn();renderUnitDrawer({onStartLesson});fireEvent.click(screen.getByRole('button',{name:'resume'}));expect(onStartLesson).toHaveBeenCalledTimes(1);expect(onStartLesson).toHaveBeenCalledWith(2)})
  it('opens completed lesson for review',()=>{const onStartLesson=vi.fn();renderUnitDrawer({onStartLesson});fireEvent.click(screen.getByRole('button',{name:'reviewLesson'}));expect(onStartLesson).toHaveBeenCalledWith(1)})
  it('invokes explicit unit start',()=>{const onStartUnit=vi.fn();renderUnitDrawer({onStartUnit});fireEvent.click(screen.getByRole('button',{name:'start',exact:true}));expect(onStartUnit).toHaveBeenCalledTimes(1)})
  it('closes via header close',()=>{const onClose=vi.fn();const {container}=renderUnitDrawer({onClose});fireEvent.click(container.querySelector('button[aria-label="close"]')!);expect(onClose).toHaveBeenCalledTimes(1)})
  it('closes via footer close',()=>{const onClose=vi.fn();renderUnitDrawer({onClose});const button=screen.getAllByRole('button',{name:'close'}).find(item=>item.textContent==='close');fireEvent.click(button!);expect(onClose).toHaveBeenCalledTimes(1)})
  it('closes on Escape',()=>{const onClose=vi.fn();renderUnitDrawer({onClose});fireEvent.keyDown(document,{key:'Escape'});expect(onClose).toHaveBeenCalledTimes(1)})
  it('does not close for Enter',()=>{const onClose=vi.fn();renderUnitDrawer({onClose});fireEvent.keyDown(document,{key:'Enter'});expect(onClose).not.toHaveBeenCalled()})
  it('closes on backdrop only',()=>{const onClose=vi.fn();const {container}=renderUnitDrawer({onClose});fireEvent.mouseDown(screen.getByText('Verb Conjugation'));expect(onClose).not.toHaveBeenCalled();fireEvent.mouseDown(container.firstChild as HTMLElement);expect(onClose).toHaveBeenCalledTimes(1)})
})
