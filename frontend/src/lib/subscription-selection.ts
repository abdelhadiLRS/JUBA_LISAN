export type ProductTier = 'free'|'go'|'plus'
export type ProductInterval = 'monthly'|'yearly'
export type ProductSelection = {tier:ProductTier;interval:ProductInterval}
const KEY='juba_subscription_selection'
export function readProductSelection(params:{get:(key:string)=>string|null}):ProductSelection|null{
 const tier=params.get('tier'),interval=params.get('interval'),legacy=params.get('plan')
 if(tier==='free'||tier==='go'||tier==='plus')return interval==='monthly'||interval==='yearly'?{tier,interval}:null
 if(!tier&&!interval&&(legacy==='monthly'||legacy==='yearly'))return {tier:'plus',interval:legacy}
 return null
}
export function productQuery(selection:ProductSelection|null):string{
 return selection?`tier=${selection.tier}&interval=${selection.interval}`:''
}
export function rememberProductSelection(selection:ProductSelection|null){
 if(typeof window==='undefined')return
 try{if(selection)sessionStorage.setItem(KEY,JSON.stringify(selection));else sessionStorage.removeItem(KEY)}catch{}
}
export function pendingProductSelection():ProductSelection|null{
 if(typeof window==='undefined')return null
 try{const item=JSON.parse(sessionStorage.getItem(KEY)||'null');if(item&&(item.tier==='free'||item.tier==='go'||item.tier==='plus')&&(item.interval==='monthly'||item.interval==='yearly'))return item}catch{}
 return null
}
