from pydantic import AnyHttpUrl, BaseModel, Field


class NewsItem(BaseModel):
    title: str = Field(min_length=1)
    description: str = "No description available."
    date: str
    link: AnyHttpUrl


class NewsResponse(BaseModel):
    hacker_news: list[NewsItem]
    devto: list[NewsItem]
    layoffs_news: list[NewsItem]
    hiring_news: list[NewsItem]
    funding_news: list[NewsItem]
    ai_jobs: list[NewsItem]
    github_trending: list[NewsItem]
