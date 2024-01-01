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
