import os
from pathlib import Path

from orjson import loads
from pydantic import BaseModel, Field, validator


class Credentials(BaseModel):
    int_account: int | None = Field(default=None)
    username: str
    password: str
    totp_secret_key: str | None = Field(default=None)
    one_time_password: int | None = Field(default=None)

    @validator("totp_secret_key")
    @classmethod
    def one_of(cls, v, values, **kwargs):
        _ = kwargs
        if "one_time_password" in values and values["one_time_password"] is not None:
            raise ValueError(
                "You can't set both `one_time_password` and `totp_secret_key`."
            )
        return v


def build_credentials(location: str = "", override: dict | None = None) -> Credentials:
    if not location and not override:
        raise AttributeError("You need to provide at least on argument.")

    if location:
        location_path = Path(location)
    else:
        location_path = None

    env_content = os.environ.get("DEGIRO_ACCOUNT")

    if env_content:
        config = loads(env_content)
    elif location_path and location_path.exists():
        config = loads(location_path.read_text())
    else:
        config = {}

    if override:
        config.update(override)

    credentials = Credentials.model_validate(obj=config)

    return credentials
