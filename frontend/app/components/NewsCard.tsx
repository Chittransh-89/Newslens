import type { NewsItem } from "../../lib/api";

export function NewsCard({ item }: { item: NewsItem }) {
  const date = item.date === "Unknown date" || item.date === "Trending today" ? item.date : new Date(item.date).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  return <article className="flex min-h-64 flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">
    <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">{item.source}</p>
    <h3 className="text-lg font-bold leading-snug text-slate-900">{item.title}</h3>
    <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-600">{item.description}</p>
    {(item.score !== null || item.reactions !== null || item.comments !== null || item.stars || item.stars_today || item.tags.length > 0) && <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-slate-600">
      {item.score !== null && <span className="rounded-full bg-amber-50 px-2.5 py-1 text-amber-800">Score: {item.score}</span>}
      {item.reactions !== null && <span className="rounded-full bg-rose-50 px-2.5 py-1 text-rose-800">Reactions: {item.reactions}</span>}
      {item.comments !== null && <span className="rounded-full bg-sky-50 px-2.5 py-1 text-sky-800">Comments: {item.comments}</span>}
      {item.stars && <span className="rounded-full bg-amber-50 px-2.5 py-1 text-amber-800">Stars: {item.stars}</span>}
      {item.stars_today && <span className="rounded-full bg-orange-50 px-2.5 py-1 text-orange-800">Today: {item.stars_today}</span>}
      {item.tags.map((tag) => <span key={tag} className="rounded-full bg-slate-100 px-2.5 py-1 text-slate-700">#{tag}</span>)}
    </div>}
    <div className="mt-auto pt-5">
      <p className="mb-4 text-sm font-medium text-slate-500">{date}</p>
      <a href={item.link} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center rounded-lg bg-indigo-600 px-4 text-sm font-semibold text-white transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Read More<span className="ml-2" aria-hidden="true">-&gt;</span></a>
    </div>
  </article>;
}
