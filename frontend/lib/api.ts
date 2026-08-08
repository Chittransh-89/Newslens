export type NewsItem = {
  title: string;
  description: string;
  date: string;
  link: string;
  category: string;
  source: string;
  score: number | null;
  comments: number | null;
  reactions: number | null;
  tags: string[];
  stars: string | null;
  stars_today: string | null;
};
export type NewsResponse = Record<"hacker_news" | "devto" | "layoffs_news" | "hiring_news" | "funding_news" | "ai_jobs" | "github_trending", NewsItem[]>;

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getAllNews(signal?: AbortSignal): Promise<NewsResponse> {
  const response = await fetch(`${API_URL}/news/all`, { signal, cache: "no-store" });
  if (!response.ok) throw new Error("News service is unavailable. Please try again shortly.");
  return response.json() as Promise<NewsResponse>;
}
