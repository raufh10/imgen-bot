from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
  )

  # Bot
  bot_name: str = "imgen-bot"
  telegram_bot_token: str
  webhook_url: str
  webhook_secret: str
  chat_id: int

  # OpenAI
  openai_api_key: str
  openai_model: str
  openai_img_model: str

  # Server
  host: str = "0.0.0.0"
  port: int = 8000
  debug: bool = False

  # Environment
  environment: str

  @property
  def is_production(self) -> bool:
    return self.environment == "production"

settings = Settings()
