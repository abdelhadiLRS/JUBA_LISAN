import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const mocks=vi.hoisted(()=>({fetch:vi.fn(),logout:vi.fn(),setTokens:vi.fn(),inc:vi.fn(),dec:vi.fn(),state:{accessToken:'old-token',user:{id:1}}}))
vi.mock('@/store/auth',()=>({useAuthStore:{getState:()=>({...mocks.state,logout:mocks.logout,setTokens:mocks.setTokens})}}))
vi.mock('@/store/loading',()=>({useLoadingStore:{getState:()=>({inc:mocks.inc,dec:mocks.dec})}}))
const reply=(status:number,body:unknown={})=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json'}})
beforeEach(()=>{vi.resetModules();vi.clearAllMocks();mocks.state.accessToken='old-token';mocks.state.user={id:1};mocks.setTokens.mockImplementation(token=>{mocks.state.accessToken=token});vi.stubGlobal('fetch',mocks.fetch)})
afterEach(()=>{vi.useRealTimers();vi.unstubAllGlobals()})

describe('API session and request lifecycle',()=>{
  it('preserves auth on temporary refresh failure and does not replay the request',async()=>{
    mocks.fetch.mockResolvedValueOnce(reply(401)).mockResolvedValueOnce(reply(503))
    const {apiFetch,AuthSessionUnavailable}=await import('./api')
    await expect(apiFetch('/api/progress/summary')).rejects.toBeInstanceOf(AuthSessionUnavailable)
    expect(mocks.logout).not.toHaveBeenCalled();expect(mocks.fetch).toHaveBeenCalledTimes(2);expect(mocks.dec).toHaveBeenCalledTimes(1)
  })
  it('preserves auth on refresh network errors',async()=>{
    mocks.fetch.mockResolvedValueOnce(reply(401)).mockRejectedValueOnce(new TypeError('network'))
    const {apiFetch}=await import('./api')
    await expect(apiFetch('/api/progress/summary')).rejects.toThrow('Could not renew')
    expect(mocks.logout).not.toHaveBeenCalled()
  })
  it('logs out only when refresh credentials are rejected',async()=>{
    mocks.fetch.mockResolvedValueOnce(reply(401)).mockResolvedValueOnce(reply(401))
    const {apiFetch}=await import('./api')
    expect((await apiFetch('/api/progress/summary')).status).toBe(401)
    expect(mocks.logout).toHaveBeenCalledTimes(1)
  })
  it('rotates and replays after a successful refresh',async()=>{
    mocks.fetch.mockResolvedValueOnce(reply(401)).mockResolvedValueOnce(reply(200,{access_token:'new-token'})).mockResolvedValueOnce(reply(200,{ok:true}))
    const {apiFetch}=await import('./api')
    expect((await apiFetch('/api/progress/summary')).status).toBe(200)
    expect(mocks.setTokens).toHaveBeenCalledWith('new-token')
    expect(mocks.fetch.mock.calls[2][1].headers.get('Authorization')).toBe('Bearer new-token')
  })
  it('times out arcade requests even when the caller supplies a signal',async()=>{
    vi.useFakeTimers()
    mocks.fetch.mockImplementation((_url:string,options:RequestInit)=>new Promise((_resolve,reject)=>options.signal?.addEventListener('abort',()=>reject(options.signal?.reason))))
    const {apiFetch}=await import('./api')
    const controller=new AbortController()
    const promise=apiFetch('/api/progress/game-session/arena',{method:'POST',signal:controller.signal})
    const assertion=expect(promise).rejects.toBeInstanceOf(DOMException)
    await vi.advanceTimersByTimeAsync(20_001);await assertion
    expect(mocks.fetch.mock.calls[0][1].signal.aborted).toBe(true);expect(controller.signal.aborted).toBe(false)
    expect(mocks.dec).toHaveBeenCalledTimes(1)
  })
  it('cancels a request promptly on caller abort',async()=>{
    mocks.fetch.mockImplementation((_url:string,options:RequestInit)=>new Promise((_resolve,reject)=>options.signal?.addEventListener('abort',()=>reject(new DOMException('aborted','AbortError')))))
    const {apiFetch}=await import('./api')
    const controller=new AbortController(),promise=apiFetch('/api/progress/game-session/arena',{signal:controller.signal})
    const assertion=expect(promise).rejects.toThrow('aborted');controller.abort();await assertion
    expect(mocks.dec).toHaveBeenCalledTimes(1)
  })
})
