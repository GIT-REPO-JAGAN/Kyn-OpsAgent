from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    url_for,
)


pages_bp = Blueprint(
    "pages",
    __name__,
)


@pages_bp.route("/")
def index():
    return redirect(
        url_for("pages.login"),
    )


@pages_bp.route("/login")
def login():
    return render_template(
        "login.html",
    )


@pages_bp.route("/workspace")
def workspace():
    return render_template(
        "shell.html",
        agent_name=current_app.config[
            "AZURE_AGENT_NAME"
        ],
        knowledge_base=current_app.config[
            "AZURE_KNOWLEDGE_BASE"
        ],
        environment=current_app.config[
            "APP_ENVIRONMENT"
        ],
    )
