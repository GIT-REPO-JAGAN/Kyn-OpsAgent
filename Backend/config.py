"""Application configuration, sourced from environment variables (.env)."""

import os


class Config:
    # Azure AI Foundry connection
    AZURE_PROJECT_ENDPOINT = os.getenv("AZURE_PROJECT_ENDPOINT", "")
    AZURE_AGENT_NAME = os.getenv("AZURE_AGENT_NAME", "jk-service-now-opsagent")
    AZURE_AGENT_VERSION = os.getenv("AZURE_AGENT_VERSION", "3")
    AZURE_KNOWLEDGE_BASE = os.getenv("AZURE_KNOWLEDGE_BASE", "jk-service-now-kb")

    # Display / runtime
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "Development")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
