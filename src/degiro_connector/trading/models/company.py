from pydantic import BaseModel


class CompanyRatios(BaseModel):
    data: dict


class CompanyProfile(BaseModel):
    data: dict
