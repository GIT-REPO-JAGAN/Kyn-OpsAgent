"""
Operations Chat API — /api/status and /api/chat.

All Azure AI Foundry connection logic lives in Azure_Operations/; these
routes just validate the HTTP request/response and call into it.
"""

import logging

from flask import Blueprint, current_app, jsonify, request

from Azure_Operations.agent_client import AgentClientError, get_agent_service

logger = logging.getLogger("kyn-opsagent.chat_api")

chat_api_bp = Blueprint("chat_api", __name__, url_prefix="/api")


@chat_api_bp.route("/status")
def status():
    """Lightweight connectivity check the frontend polls on load."""
    cfg = current_app.config
    try:
        service = get_agent_service()
        connected = service.ping()
        return jsonify(
            {
                "connected": connected,
                "agent": cfg["AZURE_AGENT_NAME"],
                "knowledge_base": cfg["AZURE_KNOWLEDGE_BASE"],
                "environment": cfg["APP_ENVIRONMENT"],
            }
        )
    except AgentClientError as exc:
        logger.warning("Status check failed: %s", exc)
        return jsonify({"connected": False, "error": str(exc)}), 200


@chat_api_bp.route("/chat", methods=["POST"])
def chat():
    """
    Forward a single user message to the Foundry agent and return its reply.
    Body: { "message": str, "history": [{"role": "user"|"assistant", "content": str}] }
    """
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(message) > 4000:
        return jsonify({"error": "Message exceeds the 4000 character limit."}), 400

    try:
        service = get_agent_service()
        reply = service.send_message(message, history)
        return jsonify({"reply": reply})
    except AgentClientError as exc:
        logger.error("Agent call failed: %s", exc)
        return jsonify({"error": "Failed to fetch", "detail": str(exc)}), 502
