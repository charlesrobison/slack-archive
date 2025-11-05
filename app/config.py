from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

class Settings(BaseModel):
    # Slack
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str

    # Database connection details
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "slack_archive"
    DB_USER: str = "slack"
    DB_PASSWORD: str = "slack"
    DB_SCHEMA: str = "public"

    # Environment & logging
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    @property
    def database_url(self) -> str:
        """Return a SQLAlchemy connection URL."""
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

# Instantiate settings object
settings = Settings(
    SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN", ""),
    SLACK_APP_TOKEN=os.getenv("SLACK_APP_TOKEN", ""),
    DB_HOST=os.getenv("DB_HOST", "localhost"),
    DB_PORT=int(os.getenv("DB_PORT", 5432)),
    DB_NAME=os.getenv("DB_NAME", "slack_archive"),
    DB_USER=os.getenv("DB_USER", "slack"),
    DB_PASSWORD=os.getenv("DB_PASSWORD", "slack"),
    DB_SCHEMA=os.getenv("DB_SCHEMA", "public"),
    ENV=os.getenv("ENV", "development"),
    LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
)
