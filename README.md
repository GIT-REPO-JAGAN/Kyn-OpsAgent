# Kyn-OpsAgent

Kyn-OpsAgent is a ServiceNow Operations AI Advisory Workspace built with Flask and Azure AI Foundry.

The application provides:

- Natural language operations assistance
- Azure AI Foundry Agent integration
- ServiceNow incident analysis
- Azure Managed Identity authentication
- Nginx reverse proxy frontend
- Azure Container Apps deployment
- Streamlit demo launcher

The solution is containerized and deployed using Azure Container Apps with a multi-container architecture.

Kyn-OpsAgent/
│
├── app.py                       # Flask application entry point
├── streamlit_app.py             # Streamlit launcher/demo UI
├── requirements.txt
├── Dockerfile                   # Backend container image
├── compose.yaml                 # Local multi-container deployment
├── containerapp.yaml            # Azure Container Apps definition
├── README.md
├── .env.example
│
├── Frontend/
│   ├── templates/
│   │   ├── shell.html
│   │   ├── chat_panel.html
│   │   └── context_panel.html
│   │
│   └── static/
│       ├── css/
│       │   ├── shell.css
│       │   └── operations_chat.css
│       │
│       ├── js/
│       │   ├── shell.js
│       │   └── operations_chat.js
│       │
│       └── assets/
│
├── Backend/
│   ├── config.py
│   └── routes/
│       ├── pages.py
│       └── chat_api.py
│
├── Azure_Operations/
│   └── agent_client.py
│
└── nginx/
    ├── Dockerfile
    └── nginx.conf


## Architecture

```text
Browser
    │
    ▼
Nginx Reverse Proxy
    │
    ▼
Flask API
    │
    ▼
Azure AI Foundry Agent
    │
    ▼
Grounding / Knowledge Base
