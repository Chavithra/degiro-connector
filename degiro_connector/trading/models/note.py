from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class NoteItem(BaseModel):
    id: int | None = Field(default=None)
    product_id: int | None = Field(default=None)
    text: str | None = Field(default=None)
    stamp_created: datetime | None = Field(default=None)
    stamp_modified: datetime | None = Field(default=None)


class NoteBatch(BaseModel):
    data: list[NoteItem] = Field(default_factory=list)


class NoteAddRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    product_id: int | None = Field(default=None)
    text: str | None = Field(default=None)

class NoteAddResponse(BaseModel):
    data: NoteItem


class NoteEditRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    note_id: int | None = Field(default=None)
    text: str | None = Field(default=None)


class NoteEditResponse(BaseModel):
    data: NoteItem