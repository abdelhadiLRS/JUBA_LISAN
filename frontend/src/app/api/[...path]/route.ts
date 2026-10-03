import { NextRequest, NextResponse } from 'next/server'
const BACKEND_URL=process.env.BACKEND_URL||'http://localhost:8000'

async function proxy(request:NextRequest,context:{params:Promise<{path:string[]}>}){
  const {path}=await context.params
  const baseUrl=BACKEND_URL.replace(/\/$/,'')
  const backendUrl=`${baseUrl}/api/${path.join('/')}${request.nextUrl.search}`
  const headers=new Headers(request.headers)
  headers.delete('host');headers.delete('content-length');headers.delete('connection')
  const controller=new AbortController()
  const cancel=()=>controller.abort(request.signal.reason)
  if(request.signal.aborted)cancel()
  else request.signal.addEventListener('abort',cancel,{once:true})
  // Allow generation requests longer than ordinary interactive moves.
  const timeout=setTimeout(()=>controller.abort(new DOMException('Backend request timed out','TimeoutError')),path.includes('arena')?18_000:115_000)
  try{
    const init:RequestInit={method:request.method,headers,redirect:'manual',cache:'no-store',signal:controller.signal}
    if(request.method!=='GET'&&request.method!=='HEAD')init.body=await request.arrayBuffer()
    const response=await fetch(backendUrl,init)
    const responseHeaders=new Headers(response.headers)
    responseHeaders.delete('content-encoding');responseHeaders.delete('content-length')
    return new NextResponse(response.body,{status:response.status,statusText:response.statusText,headers:responseHeaders})
  }catch(error){
    const timedOut=controller.signal.aborted&&!request.signal.aborted
    console.error('[JUBA LISAN API proxy] Backend request failed:',error)
    return NextResponse.json({detail:timedOut?'Backend request timed out':'Backend API is unavailable'},{status:timedOut?504:503})
  }finally{clearTimeout(timeout);request.signal.removeEventListener('abort',cancel)}
}
export const GET=proxy
export const POST=proxy
export const PUT=proxy
export const PATCH=proxy
export const DELETE=proxy
export const HEAD=proxy
export const OPTIONS=proxy
