from pydantic import Field, BaseModel, validator, root_validator
from datetime import date, time


class HealthcheckSchema(BaseModel):
    aes_available: bool


class NewsCreatedSchema(BaseModel):
    title: str
    description: str
    date: str
    time: str

    @validator("date", pre=True, always=True)
    def validate_date(cls, value):
        try:
            day, month, year = map(int, value.split("."))
            date(year, month, day)
            return value
        except ValueError:
            raise ValueError("дата не в нужном формате")

    @validator("time", pre=True, always=True)
    def validate_time(cls, value):
        try:
            hour, minute = map(int, value.split(":"))
            time(hour, minute)
            return value
        except ValueError:
            raise ValueError("время не в нужном формате")


class NewsSchema(NewsCreatedSchema):
    id: str

    @root_validator(pre=True)
    def validator(cls, values):
        values["_source"] |= {"id": values["_id"]}
        values = values["_source"]

        return values


class NewsHits(BaseModel):
    news: list[NewsSchema]

    @root_validator(pre=True)
    def validator(cls, values):
        values["news"] = values["hits"]["hits"]
        return values
