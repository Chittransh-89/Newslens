from pydantic import AnyHttpUrl, BaseModel, Field


class NewsItem(BaseModel):
    """A source-normalized item with optional source-specific engagement metadata."""

    title: str = Field(min_length=1)
    description: str = "No description available."
    date: str
    link: AnyHttpUrl
    category: str
    source: str
    score: int | None = None
    comments: int | None = None
    reactions: int | None = None
    tags: list[str] = Field(default_factory=list)
    stars: str | None = None
    stars_today: str | None = None


class NewsResponse(BaseModel):
    """All dashboard categories returned by the NewsLens aggregation endpoint."""

    hacker_news: list[NewsItem]
    devto: list[NewsItem]
    layoffs_news: list[NewsItem]
    hiring_news: list[NewsItem]
    funding_news: list[NewsItem]
    ai_jobs: list[NewsItem]
    github_trending: list[NewsItem]
