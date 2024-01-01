from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class FavouriteName(BaseModel):
    name: str

class FavouriteId(BaseModel):
    data: int

class FavouritePosition(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    position: int
    list_id: int


class FavouriteItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    default: int | None = Field(default=None)
    id: int
    is_default: bool | None = Field(default=None)
    name: str | None = Field(default=None)


class FavouriteBatch(BaseModel):
    data: list[FavouriteItem] = Field(default_factory=list)
