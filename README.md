# Personal Mail Agent

**An intelligent, microservices-based email automation system powered by Google's Gemini AI**

A production-ready application that combines a Python FastAPI agent with a Spring Boot email service, enabling users to compose and send emails through natural language requests. The system intelligently decides when to send emails and when to provide advisory feedback.

**Author**: [bharatmarwah](https://github.com/bharatmarwah)  
**License**: MIT  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

## 📊 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   FastAPI Agent Service                      │
│              (Python 3.11 + Gemini 2.5-Flash)               │
│  • NLP Processing  • Intent Recognition  • Email Composition │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP/REST API (Port 8000)
                     │ JSON Request/Response
                     ▼
┌──────────────────────────────────────────────────────────────┐
│              Spring Boot Email Service                       │
│           (Java 21 + Spring Boot 3.5.11)                    │
│  • SMTP Gateway  • Email Validation  • Async Processing     │
└──────────────────────────────────────────────────────────────┘
                     │
                     ▼
              Gmail SMTP Server
```

## ✨ Core Features

- **🤖 AI-Powered Interactions**: Natural language understanding using Gemini AI
- **📧 Intelligent Email Routing**: Decides whether to send emails or provide guidance
- **⚡ Async Email Processing**: Non-blocking operations for high throughput
- **🔒 Secure Authentication**: Environment-based credential management
- **📊 Comprehensive Logging**: Detailed request/response logging for auditing
- **🔄 Error Resilience**: Graceful failure handling with meaningful error messages
- **📚 API Documentation**: Interactive Swagger/OpenAPI documentation
- **🐳 Container Ready**: Docker and Docker Compose support included
- **☁️ Cloud Deployable**: Works on AWS, GCP, Azure, and on-premises


## 📋 Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | FastAPI agent runtime |
| **Java** | 21+ | Spring Boot service runtime |
| **Maven** | 3.8+ | Java dependency management |
| **Docker** | 20.10+ | Container runtime (optional) |
| **Gmail Account** | - | SMTP server for email delivery |
| **Gemini API Key** | - | Google AI integration |

## 🛠️ Installation & Setup

### Option 1: Local Development (Recommended for Development)

#### Step 1: Configure Environment

```bash
# Clone the repository
git clone <repository-url>
cd PersonalMailAgent

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Required:
# - MAIL_USERNAME=your_email@gmail.com
# - MAIL_PASSWORD=your_app_specific_password
# - GOOGLE_API_KEY=your_gemini_api_key
```

**Obtaining Credentials:**

1. **Gmail SMTP Credentials**:
   - Enable 2-Factor Authentication on your Gmail account
   - Visit: https://myaccount.google.com/apppasswords
   - Generate an app-specific password
   - Use this password in `MAIL_PASSWORD`

2. **Gemini API Key**:
   - Visit: https://aistudio.google.com/apikey
   - Create a new API key
   - Copy and paste into `GOOGLE_API_KEY`

#### Step 2: Start Java Service (Terminal 1)

```bash
cd mail-tool-service

# Build and run
mvn clean install
mvn spring-boot:run

# Service will start on http://localhost:8080
# Swagger UI: http://localhost:8080/swagger-ui.html
```

#### Step 3: Start Python Agent (Terminal 2)

```bash
cd EmailAgent

# Create and activate virtual environment
python -m venv agentenv

# Windows:
agentenv\Scripts\activate

# Linux/Mac:
source agentenv/bin/activate

# Install dependencies and run
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Agent will start on http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

### Option 2: Docker Deployment (Recommended for Production)

```bash
# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start all services
docker-compose up -d

# Verify services
docker-compose ps

# View logs
docker-compose logs -f

# Services available at:
# - Java: http://localhost:8080
# - Agent: http://localhost:8000
```


## 📁 Project Structure

```
PersonalMailAgent/
├── 📄 README.md                         # Project documentation
├── 📄 QUICK_REFERENCE.md                # Quick start guide
├── 📄 TESTING.md                        # Testing procedures
├── 📄 DEPLOYMENT.md                     # Deployment instructions
├── 📄 PROJECT_ASSESSMENT.md             # Architecture review
├── 📄 AGENT_RATING.md                   # Agent evaluation
├── 📄 docker-compose.yml                # Multi-service orchestration
├── 📄 .env.example                      # Environment template
├── 📄 .gitignore                        # Git ignore rules
│
├── 📁 EmailAgent/                       # Python FastAPI Service
│   ├── main.py                         # FastAPI application & agent logic
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Container configuration
│   ├── .env.example                    # Environment variables
│   └── agentenv/                       # Virtual environment
│
└── 📁 mail-tool-service/               # Spring Boot Service
    ├── pom.xml                         # Maven configuration
    ├── Dockerfile                      # Container configuration
    ├── .env.example                    # Environment variables
    ├── src/
    │   ├── main/
    │   │   ├── java/com/bharatmarwah/mail_tool_service/
    │   │   │   ├── MailToolServiceApplication.java
    │   │   │   ├── Controller/
    │   │   │   │   └── EmailController.java
    │   │   │   ├── Service/
    │   │   │   │   └── EmailService.java
    │   │   │   └── Model/
    │   │   │       └── EmailSendRequest.java
    │   │   └── resources/
    │   │       ├── application.properties
    │   │       ├── application-dev.properties
    │   │       └── application-prod.properties
    │   └── test/
    │       └── java/com/bharatmarwah/...
    └── target/                        # Build output
```


## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Google Gemini API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# Gmail SMTP Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_specific_password

# Service Configuration
MAIL_SERVICE_URL=http://localhost:8080
APP_ENV=development
LOG_LEVEL=INFO
```

### Java Application Configuration

**Development Profile** (`application-dev.properties`):
```properties
logging.level.root=INFO
logging.level.com.bharatmarwah=DEBUG
springdoc.swagger-ui.enabled=true
spring.mail.properties.mail.smtp.connectiontimeout=5000
```

**Production Profile** (`application-prod.properties`):
```properties
logging.level.root=WARN
logging.level.com.bharatmarwah=INFO
springdoc.swagger-ui.enabled=false
spring.mail.properties.mail.smtp.connectiontimeout=10000
```

To use a specific profile:
```bash
# Development
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=dev"

# Production
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=prod"
```


## 🔌 API Reference

### Python Agent Endpoints

#### POST /chat - Process User Request

Send a message to the agent for processing. The agent determines whether to send an email or provide a conversational response.

**Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "content": "Send an email to john@example.com saying we have a meeting tomorrow at 2pm",
    "words": 200
  }'
```

**Response (Email Sent):**
```json
{
  "status": "Email Sent",
  "service_response": {
    "success": true,
    "data": "Email sent successfully"
  },
  "reply": null
}
```

**Response (Conversational):**
```json
{
  "reply": "I'd recommend sending a professional email confirming the meeting details...",
  "status": null,
  "service_response": null
}
```

#### GET /health - Health Check

Check if the agent service is running.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET / - API Information

Get information about the API.

```bash
curl http://localhost:8000/
```

### Java Email Service Endpoints

#### POST /api/email - Send Email Directly

Send an email directly without going through the agent.

**Request:**
```bash
curl -X POST http://localhost:8080/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Meeting Confirmation",
    "body": "Hi John, we have confirmed the meeting for tomorrow at 2pm. Looking forward to it!"
  }'
```

**Response:**
```json
"Email sent successfully"
```

#### GET /actuator/health - Service Health

Check Spring Boot service health.

```bash
curl http://localhost:8080/actuator/health
```

### Interactive Documentation

- **Python API Docs**: http://localhost:8000/docs
- **Python ReDoc**: http://localhost:8000/redoc
- **Java Swagger UI**: http://localhost:8080/swagger-ui.html


## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# 1. Clone repository and setup
git clone <repository-url>
cd PersonalMailAgent

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Start services
docker-compose up -d

# 4. Verify services
docker-compose ps

# 5. View logs
docker-compose logs -f

# 6. Test services
curl http://localhost:8000/health
curl http://localhost:8080/actuator/health

# 7. Stop services
docker-compose down
```

### Building Individual Docker Images

**Java Email Service:**
```bash
cd mail-tool-service
docker build -t mail-tool-service:1.0.0 .
docker run -d -p 8080:8080 \
  -e MAIL_USERNAME=your_email@gmail.com \
  -e MAIL_PASSWORD=your_password \
  mail-tool-service:1.0.0
```

**Python Agent:**
```bash
cd EmailAgent
docker build -t email-agent:1.0.0 .
docker run -d -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  -e MAIL_SERVICE_URL=http://mail-tool-service:8080 \
  email-agent:1.0.0
```

### Docker Compose Services

The `docker-compose.yml` file defines:
- **mail-tool-service**: Spring Boot email service (port 8080)
- **email-agent**: FastAPI agent service (port 8000)
- **mail-agent-network**: Bridge network for inter-service communication

Services include:
- Health checks
- Automatic restart
- JSON logging
- Proper dependency management


## 🧪 Testing & Examples

### Basic Functionality Test

**Test 1: Agent Health Check**
```bash
curl http://localhost:8000/health
```

**Test 2: Send Email via Agent**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "content": "Send an email to recipient@example.com saying hello",
    "words": 100
  }'
```

**Test 3: Direct Email Service**
```bash
curl -X POST http://localhost:8080/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email"
  }'
```

### Comprehensive Testing

For detailed testing procedures, see [TESTING.md](TESTING.md) which includes:
- Unit test examples
- Integration test scenarios
- Load testing procedures
- Performance benchmarks

## 🔍 Troubleshooting

### Java Service Issues

**Port 8080 Already in Use:**
```bash
# Find process using port
lsof -i :8080

# Or use a different port
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8081"
```

**SMTP Authentication Failed:**
1. Verify Gmail 2-FA is enabled
2. Generate app-specific password from: https://myaccount.google.com/apppasswords
3. Use app password in `MAIL_PASSWORD` (not your Gmail password)
4. Check environment variables are set correctly

**Cannot Find Mail Service:**
```bash
# Ensure Java service is running
curl http://localhost:8080/actuator/health

# Check firewall settings
# Port 8080 must be accessible
```

### Python Agent Issues

**Module Import Error:**
```bash
# Activate virtual environment
agentenv\Scripts\activate  # Windows
source agentenv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Connection Refused (Email Service):**
1. Ensure Java service is running on port 8080
2. Verify `MAIL_SERVICE_URL` environment variable is correct
3. Check network connectivity between containers (if using Docker)

**Invalid API Key:**
1. Generate new API key: https://aistudio.google.com/apikey
2. Set `GOOGLE_API_KEY` environment variable
3. Verify API is enabled in Google Cloud Console

### Docker-Related Issues

**Services Cannot Communicate:**
```bash
# Verify network
docker network inspect personal-mail-agent_mail-agent-network

# Check service names
docker-compose ps
```

**Port Already in Use:**
```bash
# Modify docker-compose.yml ports
# Or stop conflicting services
docker ps
docker stop <container-id>
```

For more troubleshooting help, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 Technology Stack

### Backend Services (Java)
| Component | Version | Purpose |
|-----------|---------|---------|
| **Spring Boot** | 3.5.11 | Web framework |
| **Java** | 21 | Runtime environment |
| **Maven** | 3.8+ | Build & dependency management |
| **Lombok** | Latest | Boilerplate reduction |
| **SpringDoc** | 2.8.15 | OpenAPI/Swagger documentation |

### Agent Services (Python)
| Component | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.135.1 | Web framework |
| **Python** | 3.10+ | Runtime environment |
| **LangChain** | 0.1.20 | LLM integration |
| **Gemini AI** | Latest | Natural language processing |
| **Pydantic** | 2.7.4 | Data validation |
| **httpx** | 0.27.1 | Async HTTP client |

## 📖 Additional Documentation

For more detailed information, refer to:
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick API examples and commands
- **[TESTING.md](TESTING.md)** - Testing strategies and procedures
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guides for cloud platforms
- **[PROJECT_ASSESSMENT.md](PROJECT_ASSESSMENT.md)** - Architecture review and analysis
- **[AGENT_RATING.md](AGENT_RATING.md)** - Agent evaluation and performance metrics

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes (`git commit -m 'Add your feature'`)
4. **Push** to the branch (`git push origin feature/your-feature`)
5. **Submit** a Pull Request

### Development Guidelines
- Follow existing code conventions
- Add tests for new features
- Update documentation accordingly
- Keep commits atomic and descriptive

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Bharat Marwah** (bharatmarwah)

---

## 🔗 Quick Links

- 📖 [Full Documentation](./docs/)
- 🐛 [Report Issues](https://github.com/bharatmarwah/PersonalMailAgent/issues)
- 💡 [Feature Requests](https://github.com/bharatmarwah/PersonalMailAgent/discussions)
- 🌟 [Star on GitHub](https://github.com/bharatmarwah/PersonalMailAgent)

## ⚠️ Important Notes

- **API Keys**: Never commit `.env` files with credentials. Use environment variables or secrets management systems in production.
- **Email Configuration**: Use app-specific passwords for Gmail, not your main account password.
- **Production Use**: Implement API authentication and rate limiting before deploying to production.
- **Compliance**: Ensure compliance with email sending regulations (CAN-SPAM, GDPR, etc.)

---

**Last Updated**: March 2, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

**Made with ❤️ by bharatmarwah**

