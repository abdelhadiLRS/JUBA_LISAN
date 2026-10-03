'use client'
import {type ReactNode} from 'react'
import Link from 'next/link'
import {useLocale} from 'next-intl'
import {ChevronRight, CreditCard, type LucideIcon} from 'lucide-react'

interface SettingsPageHeaderProps{title:string;eyebrow:string;description?:string}
export function SettingsPageHeader({title,eyebrow,description}:SettingsPageHeaderProps){
 return <header className="reference-settings-heading"><p>{eyebrow}</p><h1>{title}</h1>{description&&<div>{description}</div>}<style>{`
 .juba-app-shell .reference-settings-heading{padding-block:20px;min-height:100px}
 .juba-app-shell .reference-settings-heading>p{font-size:11px;color:var(--juba-green-dark);margin:0 0 6px}
 .juba-app-shell .reference-settings-heading h1{font-size:28px;font-weight:650;margin:0;line-height:1.3}
 .juba-app-shell .reference-settings-heading>div{font-size:14px;line-height:1.6;color:var(--juba-muted);max-width:70ch;margin-block-start:8px}
 .juba-app-shell .reference-settings-nav{display:flex;align-items:center;gap:8px;border-block-end:1px solid var(--juba-border);overflow-x:auto;padding-block:8px}
 .juba-app-shell .reference-settings-nav a{display:flex;align-items:center;gap:8px;min-height:44px;white-space:nowrap;font-size:12px;color:var(--juba-muted);padding:8px 12px;text-decoration:none;border-radius:5px}
 .juba-app-shell .reference-settings-nav a:hover{color:var(--juba-green-dark);background:var(--juba-green-soft)}
 .juba-app-shell .reference-settings-panel{scroll-margin-block-start:88px;display:flex;flex-direction:column;gap:16px;margin-block-start:24px}
 .juba-app-shell .reference-settings-panel>h2{font-size:16px;font-weight:650;margin:0}
 .juba-app-shell .reference-settings-action{display:grid;grid-template-columns:36px minmax(0,1fr) 16px;align-items:center;gap:12px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);color:var(--juba-ink);text-decoration:none}
 .juba-app-shell .reference-settings-action:hover{background:var(--juba-green-soft)}
 .juba-app-shell .reference-settings-action>span{display:grid;place-items:center;width:36px;height:36px;background:var(--juba-green-soft);border-radius:5px;color:var(--juba-green-dark)}
 .juba-app-shell .reference-settings-action strong{font-size:14px;font-weight:600}
 .juba-app-shell .reference-settings-action p{font-size:12px;line-height:1.5;color:var(--juba-muted);margin:4px 0 0}
 .juba-app-shell[dir="rtl"] .reference-settings-action>svg{transform:scaleX(-1)}
 @media(max-width:640px){.juba-app-shell .reference-settings-heading h1{font-size:24px}}
 `}</style></header>
}
export function SettingsNav({items}:{items:{href:string;label:string;icon:LucideIcon}[]}){
 const ar=useLocale().startsWith('ar')
 const entries=items.some(item=>item.href==='/settings/subscription')?items:[...items,{href:'/settings/subscription',label:ar?'الاشتراك والاستخدام':'Subscription and usage',icon:CreditCard}]
 return <nav className="reference-settings-nav">{entries.map(({href,label,icon:Icon})=><Link key={href} href={href}><Icon size={16} aria-hidden="true"/>{label}</Link>)}</nav>
}
export function SettingsPanel({id,title,children}:{id?:string;title?:string;children:ReactNode}){return <section id={id} className="reference-settings-panel">{title&&<h2>{title}</h2>}{children}</section>}
export function SettingsActionCard({href,label,description,icon:Icon}:{href:string;label:string;description:string;icon:LucideIcon}){return <Link href={href} className="reference-settings-action"><span><Icon size={20} aria-hidden="true"/></span><div><strong>{label}</strong><p>{description}</p></div><ChevronRight size={16} aria-hidden="true"/></Link>}
