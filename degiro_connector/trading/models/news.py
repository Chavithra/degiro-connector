from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class NewsRequest(BaseModel):
    isin: str
    limit: int = Field(default=10)
    offset: int = Field(default=0)
    languages: str


class NewsItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    brief: str | None = Field(default=None)
    category: str | None = Field(default=None)
    content: str
    date: datetime
    html_content: bool
    id: str
    isins: list[str]
    language: str
    last_updated: datetime | None = Field(default=None)
    picture_url: str | None = Field(default=None)
    provider: str
    source: str
    title: str


class NewsBatch(BaseModel):
    items: list[NewsItem] = Field(default_factory=list)
    offset: int
    total: int


class BatchWrapper(BaseModel):
    data: NewsBatch


class PreviewRequest(BaseModel):
    limit: int = Field(default=20)
    category: str | None = Field(default=None)


class TopNewsPreview(BaseModel):
    offset: int
    items: list[dict]
    total: int


class PreviewWrapper(BaseModel):
    data: TopNewsPreview


class LatestRequest(BaseModel):
    languages: str
    limit: int
    offset: int


class LatestNews(BaseModel):
    offset: int
    items: list[dict]
    total: int


class LatestWrapper(BaseModel):
    data: LatestNews
