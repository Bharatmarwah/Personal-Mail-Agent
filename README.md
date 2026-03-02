# Personal Mail Agent

**An AI-powered email automation system using Google Gemini and Spring Boot**

A microservices application that combines a Python FastAPI agent with a Spring Boot email service. Users send a natural language prompt describing what they want to email about, and the Gemini AI composes a professional email and sends it via Gmail SMTP.

**Author**: [bharatmarwah](https://github.com/bharatmarwah)  
**Version**: 2.0.0

---

## 📊 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   FastAPI Agent Service                      │
│              (Python 3.10+ / Gemini 2.5-Flash)              │
│         • AI Email Composition  • Word Count Control         │
│                    Port 8000                                 │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP POST (JSON)
                     ▼
┌──────────────────────────────────────────────────────────────┐
│              Spring Boot Email Service                       │
│             (Java 21 / Spring Boot 3.5.11)                  │
│         • SMTP Gateway  • Email Delivery                     │
│                    Port 8080                                 │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
              Gmail SMTP Server
```

## ✨ Features

- **🤖 AI Email Writing** — Gemini 2.5-Flash composes professional emails from a simple prompt
- **📏 Word Count Control** — Specify a minimum word count; the agent regenerates if too short
- **📧 Gmail SMTP Delivery** — Emails sent via Spring Boot mail service through Gmail
- **⚡ Async Architecture** — Non-blocking HTTP calls between services using `httpx`
- **🐳 Docker Compose** — One-command deployment with health checks and networking
- **📚 Swagger Docs** — Interactive API docs at `/docs` (FastAPI) and `/swagger-ui.html` (Spring Boot)

## 📋 Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | FastAPI agent runtime |
| **Java** | 21+ | Spring Boot service runtime |
| **Maven** | 3.8+ | Java build tool |
| **Docker** | 20.10+ | Container deployment (optional) |
| **Gmail Account** | — | SMTP email delivery |
| **Gemini API Key** | — | Google AI for email composition |

## 🛠️ Setup

### 1. Get Credentials

- **Gmail App Password**: Enable 2FA → [Generate App Password](https://myaccount.google.com/apppasswords)
- **Gemini API Key**: [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env:
#   GOOGLE_API_KEY=your_gemini_api_key
#   MAIL_USERNAME=your_email@gmail.com
#   MAIL_PASSWORD=your_app_specific_password
```

### 3. Start Services

#### Option A: Local Development

**Terminal 1 — Java Email Service:**
```bash
cd mail-tool-service
mvn clean install
mvn spring-boot:run
# Running on http://localhost:8080
```

**Terminal 2 — Python Agent:**
```bash
cd EmailAgent

# Create & activate virtual environment
python -m venv agentenv
agentenv\Scripts\activate        # Windows
# source agentenv/bin/activate   # Linux/Mac

pip install -r requirements.txt
uvicorn main:app --reload
# Running on http://localhost:8000
```

#### Option B: Docker Compose

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
```

## 📁 Project Structure

```
PersonalMailAgent/
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── EmailAgent/                          # Python FastAPI Agent
│   ├── main.py                         # App entry point & AI logic
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Local env vars (not committed)
│   └── agentenv/                       # Virtual environment
│
└── mail-tool-service/                   # Spring Boot Email Service
    ├── pom.xml                         # Maven config
    ├── Dockerfile
    └── src/main/
        ├── java/com/bharatmarwah/mail_tool_service/
        │   ├── MailToolServiceApplication.java
        │   ├── Controller/
        │   │   └── EmailController.java
        │   ├── Service/
        │   │   └── EmailService.java
        │   └── Model/
        │       └── EmailSendRequest.java
        └── resources/
            ├── application.properties
            ├── application-dev.properties
            └── application-prod.properties
```

## 🔌 API Reference

### POST `/chat` — Compose & Send Email

Send a prompt and the agent writes a professional email and delivers it.

**Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email": "recipient@example.com",
    "content": "Thank them for attending the meeting and confirm next steps",
    "words": 200
  }'
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `email` | string | *required* | Recipient email address |
| `content` | string | *required* | What the email should be about |
| `words` | int | `150` | Minimum word count |

**Response:**
```json
{
  "status": "Email Sent",
  "service_response": {
    "success": true,
    "data": "Email sent successfully"
  }
}
```

### POST `/api/email` — Direct Email (Java Service)

Send an email directly without AI composition.

```bash
curl -X POST http://localhost:8080/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Meeting Confirmation",
    "body": "Hi, confirming our meeting tomorrow at 2pm."
  }'
```

### Interactive Documentation

| Service | URL |
|---------|-----|
| FastAPI Swagger | http://localhost:8000/docs |
| FastAPI ReDoc | http://localhost:8000/redoc |
| Spring Boot Swagger | http://localhost:8080/swagger-ui.html |

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | ✅ | — | Gemini API key |
| `MAIL_USERNAME` | ✅ | — | Gmail address (Java service) |
| `MAIL_PASSWORD` | ✅ | — | Gmail app-specific password |
| `MAIL_SERVICE_URL` | ❌ | `http://localhost:8080` | Java service URL |

## 🧰 Tech Stack

### Python Agent
| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.135.1 | Web framework |
| Uvicorn | 0.41.0 | ASGI server |
| LangChain Core | 1.2.16 | LLM abstraction |
| LangChain Google GenAI | 4.2.1 | Gemini integration |
| Pydantic | 2.12.5 | Request validation |
| httpx | 0.28.1 | Async HTTP client |

### Java Email Service
| Component | Version | Purpose |
|-----------|---------|---------|
| Spring Boot | 3.5.11 | Web framework |
| Java | 21 | Runtime |
| Spring Mail | — | SMTP email sending |
| SpringDoc OpenAPI | 2.8.15 | Swagger UI |
| Lombok | — | Boilerplate reduction |

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `Could not import module "main"` | Run `uvicorn` from inside the `EmailAgent/` directory |
| SMTP authentication failed | Use a Gmail [App Password](https://myaccount.google.com/apppasswords), not your regular password |
| Connection refused to mail service | Make sure the Java service is running on port 8080 first |
| Module not found errors | Activate the virtual environment and run `pip install -r requirements.txt` |
| Port already in use | Stop the conflicting process or change the port |

## 🐳 Docker Services

The `docker-compose.yml` defines:
- **mail-tool-service** — Spring Boot on port 8080 with health checks
- **email-agent** — FastAPI on port 8000, depends on mail service health
- **mail-agent-network** — Bridge network for inter-service communication

Both services include automatic restart, JSON logging, and health monitoring.

---

**Made with ❤️ by bharatmarwah**
