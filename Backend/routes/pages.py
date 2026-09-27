"""Page routes — render the Frontend templates."""

from flask import Blueprint, current_app, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def shell():
    """Render the app shell (Frontend/templates/shell.html), which includes
    the chat panel and context panel partials."""
    cfg = current_app.config
    return render_template(
        "shell.html",
        agent_name=cfg["AZURE_AGENT_NAME"],
        knowledge_base=cfg["AZURE_KNOWLEDGE_BASE"],
        environment_label=cfg["APP_ENVIRONMENT"],
    )
