"""
Azure_Operations: everything that talks to Azure AI Foundry.

Nothing outside this package should import azure-identity or
azure-ai-projects directly — Backend/routes/chat_api.py calls in through
get_agent_service() only.
"""
