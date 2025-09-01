from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class FavoriteName(BaseModel):
    name: str


class FavoriteId(BaseModel):
    data: int


class FavoritePosition(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    position: int
    list_id: int


class FavoriteItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    default: bool | None = Field(default=None)
    id: int
    is_default: bool | None = Field(default=None)
    name: str | None = Field(default=None)
    product_ids: list[int] = Field(default_factory=list)


class FavoriteBatch(BaseModel):
    data: list[FavoriteItem] = Field(default_factory=list)
