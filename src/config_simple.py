"""
Simplified Configuration for Local Development
Configuration that works without Docker, PostgreSQL, Redis, and Kafka
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Application
    app_name: str = Field(default="TaskFlow AI Customer Success Agent")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO")

    # API
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_workers: int = Field(default=1)  # Single worker for local development

    # Database - Using SQLite for simplified version
    database_url: str = Field(
        default="sqlite+aiosqlite:///./taskflow_crm.db"
    )
    database_pool_size: int = Field(default=5)
    database_max_overflow: int = Field(default=2)

    # Redis - Optional in simplified version
    redis_url: str = Field(default="")  # Empty string means Redis is disabled
    redis_max_connections: int = Field(default=5)

    # Kafka - Optional in simplified version
    kafka_bootstrap_servers: str = Field(default="")  # Empty string means Kafka is disabled
    kafka_topic_inquiries: str = Field(default="customer-inquiries")
    kafka_topic_responses: str = Field(default="customer-responses")
    kafka_consumer_group: str = Field(default="agent-processors")

    # OpenAI (or Groq - they use same interface)
    openai_api_key: str = Field(default="")  # You'll need to set this in your .env
    openai_model: str = Field(default="llama-3.1-8b-instant")  # Updated Groq LLaMA model
    openai_max_tokens: int = Field(default=1000)
    openai_temperature: float = Field(default=0.7)

    # Groq-specific settings
    use_groq: bool = Field(default=True)  # Whether to use Groq instead of OpenAI
    groq_base_url: str = Field(default="https://api.groq.com/openai/v1")

    # Gmail API
    gmail_credentials_file: str = Field(default="credentials/gmail-credentials.json")
    gmail_token_file: str = Field(default="credentials/gmail-token.json")
    gmail_support_email: str = Field(default="support@taskflow.com")
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")
    google_project_id: str = Field(default="")
    pubsub_topic_name: str = Field(default="")
    pubsub_subscription_name: str = Field(default="")

    # Twilio WhatsApp
    twilio_account_sid: str = Field(default="")
    twilio_auth_token: str = Field(default="")
    twilio_whatsapp_number: str = Field(default="")
    twilio_webhook_url: str = Field(default="")

    # Security
    secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_hours: int = Field(default=24)

    # Performance
    max_concurrent_requests: int = Field(default=100)
    request_timeout_seconds: int = Field(default=30)
    rate_limit_per_minute: int = Field(default=60)

    # Monitoring
    prometheus_port: int = Field(default=9090)
    enable_metrics: bool = Field(default=False)  # Disable metrics for simplified version

    # Feature Flags
    enable_sentiment_analysis: bool = Field(default=True)
    enable_auto_escalation: bool = Field(default=True)
    enable_daily_reports: bool = Field(default=True)
    enable_email_polling: bool = Field(default=True)

    # Email Polling Configuration
    poll_interval_seconds: int = Field(default=60)

    @validator("app_env")
    def validate_env(cls, v):
        """Validate environment"""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"app_env must be one of {allowed}")
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.app_env == "development"

    @property
    def use_redis(self) -> bool:
        """Check if Redis should be used"""
        return bool(self.redis_url)

    @property
    def use_kafka(self) -> bool:
        """Check if Kafka should be used"""
        return bool(self.kafka_bootstrap_servers)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings