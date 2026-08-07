"use client";

import { useState } from "react";

const links = [["Top stories", "hacker-news"], ["Jobs", "hiring"], ["Funding", "funding"], ["Trending", "github"]];

export function Navbar() {
  const [open, setOpen] = useState(false);
  return <header className="sticky top-0 z-10 border-b border-slate-200 bg-slate-50/95 backdrop-blur"><nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"><div className="flex min-h-16 items-center justify-between"><a className="text-lg font-extrabold tracking-tight text-slate-900" href="#top">News<span className="text-indigo-600">Lens</span></a><button onClick={() => setOpen(!open)} className="min-h-11 rounded-lg px-3 text-sm font-semibold text-slate-700 md:hidden" aria-expanded={open} aria-label="Toggle navigation">Menu</button><div className="hidden gap-6 md:flex">{links.map(([label, id]) => <a key={id} className="text-sm font-medium text-slate-600 hover:text-indigo-600" href={`#${id}`}>{label}</a>)}</div></div>{open && <div className="border-t border-slate-200 py-3 md:hidden">{links.map(([label, id]) => <a onClick={() => setOpen(false)} key={id} className="block rounded-lg px-3 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100" href={`#${id}`}>{label}</a>)}</div>}</nav></header>;
}
