from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FundAPP Backend API - Fundación Biosferas"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "fundapp-secret-jwt-key-for-fundacion-biosferas-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas

    # Supabase Configuration
    SUPABASE_URL: Optional[str] = "https://fpuwuweqjcqycifjifsx.supabase.co"
    SUPABASE_KEY: Optional[str] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
