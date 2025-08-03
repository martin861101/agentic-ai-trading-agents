from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/agentic_trading"
    
    # Redis
    redis_url: str = "redis://localhost:6380"
    
    # API Keys - UPDATE THESE!
    travily_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Security
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Agent ports
    chartanalyst_port: int = 8001
    riskmanager_port: int = 8002
    marketsentinel_port: int = 8003
    macroforecaster_port: int = 8004
    tacticbot_port: int = 8005
    platformpilot_port: int = 8006

    # Orchestrator
    orchestrator_port: int = 8007

    class Config:
        env_file = ".env"

settings = Settings()
