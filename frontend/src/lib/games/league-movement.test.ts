import {describe,expect,it} from 'vitest'
import {projectedMovement,settledMovement} from './league-movement'

describe('League movement projections mirror server progression',()=>{
  it('keeps divisions with fewer than five eligible learners unchanged',()=>{
    expect(projectedMovement('silver',1,100,4)).toBe('stay')
    expect(projectedMovement('silver',4,0,4)).toBe('stay')
  })
  it('requires positive XP for promotion',()=>{
    expect(projectedMovement('silver',1,0,10)).toBe('stay')
    expect(projectedMovement('silver',1,100,10)).toBe('promotion')
  })
  it('uses exact top and bottom rank boundaries',()=>{
    expect(projectedMovement('silver',2,100,10)).toBe('promotion')
    expect(projectedMovement('silver',3,90,10)).toBe('stay')
    expect(projectedMovement('silver',8,20,10)).toBe('stay')
    expect(projectedMovement('silver',9,10,10)).toBe('demotion')
    expect(projectedMovement('silver',10,0,10)).toBe('demotion')
  })
  it('does not split a shared rank at a cutoff',()=>{
    // Three tied learners may all share rank two in a top-two division.
    expect(projectedMovement('gold',2,100,10)).toBe('promotion')
    // Three tied bottom learners share rank eight: none exceeds rank eight.
    expect(projectedMovement('gold',8,10,10)).toBe('stay')
  })
  it('respects Bronze and Diamond bounds',()=>{
    expect(projectedMovement('bronze',10,0,10)).toBe('stay')
    expect(projectedMovement('diamond',1,100,10)).toBe('stay')
    expect(projectedMovement('diamond',10,0,10)).toBe('demotion')
  })
  it('handles the five-player minimum',()=>{
    expect(projectedMovement('silver',1,1,5)).toBe('promotion')
    expect(projectedMovement('silver',4,0,5)).toBe('stay')
    expect(projectedMovement('silver',5,0,5)).toBe('demotion')
  })
  it('does not infer settled decisions without a persisted next tier',()=>{
    expect(settledMovement('silver',null)).toBeNull()
    expect(settledMovement('silver','gold')).toBe('promotion')
    expect(settledMovement('silver','bronze')).toBe('demotion')
    expect(settledMovement('silver','silver')).toBe('stay')
    expect(settledMovement('unknown','gold')).toBeNull()
  })
  it('rejects unknown divisions and missing ranks as projections',()=>{
    expect(projectedMovement('unknown',1,100,10)).toBe('stay')
    expect(projectedMovement('silver',0,100,10)).toBe('stay')
  })
})
