from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class LoginSuccess(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    is_pass_code_enabled: bool | None = Field(default=None)
    locale: str | None = Field(default=None)
    redirect_url: str | None = Field(default=None)
    session_id: str
    status: int | None = Field(default=None)
    status_text: str | None = Field(default=None)


class LoginError(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    login_failures: int | None = Field(default=None)
    error: str | None = Field(default=None)
    path: str | None = Field(default=None)
    status: int
    status_text: str | None = Field(default=None)
    timestamp: date | None = Field(default=None)


class Login(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    username: str
    password: str
    is_pass_code_reset: bool = Field(default=False)
    is_redirect_to_mobile: bool = Field(default=False)
    query_tarams: dict = Field(default_factory=dict)
    one_time_password: str | None = Field(default=None)
