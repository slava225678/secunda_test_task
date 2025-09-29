from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки PostgreSQL
    API_KEY: str = "supersecretkey"
    postgres_user: str = 'admin'
    postgres_password: str = 'secret'
    postgres_db: str = 'secunda_project'
    postgres_host: str = 'db'
    postgres_port: int = 5432

    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
