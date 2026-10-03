export function nextLessonFromSources(journey:{next_lesson_id:number|null}|null,today:Array<{id:number|null;is_completed?:boolean}>):number|null{
 // A successful authoritative null means no next lesson, not a failed lookup.
 if(journey!==null)return journey.next_lesson_id
 return today.find(lesson=>lesson.id!==null&&!lesson.is_completed)?.id??null
}
