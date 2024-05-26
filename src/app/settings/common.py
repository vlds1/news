from pydantic import AnyHttpUrl, BaseSettings, validator


class UvicornSettings(BaseSettings):
    class Config:
        env_prefix = "UVICORN_"
        env_file = ".env"

    HOST: str = "127.0.0.1"
    PORT: int = 8000


class ElasticSettings(BaseSettings):
    class Config:
        env_prefix = "ELASTIC_"
        env_file = ".env"

    INDEX: str
    HOSTS: list[str] = ["127.0.0.1"]
    USER: str = "elastic"
    PASSWORD: str = "changeme"
    PORT: str = 9200
    LIST_DSN: list[AnyHttpUrl] = []

    @validator("LIST_DSN")
    def build_list_dsn(cls, value, values, **kwargs):
        if value:
            return value
        list_dsn = []
        for host in values["HOSTS"]:
            dsn = (
                f'http://{values["USER"]}:{values["PASSWORD"]}@{host}:{values["PORT"]}/'
            )
            list_dsn.append(dsn)
        return list_dsn


class Settings(BaseSettings):
    uvicorn: UvicornSettings = UvicornSettings()
    elastic: ElasticSettings = ElasticSettings()
