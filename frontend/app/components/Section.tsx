import type { NewsItem } from "../../lib/api";
import { NewsCard } from "./NewsCard";

export function Section({ title, items, id }: { title: string; items: NewsItem[]; id: string }) {
  return <section id={id} className="scroll-mt-24 py-7 sm:py-9">
    <h2 className="mb-5 text-2xl font-bold tracking-tight text-slate-900">{title}</h2>
    {items.length ? <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">{items.map((item) => <NewsCard key={item.link} item={item} />)}</div> : <p className="rounded-xl border border-dashed border-slate-300 bg-white p-5 text-sm text-slate-500">No stories are available from this source right now.</p>}
  </section>;
}
