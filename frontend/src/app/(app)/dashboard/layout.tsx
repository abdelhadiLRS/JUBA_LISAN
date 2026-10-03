import type { ReactNode } from 'react'
import ReferenceFeatures from './ReferenceFeatures'

export default function DashboardLayout({children}:{children:ReactNode}){
  return <div className="reference-dashboard-route">{children}<ReferenceFeatures/></div>
}
