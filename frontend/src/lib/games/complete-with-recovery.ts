import {apiFetch} from '@/lib/api'
import type {GameSessionResult} from './persist'

/** Never re-award XP locally after an ambiguous completion response. */
export async function completeWithRecovery(sessionId:string, payload:object):Promise<GameSessionResult>{
  let completionError:unknown
  let recoverable=false
  try{
    const response=await apiFetch('/api/progress/game-session/complete',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload),
    })
    // A conflict can mean that a previous request committed, but its response
    // never reached us. Validation/auth errors must remain errors.
    recoverable=response.status===409||response.status>=500
    if(!response.ok)throw new Error(`Game session completion failed: ${response.status}`)
    // Even an unreadable successful response is an ambiguous committed write.
    recoverable=true
    return await response.json() as GameSessionResult
  }catch(error){
    completionError=error
    // Network failures before/after headers can both follow a committed write.
    if(error instanceof TypeError)recoverable=true
  }
  if(recoverable){
    try{
      const recovered=await apiFetch(`/api/progress/game-session/${encodeURIComponent(sessionId)}/result`)
      if(recovered.ok)return await recovered.json() as GameSessionResult
    }catch{
      // Recovery failure is not proof that completion failed or succeeded.
    }
  }
  throw completionError instanceof Error?completionError:new Error('Game result could not be confirmed')
}
