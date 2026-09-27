"""
Kyn-OpsAgent — ServiceNow Operations AI Advisory Workspace.

Ties the three layers together:
  Frontend/         templates + static assets (what the browser renders)
  Backend/          Flask app wiring, config, and HTTP routes
  Azure_Operations/ Azure AI Foundry agent integration

Run:
    pip install -r requirements.txt
    cp .env.example .env   # fill in your values
    az login               # DefaultAzureCredential needs a signed-in identity
    python app.py
"""

import logging

from flask import Flask
from dotenv import load_dotenv

from Backend.config import Config


def create_app() -> Flask:
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="Frontend/templates",
        static_folder="Frontend/static",
    )
    app.config.from_object(Config)

    logging.basicConfig(level=app.config["LOG_LEVEL"])

    from Backend.routes.pages import pages_bp
    from Backend.routes.chat_api import chat_api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(chat_api_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=app.config["DEBUG"])
