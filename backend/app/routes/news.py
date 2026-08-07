from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.models.schemas import NewsResponse
from app.services.news_service import NewsService

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/all", response_model=NewsResponse, summary="Get the latest technology news")
async def get_all_news(settings: Settings = Depends(get_settings)) -> NewsResponse:
    return await NewsService(settings).get_all_news()
