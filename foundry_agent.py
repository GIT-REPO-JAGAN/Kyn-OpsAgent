import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


load_dotenv()


PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
AGENT_NAME = os.getenv("AGENT_NAME")
AGENT_VERSION = os.getenv("AGENT_VERSION")


def validate_configuration():
    """Check that all required environment variables are available."""

    missing_variables = []

    if not PROJECT_ENDPOINT:
        missing_variables.append("PROJECT_ENDPOINT")

    if not AGENT_NAME:
        missing_variables.append("AGENT_NAME")

    if not AGENT_VERSION:
        missing_variables.append("AGENT_VERSION")

    if missing_variables:
        missing_text = ", ".join(missing_variables)

        raise ValueError(
            f"Missing environment variables: {missing_text}. "
            "Create a .env file and provide the required values."
        )


def create_openai_client():
    """Create an authenticated OpenAI client for the Foundry project."""

    validate_configuration()

    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential,
    )

    return project_client.get_openai_client()


def ask_agent(question: str) -> str:
    """
    Submit a question to the published Azure AI Foundry agent.

    The agent uses the knowledge base configured in Azure AI Foundry.
    """

    if not question or not question.strip():
        raise ValueError("The question cannot be empty.")

    openai_client = create_openai_client()

    response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": question.strip(),
            }
        ],
        extra_body={
            "agent_reference": {
                "name": AGENT_NAME,
                "version": AGENT_VERSION,
                "type": "agent_reference",
            }
        },
    )

    if not response.output_text:
        return "The agent completed the request but returned no text."

    return response.output_text
