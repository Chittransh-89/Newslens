import asyncio
from collections.abc import Awaitable
from datetime import datetime, timezone
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup

from app.config import Settings
from app.models.schemas import NewsItem, NewsResponse
from app.utils.helpers import clean_text, format_date


class NewsService:
    """Collect and normalize headlines from the public sources used by NewsLens."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_all_news(self) -> NewsResponse:
        async with httpx.AsyncClient(
            timeout=self.settings.request_timeout_seconds,
            headers={"User-Agent": self.settings.user_agent},
            follow_redirects=True,
        ) as client:
            results = await asyncio.gather(
                self._safe_fetch(self._fetch_hacker_news(client)),
                self._safe_fetch(self._fetch_devto(client)),
                self._safe_fetch(self._fetch_bing(client, "tech company layoffs", 4)),
                self._safe_fetch(self._fetch_bing(client, "technology company hiring", 4)),
                self._safe_fetch(self._fetch_bing(client, "startup funding raised", 4)),
                self._safe_fetch(self._fetch_bing(client, "AI jobs demand", 4)),
                self._safe_fetch(self._fetch_github_trending(client)),
            )

        return NewsResponse(
            hacker_news=results[0], devto=results[1], layoffs_news=results[2],
            hiring_news=results[3], funding_news=results[4], ai_jobs=results[5],
            github_trending=results[6],
        )

    async def _safe_fetch(self, task: Awaitable[list[NewsItem]]) -> list[NewsItem]:
        try:
            return await task
        except (httpx.HTTPError, ValueError, AttributeError):
            # A source failing should not prevent the dashboard from serving the others.
            return []

    async def _fetch_hacker_news(self, client: httpx.AsyncClient) -> list[NewsItem]:
        ids_response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        ids_response.raise_for_status()
        story_ids = ids_response.json()[:5]
        responses = await asyncio.gather(*[
            client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json") for story_id in story_ids
        ])
        stories = []
        for response in responses:
            response.raise_for_status()
            story = response.json()
            if not story or not story.get("title"):
                continue
            score = story.get("score", 0)
            comments = story.get("descendants", 0)
            stories.append(NewsItem(
                title=clean_text(story["title"], 180),
                description=f"{score} points | {comments} comments on Hacker News.",
                date=datetime.fromtimestamp(story.get("time", 0), tz=timezone.utc).isoformat(),
                link=story.get("url") or f"https://news.ycombinator.com/item?id={story['id']}",
            ))
        return stories

    async def _fetch_devto(self, client: httpx.AsyncClient) -> list[NewsItem]:
        response = await client.get("https://dev.to/api/articles", params={"top": 7, "per_page": 5})
        response.raise_for_status()
        return [NewsItem(
            title=clean_text(article.get("title"), 180),
            description=clean_text(article.get("description") or article.get("tag_list") and f"Tags: {', '.join(article['tag_list'][:3])}"),
            date=format_date(article.get("published_at")),
            link=article["url"],
        ) for article in response.json() if article.get("title") and article.get("url")]

    async def _fetch_bing(self, client: httpx.AsyncClient, query: str, limit: int) -> list[NewsItem]:
        url = f"https://www.bing.com/news/search?{urlencode({'q': query, 'format': 'rss'})}"
        response = await client.get(url)
        response.raise_for_status()
        feed = BeautifulSoup(response.text, "xml")
        articles: list[NewsItem] = []
        for item in feed.find_all("item")[:limit]:
            title, link = item.find("title"), item.find("link")
            if not title or not link:
                continue
            description = item.find("description")
            published = item.find("pubDate")
            articles.append(NewsItem(
                title=clean_text(title.get_text(), 180),
                description=clean_text(description.get_text() if description else None),
                date=format_date(published.get_text() if published else None),
                link=link.get_text(strip=True),
            ))
        return articles

    async def _fetch_github_trending(self, client: httpx.AsyncClient) -> list[NewsItem]:
        response = await client.get("https://github.com/trending")
        response.raise_for_status()
        page = BeautifulSoup(response.text, "html.parser")
        articles: list[NewsItem] = []
        for repo in page.select("article.Box-row")[:5]:
            anchor = repo.select_one("h2 a")
            if not anchor or not anchor.get("href"):
                continue
            name = clean_text(anchor.get_text(" "), 100).replace(" / ", "/")
            description = repo.select_one("p")
            stars_today = repo.select_one("span.d-inline-block.float-sm-right")
            text = clean_text(description.get_text(" ") if description else None)
            if stars_today:
                text = f"{text} | {clean_text(stars_today.get_text(), 80)}"
            articles.append(NewsItem(
                title=name,
                description=text,
                date="Trending today",
                link=f"https://github.com{anchor['href']}",
            ))
        return articles
