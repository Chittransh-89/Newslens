"use client";

import { useEffect, useState } from "react";
import { getAllNews, type NewsResponse } from "../lib/api";
import { Navbar } from "./components/Navbar";
import { Section } from "./components/Section";

const sections: Array<[keyof NewsResponse, string, string]> = [["hacker_news", "Hacker News", "hacker-news"], ["devto", "Dev.to", "devto"], ["layoffs_news", "Layoffs", "layoffs"], ["hiring_news", "Hiring", "hiring"], ["funding_news", "Startup Funding", "funding"], ["ai_jobs", "AI Jobs", "ai-jobs"], ["github_trending", "GitHub Trending", "github"]];

export default function Home() {
  const [news, setNews] = useState<NewsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const loadNews = async () => { setLoading(true); setError(null); try { setNews(await getAllNews()); } catch (err) { setError(err instanceof Error ? err.message : "Unable to load the news."); } finally { setLoading(false); } };
  useEffect(() => { void loadNews(); }, []);
  return <><Navbar /><main id="top" className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8"><div className="py-10 sm:py-14"><p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">Daily signal, less noise</p><h1 className="mt-3 max-w-2xl text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">Technology news, in focus.</h1><p className="mt-4 max-w-xl text-base leading-7 text-slate-600 sm:text-lg">The latest developer stories, market moves, and projects worth watching.</p></div>{loading && <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">{Array.from({ length: 6 }, (_, i) => <div key={i} className="h-64 animate-pulse rounded-2xl bg-slate-200" />)}</div>}{error && <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800"><p className="font-semibold">Could not load the news</p><p className="mt-1 text-sm">{error}</p><button onClick={() => void loadNews()} className="mt-4 min-h-11 rounded-lg bg-red-700 px-4 text-sm font-semibold text-white hover:bg-red-800">Try again</button></div>}{news && !loading && sections.map(([key, title, id]) => <Section key={key} title={title} id={id} items={news[key]} />)}</main></>;
}
