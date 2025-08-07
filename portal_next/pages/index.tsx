import React from 'react'
export async function getServerSideProps() {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://media1.local:8000'
  const res = await fetch(base + '/api/portal?limit=20')
  const data = await res.json()
  return { props: { data, base } }
}
export default function Home({ data, base }: any) {
  return (<main style={{maxWidth:960,margin:'20px auto',padding:'0 16px'}}>
    <h1>Portal (SSR)</h1>
    <ul>{data.items.map((x:any)=>(<li key={x.id}><a href={x.url} target="_blank">{x.title}</a> <small>({x.site})</small></li>))}</ul>
  </main>)
}
