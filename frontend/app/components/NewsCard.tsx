import type { NewsItem } from "../../lib/api";

export function NewsCard({ item }: { item: NewsItem }) {
  const date = item.date === "Unknown date" || item.date === "Trending today" ? item.date : new Date(item.date).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  return <article className="flex min-h-64 flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">
    <h3 className="text-lg font-bold leading-snug text-slate-900">{item.title}</h3>
    <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-600">{item.description}</p>
    <div className="mt-auto pt-5">
      <p className="mb-4 text-sm font-medium text-slate-500">{date}</p>
      <a href={item.link} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center rounded-lg bg-indigo-600 px-4 text-sm font-semibold text-white transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Read More<span className="ml-2" aria-hidden="true">-&gt;</span></a>
    </div>
  </article>;
}
