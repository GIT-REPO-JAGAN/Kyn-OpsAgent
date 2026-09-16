# Kyn-OpsAgent

Kyn-OpsAgent is an IT Operations assistant built using Microsoft Foundry.

The application searches a knowledge base containing synthetic ServiceNow-style
incident records and provides grounded incident summaries, probable root causes,
recommended resolutions, related incidents, and references.

## Architecture

```text
Streamlit Chat UI
        |
        v
Azure AI Foundry Agent
        |
        v
Foundry IQ Knowledge Base
        |
        v
Azure AI Search
        |
        v
ServiceNow Incident Data
