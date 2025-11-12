from pydantic import BaseModel
from pydantic_settings import BaseSettings

class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix:str = "/api"


class Settings(BaseSettings):
    title: str = "FastAPI Wallet"
    version: str = "0.1.0"
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

settings = Settings()