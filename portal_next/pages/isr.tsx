import React from 'react'
export async function getStaticProps() {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://media1.local:8000'
  const res = await fetch(base + '/api/portal?limit=20')
  const data = await res.json()
  return { props: { data, base }, revalidate: 30 }
}
export default function ISR({ data, base }: any) {
  return (<main style={{maxWidth:960,margin:'20px auto',padding:'0 16px'}}>
    <h1>Portal (ISR, revalidate=30s)</h1>
    <ul>{data.items.map((x:any)=>(<li key={x.id}><a href={x.url} target="_blank">{x.title}</a> <small>({x.site})</small></li>))}</ul>
  </main>)
}
