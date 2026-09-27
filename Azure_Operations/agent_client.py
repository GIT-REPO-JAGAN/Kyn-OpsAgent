"""
Thin wrapper around the Azure AI Foundry Python SDK for calling the
Operations Chat agent, following the pattern from the Foundry "Call in
code" sample:

    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient

    project_client = AIProjectClient(endpoint=..., credential=...)
    openai_client = project_client.get_openai_client()
    response = openai_client.responses.create(
        input=[...],
        extra_body={"agent_reference": {"name": ..., "version": ..., "type": "agent_reference"}},
    )

Credentials are resolved by DefaultAzureCredential (az login locally,
managed identity in Azure). No keys are handled by this app directly.
Config (endpoint, agent name/version) comes from Flask's app.config —
see config.py — so it's set once, in one place, for the whole app.
"""

import threading

from flask import current_app


class AgentClientError(Exception):
    """Raised for any failure talking to the Foundry agent."""


class AzureAgentService:
    def __init__(self, endpoint: str, agent_name: str, agent_version: str):
        if not endpoint:
            raise AgentClientError(
                "AZURE_PROJECT_ENDPOINT is not set. Copy .env.example to .env and fill it in."
            )
        self.endpoint = endpoint
        self.agent_name = agent_name
        self.agent_version = agent_version

        self._client_lock = threading.Lock()
        self._openai_client = None

    def _get_openai_client(self):
        """Lazily create the OpenAI-compatible client bound to this project."""
        if self._openai_client is not None:
            return self._openai_client

        with self._client_lock:
            if self._openai_client is not None:
                return self._openai_client
            try:
                from azure.identity import DefaultAzureCredential
                from azure.ai.projects import AIProjectClient
            except ImportError as exc:
                raise AgentClientError(
                    "azure-ai-projects / azure-identity are not installed. "
                    "Run: pip install -r requirements.txt"
                ) from exc

            try:
                project_client = AIProjectClient(
                    endpoint=self.endpoint,
                    credential=DefaultAzureCredential(),
                )
                self._openai_client = project_client.get_openai_client()
            except Exception as exc:  # noqa: BLE001 - surface as a clean API error
                raise AgentClientError(f"Could not connect to Foundry project: {exc}") from exc

        return self._openai_client

    def ping(self) -> bool:
        """Cheap check that credentials + endpoint resolve. Does not call the agent."""
        self._get_openai_client()
        return True

    def send_message(self, message: str, history=None) -> str:
        """
        Send a message to the agent, referencing it by name/version the same
        way the Foundry playground does, and return the text reply.
        """
        client = self._get_openai_client()

        conversation = []
        for turn in history or []:
            role = turn.get("role")
            content = turn.get("content")
            if role in ("user", "assistant") and content:
                conversation.append({"role": role, "content": content})
        conversation.append({"role": "user", "content": message})

        try:
            response = client.responses.create(
                input=conversation,
                extra_body={
                    "agent_reference": {
                        "name": self.agent_name,
                        "version": self.agent_version,
                        "type": "agent_reference",
                    }
                },
            )
        except Exception as exc:  # noqa: BLE001
            raise AgentClientError(f"Agent request failed: {exc}") from exc

        text = getattr(response, "output_text", None)
        if not text:
            raise AgentClientError("Agent returned an empty response.")
        return text


def get_agent_service() -> AzureAgentService:
    """
    Return a Flask-app-scoped AzureAgentService, cached on app.extensions
    so repeated requests reuse one client + credential instead of
    reconnecting every call.
    """
    if "agent_service" not in current_app.extensions:
        cfg = current_app.config
        current_app.extensions["agent_service"] = AzureAgentService(
            endpoint=cfg["AZURE_PROJECT_ENDPOINT"],
            agent_name=cfg["AZURE_AGENT_NAME"],
            agent_version=cfg["AZURE_AGENT_VERSION"],
        )
    return current_app.extensions["agent_service"]
