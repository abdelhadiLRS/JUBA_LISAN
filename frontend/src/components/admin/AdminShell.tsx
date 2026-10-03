'use client'

import { type ReactNode } from 'react'
import { type LucideIcon } from 'lucide-react'
interface AdminPageHeaderProps{title:string;eyebrow:string;actions?:ReactNode}
export function AdminPageHeader({title,eyebrow,actions}:AdminPageHeaderProps){return <header className="reference-admin-heading"><div><p>{eyebrow}</p><h1>{title}</h1></div>{actions&&<div className="reference-admin-actions">{actions}</div>}<style>{`
  .juba-app-shell .reference-admin-heading{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;min-height:100px;padding-block:16px;}
  .juba-app-shell .reference-admin-heading p{font-size:11px;color:var(--juba-green-dark);margin:0 0 6px;}
  .juba-app-shell .reference-admin-heading h1{font-size:28px;font-weight:650;line-height:1.3;margin:0;}
  .juba-app-shell .reference-admin-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
  .juba-app-shell .reference-admin-panel{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
  .juba-app-shell .reference-admin-panel-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:16px;border-block-end:1px solid var(--juba-border);}
  .juba-app-shell .reference-admin-panel-head h2{font-size:14px;font-weight:650;margin:0;}
  .juba-app-shell .reference-admin-panel-head>div{margin-inline-start:auto;font-size:12px;color:var(--juba-muted);}
  .juba-app-shell .reference-admin-metric{display:flex;align-items:center;gap:12px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);min-width:0;}
  .juba-app-shell .reference-admin-metric>div{flex:1;min-width:0;}
  .juba-app-shell .reference-admin-metric p{margin:0 0 8px;font-size:11px;color:var(--juba-muted);}
  .juba-app-shell .reference-admin-metric strong{display:block;font-size:22px;font-weight:650;font-variant-numeric:tabular-nums;overflow-wrap:anywhere;}
  .juba-app-shell .reference-admin-metric>span{display:grid;place-items:center;width:36px;height:36px;flex:none;border-radius:5px;background:var(--juba-green-soft);color:var(--juba-green-dark);}
  .juba-app-shell .reference-admin-badge{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--juba-border);border-radius:4px;padding:3px 8px;color:var(--juba-muted);font-size:11px;font-weight:600;}
  .juba-app-shell .reference-admin-badge[data-tone="info"]{color:var(--duo-blue);}
  .juba-app-shell .reference-admin-badge[data-tone="success"]{color:var(--juba-green-dark);background:var(--juba-green-soft);}
  .juba-app-shell .reference-admin-badge[data-tone="warning"]{color:oklch(45% .09 75);background:oklch(97% .03 90);}
  .juba-app-shell .reference-admin-badge[data-tone="danger"]{color:var(--duo-red);}
  @media(max-width:640px){.juba-app-shell .reference-admin-heading h1{font-size:24px;}}
`}</style></header>}
export function AdminPanel({title,meta,children}:{title?:string;meta?:ReactNode;children:ReactNode}){return <section className="reference-admin-panel">{(title||meta)&&<header className="reference-admin-panel-head">{title&&<h2>{title}</h2>}{meta&&<div>{meta}</div>}</header>}{children}</section>}
export function AdminMetric({label,value,icon:Icon}:{label:string;value:ReactNode;icon:LucideIcon}){return <div className="reference-admin-metric"><div><p>{label}</p><strong>{value}</strong></div><span><Icon size={20} aria-hidden="true"/></span></div>}
export function AdminBadge({children,tone='neutral'}:{children:ReactNode;tone?:'neutral'|'info'|'success'|'warning'|'danger'}){return <span className="reference-admin-badge" data-tone={tone}>{children}</span>}
