# Kyn-OpsAgent

ServiceNow Operations AI Advisory Workspace — a Flask + vanilla JS UI that
talks to an Azure AI Foundry agent (`jk-service-now-opsagent`) the same way
the Foundry Playground does.

## Project structure

Organized by **operation**: Frontend, Backend, and Azure Operations each
live in their own top-level folder, so you always know where to look.

```
Kyn-OpsAgent/
├── app.py                              # Entrypoint — wires Frontend + Backend + Azure_Operations together
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── Frontend/                            # Everything the browser renders
│   ├── templates/
│   │   ├── shell.html                   #   Page layout: sidebar, topbar; includes the two partials below
│   │   ├── chat_panel.html              #   Messages, input, quick-action chips
│   │   └── context_panel.html           #   Agent Context panel (connection, grounding, safety)
│   └── static/
│       ├── css/
│       │   ├── shell.css                #   Design tokens, layout grid, sidebar, topbar
│       │   └── operations_chat.css      #   Chat panel, messages, input, context panel styling
│       ├── js/
│       │   ├── shell.js                 #   Connection-status polling, "New session" button
│       │   └── operations_chat.js       #   Send message, quick actions, context-panel sync
│       └── assets/                      #   Drop LOGO.png here (see below)
│
├── Backend/                             # Flask app wiring, config, and HTTP routes
│   ├── config.py                        #   All env-driven settings, in one place
│   └── routes/
│       ├── pages.py                     #   GET /  → renders the shell
│       └── chat_api.py                  #   POST /api/chat, GET /api/status
│
└── Azure_Operations/                    # All Azure AI Foundry integration logic
    └── agent_client.py                  #   AIProjectClient wrapper — the only place that
                                          #   imports azure-identity / azure-ai-projects
```

**Where to look for what:**

| You want to change... | Go to... |
|---|---|
| Layout, colors, spacing | `Frontend/static/css/` |
| Chat behavior in the browser (sending, rendering messages) | `Frontend/static/js/operations_chat.js` |
| Sidebar/topbar behavior (status dot, new session) | `Frontend/static/js/shell.js` |
| Page markup | `Frontend/templates/` |
| What URL does what | `Backend/routes/` |
| Which agent/endpoint/env vars are used | `Backend/config.py` and `.env` |
| How the agent is actually called | `Azure_Operations/agent_client.py` |

`Backend/routes/chat_api.py` is the seam between the layers: it validates
the HTTP request, calls into `Azure_Operations.agent_client`, and returns
JSON. Nothing in `Frontend/` talks to Azure directly, and nothing outside
`Azure_Operations/` imports the Azure SDKs.

## How it works

- **Frontend**: `shell.html` is the page shell; it includes `chat_panel.html`
  and `context_panel.html`. Pure HTML/CSS/JS, no build step, no framework.
- **Backend**: `app.py` creates the Flask app pointed at `Frontend/templates`
  and `Frontend/static`, then registers two route blueprints:
  - `pages.py` → `GET /` renders the shell.
  - `chat_api.py` → `GET /api/status` (connectivity check) and
    `POST /api/chat` (forwards a message + short history to the agent).
- **Azure Operations**: `agent_client.py` calls the Foundry agent via
  `AIProjectClient.get_openai_client().responses.create(...)`, referencing
  it by `name`/`version` exactly like the "Call in code" sample from the
  Playground, and returns `output_text`. Credentials are never handled
  directly — `DefaultAzureCredential` resolves them (your `az login`
  session locally, or a managed identity when deployed to Azure).

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set AZURE_PROJECT_ENDPOINT to your project's endpoint
#   e.g. https://<project>.services.ai.azure.com/api/projects/<project-name>

az login                          # DefaultAzureCredential needs a signed-in identity

python app.py                     # serves on http://localhost:5000
```

## Running in GitHub Codespaces

1. Push this folder to the `Kyn-OpsAgent` repo (or open the existing repo in
   a Codespace).
2. In the Codespace terminal:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env   # fill in AZURE_PROJECT_ENDPOINT
   az login --use-device-code
   python app.py
   ```
3. Codespaces will prompt to forward port `5000` — open it in the browser
   (set port visibility to Private/Public as needed).

## Adding the Kyndryl logo

The sidebar currently renders the `kyndryl.` wordmark in CSS (no image
asset, so there's nothing to license or track in source control). To use
your own `LOGO.png` instead:

1. Drop the file at `Frontend/static/assets/LOGO.png`.
2. In `Frontend/templates/shell.html`, replace the `.brand-wordmark` div
   with:
   ```html
   <img src="{{ url_for('static', filename='assets/LOGO.png') }}" alt="Kyndryl" class="brand-logo">
   ```
   `.brand-logo` is already styled in `Frontend/static/css/shell.css`.

## Configuration reference (`.env`)

| Variable | Purpose |
|---|---|
| `AZURE_PROJECT_ENDPOINT` | Foundry project endpoint (required) |
| `AZURE_AGENT_NAME` | Agent name reference, default `jk-service-now-opsagent` |
| `AZURE_AGENT_VERSION` | Agent version reference, default `3` |
| `AZURE_KNOWLEDGE_BASE` | Display-only label shown in the context panel |
| `APP_ENVIRONMENT` | Display-only label ("Development" / "Production") |
| `PORT` | Flask port, default `5000` |
| `FLASK_DEBUG` | `true`/`false` |

## Notes on scope

- This ships the minimum needed to run: no ORM, no build tooling, no auth
  layer beyond Azure identity — add those as your deployment needs grow.
- The UI is read-only/advisory by design (matches the reference "No write
  operations are performed from this interface" policy) — it never calls
  ServiceNow directly; all grounding goes through the Foundry agent's own
  connected knowledge base.
- The other sidebar items (Active Incidents, Problem Analysis, Knowledge,
  Conversation History, Insights) are shown as disabled placeholders in the
  nav. To build one out: add its markup to `Frontend/templates/`, its route
  to `Backend/routes/`, and any Azure calls it needs to `Azure_Operations/`.
