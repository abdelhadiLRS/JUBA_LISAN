'use client'

import {useCallback,useEffect,useRef,useState} from 'react'
import {apiFetch} from '@/lib/api'
import {markLearningProgressUpdated,subscribeToLearningProgressUpdated} from '@/lib/learning-progress'
import type {GoalData,GameSummary,HistoryEntry} from './reference-feature-data'

export function useReferenceFeatures(language:string|undefined){
 const [goal,setGoal]=useState<GoalData|null>(null),[game,setGame]=useState<GameSummary|null>(null),[history,setHistory]=useState<HistoryEntry[]>([])
 const [loading,setLoading]=useState(true),[saving,setSaving]=useState(false)
 const [goalError,setGoalError]=useState(false),[gameError,setGameError]=useState(false),[historyError,setHistoryError]=useState(false),[noPlan,setNoPlan]=useState(false)
 const [saveError,setSaveError]=useState(false),[saved,setSaved]=useState(false)
 const requestVersion=useRef(0),contextVersion=useRef(0),mounted=useRef(false),lock=useRef(false),pendingRefresh=useRef(false)
 const load=useCallback(async()=>{
  if(!mounted.current)return
  if(lock.current){pendingRefresh.current=true;return}
  const request=++requestVersion.current,context=contextVersion.current
  setLoading(true)
  const [goals,games,activity]=await Promise.allSettled([
   apiFetch('/api/progress/goals').then(async r=>{if(r.status===404)return null;if(!r.ok)throw new Error();return await r.json() as GoalData}),
   apiFetch('/api/progress/game-summary').then(async r=>{if(!r.ok)throw new Error();return await r.json() as GameSummary}),
   apiFetch('/api/progress/history?range=week').then(async r=>{if(!r.ok)throw new Error();return await r.json() as {entries:HistoryEntry[]}}),
  ])
  if(!mounted.current||context!==contextVersion.current||request!==requestVersion.current)return
  setGoalError(goals.status==='rejected');setGameError(games.status==='rejected');setHistoryError(activity.status==='rejected')
  setGoal(goals.status==='fulfilled'?goals.value:null);setNoPlan(goals.status==='fulfilled'&&goals.value===null)
  setGame(games.status==='fulfilled'?games.value:null)
  setHistory(activity.status==='fulfilled'&&Array.isArray(activity.value.entries)?activity.value.entries:[])
  setLoading(false)
 },[])
 useEffect(()=>{
  mounted.current=true;contextVersion.current++;requestVersion.current++
  setGoal(null);setGame(null);setHistory([]);setSaved(false);setSaveError(false);setNoPlan(false)
  setGoalError(false);setGameError(false);setHistoryError(false);setLoading(true)
  void load()
  const unsubscribe=subscribeToLearningProgressUpdated(()=>void load())
  return()=>{mounted.current=false;contextVersion.current++;requestVersion.current++;unsubscribe()}
 },[language,load])
 const saveTargets=useCallback(async(daily:number,weekly:number):Promise<boolean>=>{
  if(!mounted.current||lock.current)return false
  if(!Number.isInteger(daily)||daily<1||daily>10000||!Number.isInteger(weekly)||weekly<1||weekly>70000){setSaveError(true);return false}
  lock.current=true;requestVersion.current++
  const context=contextVersion.current
  setSaving(true);setLoading(false);setSaveError(false);setSaved(false)
  try{
   const response=await apiFetch('/api/progress/goals',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({daily_xp_target:daily,weekly_xp_target:weekly})})
   if(!response.ok)throw new Error()
   const updated=await response.json() as GoalData
   // Notify subscribers of a successful server write even if this panel's
   // active language changed; never apply that old-language payload locally.
   markLearningProgressUpdated()
   if(!mounted.current||context!==contextVersion.current)return false
   setGoal(updated);setNoPlan(false);setGoalError(false);setSaved(true)
   return true
  }catch{
   if(mounted.current&&context===contextVersion.current)setSaveError(true)
   return false
  }finally{
   lock.current=false
   if(mounted.current){setSaving(false);if(pendingRefresh.current||context!==contextVersion.current){pendingRefresh.current=false;void load()}}
  }
 },[load])
 return {goal,game,history,loading,saving,goalError,gameError,historyError,noPlan,saveError,saved,load,saveTargets}
}
