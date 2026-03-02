# Personal Mail Agent

A sophisticated multi-service application that combines a Python FastAPI agent powered by Google's Gemini AI with a Spring Boot email service. The agent intelligently processes user requests and automatically sends emails when appropriate.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Agent (Python)                   │
│          (Powered by Gemini 2.5-Flash + LangChain)          │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP Requests (EmailSendRequest)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│            Spring Boot Email Service (Java)                 │
│    (Configured with Gmail SMTP + JWT Authentication)        │
└──────────────────────────────────────────────────────────────┘
```

## 📋 Features

- **AI-Powered Email Agent**: Processes natural language requests and decides when to send emails
- **Dual Service Architecture**: Separation of concerns with dedicated agent and email services
- **Async Email Processing**: Non-blocking email operations for better performance
- **Comprehensive Error Handling**: Graceful error handling and logging across all services
- **RESTful APIs**: Well-documented endpoints with OpenAPI/Swagger support
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Environment Configuration**: Secure handling of credentials via environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Java 21+
- Maven 3.8+
- Gmail Account (for SMTP configuration)
- Google Gemini API Key

### Installation

#### 1. Clone and Setup Python Agent

```bash
cd EmailAgent
python -m venv agentenv
agentenv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set GOOGLE_API_KEY=your_gemini_api_key
```

#### 2. Configure Java Service

```bash
cd mail-tool-service

# Set environment variables
set MAIL_USERNAME=your_email@gmail.com
set MAIL_PASSWORD=your_app_password

# Build the project
mvn clean install

# Run the service
mvn spring-boot:run
```

### Running the Application

**Terminal 1 - Start Java Email Service:**
```bash
cd mail-tool-service
mvn spring-boot:run
# Runs on http://localhost:8080
```

**Terminal 2 - Start Python Agent:**
```bash
cd EmailAgent
agentenv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
# Runs on http://localhost:8000
```

**Test the Agent:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "content": "Send an email to john@example.com saying hello and asking how he is doing",
    "words": 200
  }'
```

## 📁 Project Structure

```
PersonalMailAgent/
├── EmailAgent/                          # Python FastAPI Agent
│   ├── main.py                         # FastAPI app with agent logic
│   ├── requirements.txt                # Python dependencies
│   ├── agentenv/                       # Virtual environment
│   └── .env.example                    # Environment variables template
│
├── mail-tool-service/                  # Spring Boot Email Service
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/bharatmarwah/mail_tool_service/
│   │   │   │   ├── MailToolServiceApplication.java
│   │   │   │   ├── Controller/
│   │   │   │   │   └── EmailController.java
│   │   │   │   ├── Service/
│   │   │   │   │   └── EmailService.java
│   │   │   │   └── Model/
│   │   │   │       └── EmailSendRequest.java
│   │   │   └── resources/
│   │   │       ├── application.properties
│   │   │       ├── application-dev.properties
│   │   │       └── application-prod.properties
│   │   └── test/
│   ├── pom.xml                         # Maven dependencies
│   ├── Dockerfile                      # Docker configuration
│   └── docker-compose.yml              # Multi-service orchestration
│
├── docker-compose.yml                  # Complete stack composition
├── README.md                           # This file
└── .env.example                        # Environment variables template
```

## 🔧 Configuration

### Java Service (application.properties)

```properties
spring.application.name=mail-tool-service
spring.mail.host=smtp.gmail.com
spring.mail.port=587
spring.mail.username=${MAIL_USERNAME}
spring.mail.password=${MAIL_PASSWORD}
spring.mail.properties.mail.smtp.auth=true
spring.mail.properties.mail.smtp.starttls.enable=true
```

### Python Agent (.env)

```
GOOGLE_API_KEY=your_gemini_api_key
MAIL_SERVICE_URL=http://localhost:8080
```

## 📚 API Endpoints

### Python Agent API

**POST /chat** - Process user message and optionally send email
```json
Request:
{
  "email": "user@example.com",
  "content": "Please send an email to john@example.com with subject 'Meeting Tomorrow' and say we have a meeting tomorrow at 2pm",
  "words": 200
}

Response (Email Sent):
{
  "status": "Email Sent",
  "service_response": {
    "success": true,
    "data": "Email sent successfully"
  }
}

Response (Chat Only):
{
  "reply": "I'd be happy to help you with that email! Here's a draft..."
}
```

### Java Email Service API

**POST /api/email** - Send email directly
```json
Request:
{
  "to": "recipient@example.com",
  "subject": "Meeting Tomorrow",
  "body": "Hi John, we have a meeting tomorrow at 2pm. Please confirm your attendance."
}

Response:
"Email sent successfully"
```

**GET /swagger-ui.html** - Swagger API Documentation

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Copy and configure environment variables
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Docker Images

**Build Java Service:**
```bash
cd mail-tool-service
docker build -t mail-tool-service:latest .
docker run -p 8080:8080 \
  -e MAIL_USERNAME=your_email@gmail.com \
  -e MAIL_PASSWORD=your_app_password \
  mail-tool-service:latest
```

**Build Python Agent:**
```bash
cd EmailAgent
docker build -t email-agent:latest .
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  -e MAIL_SERVICE_URL=http://mail-tool-service:8080 \
  email-agent:latest
```

## 🧪 Testing

### Test Email Sending via Agent

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sender@example.com",
    "content": "Send an email to recipient@example.com saying \"Hello, this is a test email from the AI agent!\"",
    "words": 150
  }'
```

### Test Direct Email Service

```bash
curl -X POST http://localhost:8080/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Mail Tool Service."
  }'
```

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files with real credentials
2. **API Keys**: Store Gemini API key securely
3. **SMTP Credentials**: Use app-specific passwords for Gmail (not your main password)
4. **HTTPS**: Use HTTPS in production
5. **Rate Limiting**: Consider implementing rate limits on the agent endpoint
6. **Input Validation**: All inputs are validated before processing

## 📊 Technology Stack

### Backend (Java)
- **Framework**: Spring Boot 3.5.11
- **Java Version**: 21
- **Build Tool**: Maven
- **Email**: JavaMailSender (Gmail SMTP)
- **Documentation**: SpringDoc OpenAPI (Swagger)
- **Logging**: SLF4J + Logback
- **Annotations**: Lombok

### Agent (Python)
- **Framework**: FastAPI
- **AI Model**: Gemini 2.5-Flash (via LangChain)
- **HTTP Client**: httpx (async)
- **Data Validation**: Pydantic
- **Server**: Uvicorn

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🆘 Troubleshooting

### Email Service Connection Error
- Ensure Spring Boot service is running on `http://localhost:8080`
- Check network connectivity between services
- Verify firewall settings

### Gmail SMTP Authentication Failed
- Enable "Less secure app access" or use app-specific passwords
- Verify `MAIL_USERNAME` and `MAIL_PASSWORD` are set correctly
- Check that credentials are properly escaped in environment variables

### Agent Not Sending Emails
- Check Gemini API key is valid
- Review service logs for error messages
- Ensure email service is accessible and responding
- Test with explicit email sending request

### Docker Services Not Communicating
- Ensure services are on the same Docker network
- Check service names in connection strings
- Verify exposed ports match service configuration


**Last Updated**: March 2, 2026
**by Bharat Marwah**

