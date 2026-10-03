import {describe,it,expect} from 'vitest'
import {readProductSelection,productQuery} from './subscription-selection'
describe('Product selection contract',()=>{
 it('preserves all product and interval pairs',()=>{for(const tier of ['free','go','plus'])for(const interval of ['monthly','yearly']){const params=new URLSearchParams({tier,interval});const selected=readProductSelection(params);expect(productQuery(selected)).toBe(`tier=${tier}&interval=${interval}`)}})
 it('maps an old interval-only link to Plus',()=>{expect(readProductSelection(new URLSearchParams('plan=yearly'))).toEqual({tier:'plus',interval:'yearly'})})
 it('rejects invalid values rather than granting a product',()=>{expect(readProductSelection(new URLSearchParams('tier=admin&interval=monthly'))).toBeNull();expect(readProductSelection(new URLSearchParams('tier=go&interval=forever'))).toBeNull()})
})
