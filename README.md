# Kyn-OpsAgent

Kyn-OpsAgent is an AI-powered ServiceNow Operations Advisory Workspace built using Flask and Azure AI Foundry. The solution enables operations teams to interact with an AI agent for incident analysis, troubleshooting guidance, operational insights, and knowledge retrieval.

---

## Key Features

- ServiceNow incident analysis
- Azure AI Foundry Agent integration
- Natural language operational assistance
- Knowledge-base grounded responses
- Azure Managed Identity authentication
- Nginx reverse proxy architecture
- Dockerized deployment
- Azure Container Apps hosting

---

## Solution Architecture

```text
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────┐
│    Nginx     │
│ Reverse Proxy│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Flask Backend│
│ Kyn-OpsAgent │
└──────┬───────┘
       │ Managed Identity
       ▼
┌──────────────┐
│ Azure AI     │
│ Foundry Agent│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Knowledge    │
│ Base         │
└──────────────┘


Kyn-OpsAgent
│
├── Application
│   ├── app.py
│   ├── streamlit_app.py
│   └── requirements.txt
│
├── Frontend
│   ├── HTML Templates
│   ├── CSS Styles
│   ├── JavaScript Components
│   └── Static Assets
│
├── Backend
│   ├── Configuration
│   └── API Routes
│
├── Azure Operations
│   └── Azure AI Foundry Integration
│
├── Nginx
│   ├── Reverse Proxy Configuration
│   └── Container Definition
│
└── Deployment
    ├── Dockerfile
    ├── compose.yaml
    └── containerapp.yaml
