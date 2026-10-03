import {describe,expect,it} from 'vitest'
import {nextLessonFromSources} from './plan-next-lesson'
describe('Authoritative next lesson',()=>{
 it('preserves the journey lesson over a different today lesson',()=>expect(nextLessonFromSources({next_lesson_id:10},[{id:20,is_completed:false}])).toBe(10))
 it('preserves authoritative null rather than reviving a today lesson',()=>expect(nextLessonFromSources({next_lesson_id:null},[{id:20,is_completed:false}])).toBeNull())
 it('falls back to today only without an authoritative journey',()=>expect(nextLessonFromSources(null,[{id:null},{id:5,is_completed:true},{id:20,is_completed:false}])).toBe(20))
 it('does not clear a journey lesson when today is empty',()=>expect(nextLessonFromSources({next_lesson_id:10},[])).toBe(10))
 it('returns null when no actionable source exists',()=>expect(nextLessonFromSources(null,[{id:5,is_completed:true}])).toBeNull())
})
