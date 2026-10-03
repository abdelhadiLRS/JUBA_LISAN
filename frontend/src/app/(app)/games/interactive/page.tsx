'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { Brain, Link2, ListOrdered, Puzzle, ChevronRight, ChevronLeft, Gamepad2 } from 'lucide-react'

type Lang='ar'|'fr'|'en'
const copy={
  ar:{title:'الألعاب التفاعلية',subtitle:'تدريبات عملية للذاكرة والمطابقة والترتيب وبناء الجمل.',memory:'لعبة الذاكرة',memoryDesc:'طابق البطاقات وأكمل جميع الأزواج.',matching:'لعبة المطابقة',matchingDesc:'اربط كل كلمة بترجمتها الصحيحة.',ordering:'لعبة الترتيب',orderingDesc:'رتّب العناصر في التسلسل الصحيح.',sentenceBuilder:'بناء الجمل',sentenceBuilderDesc:'رتّب الكلمات لتكوين جملة صحيحة.',start:'ابدأ',back:'العودة إلى مركز الألعاب',language:'اللغة'},
  fr:{title:'Jeux interactifs',subtitle:'Des activités pratiques de mémoire, association, classement et construction de phrases.',memory:'Jeu de mémoire',memoryDesc:'Associe les cartes et complète toutes les paires.',matching:'Jeu d’association',matchingDesc:'Relie chaque mot à sa bonne traduction.',ordering:'Jeu de classement',orderingDesc:'Place les éléments dans le bon ordre.',sentenceBuilder:'Construction de phrases',sentenceBuilderDesc:'Remets les mots dans le bon ordre.',start:'Commencer',back:'Retour aux jeux',language:'Langue'},
  en:{title:'Interactive games',subtitle:'Hands-on practice for memory, matching, ordering, and sentence building.',memory:'Memory game',memoryDesc:'Match the cards and complete every pair.',matching:'Matching game',matchingDesc:'Connect each word to its correct translation.',ordering:'Ordering game',orderingDesc:'Place the items in the correct sequence.',sentenceBuilder:'Sentence builder',sentenceBuilderDesc:'Arrange the words into a correct sentence.',start:'Start',back:'Back to games',language:'Language'},
} as const
export default function InteractiveGamesPage(){
  const [lang,setLang]=useState<Lang>('ar')
  useEffect(()=>{const value=new URLSearchParams(window.location.search).get('lang');if(value==='ar'||value==='fr'||value==='en')setLang(value)},[])
  const rtl=lang==='ar'
  const t=copy[lang]
  const cards=[{href:'/games/memory',title:t.memory,desc:t.memoryDesc,icon:Brain},{href:'/games/matching',title:t.matching,desc:t.matchingDesc,icon:Link2},{href:'/games/ordering',title:t.ordering,desc:t.orderingDesc,icon:ListOrdered},{href:'/games/sentence-builder',title:t.sentenceBuilder,desc:t.sentenceBuilderDesc,icon:Puzzle}]
  return <div className="juba-page-shell reference-interactive-index" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-interactive-index{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-interactive-header{display:flex;align-items:center;gap:16px;min-height:100px;}
      .juba-app-shell .reference-interactive-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-interactive-header h1{font-size:28px;font-weight:650;margin:0;}
      .juba-app-shell .reference-interactive-header p{font-size:14px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-game-language{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--juba-border);border-radius:6px;font-size:13px;}
      .juba-app-shell .reference-game-language>span{margin-inline-end:auto;color:var(--juba-muted);}
      .juba-app-shell .reference-game-language button{min-height:36px;padding:6px 12px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-muted);font-size:12px;}
      .juba-app-shell .reference-game-language button[aria-pressed="true"]{color:var(--juba-green-dark);background:var(--juba-green-soft);border-color:var(--juba-green);}
      .juba-app-shell .reference-game-list{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-game-row{display:grid;grid-template-columns:40px minmax(0,1fr) auto;align-items:center;gap:16px;padding:20px 16px;color:var(--juba-ink);text-decoration:none;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-game-row:last-child{border:0;}
      .juba-app-shell .reference-game-row:hover{background:var(--juba-green-soft);}
      .juba-app-shell .reference-game-row>svg{color:var(--juba-green);width:32px;height:32px;}
      .juba-app-shell .reference-game-row strong{font-size:15px;font-weight:650;}
      .juba-app-shell .reference-game-row p{font-size:13px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-game-row>span{display:flex;align-items:center;gap:8px;color:var(--juba-green-dark);font-size:12px;font-weight:650;}
      .juba-app-shell .reference-games-back{display:inline-flex;align-items:center;gap:8px;min-height:44px;color:var(--juba-muted);font-size:13px;align-self:flex-start;}
      @media(max-width:640px){.juba-app-shell .reference-interactive-index{gap:16px;}.juba-app-shell .reference-interactive-header h1{font-size:24px;}.juba-app-shell .reference-game-language button{min-height:44px;}.juba-app-shell .reference-game-row{grid-template-columns:32px minmax(0,1fr);gap:12px;padding:16px;}.juba-app-shell .reference-game-row>span{grid-column:2;}.juba-app-shell .reference-interactive-header>svg{display:none;}}
    `}</style>
    <header className="reference-interactive-header"><Gamepad2 size={40} aria-hidden="true"/><div><h1>{t.title}</h1><p>{t.subtitle}</p></div></header>
    <div className="reference-game-language" role="group" aria-label={t.language}><span>{t.language}</span>{(['ar','fr','en'] as Lang[]).map(value=><button key={value} aria-pressed={lang===value} onClick={()=>setLang(value)}>{value.toUpperCase()}</button>)}</div>
    <section className="reference-game-list" aria-label={t.title}>{cards.map(({href,title,desc,icon:Icon})=><Link href={href+'?lang='+lang} key={href} className="reference-game-row"><Icon aria-hidden="true"/><div><strong>{title}</strong><p>{desc}</p></div><span>{t.start}{rtl?<ChevronLeft size={16}/>:<ChevronRight size={16}/>}</span></Link>)}</section>
    <Link className="reference-games-back" href="/games">{rtl?<ChevronRight size={16}/>:<ChevronLeft size={16}/>} {t.back}</Link>
  </div>
}
