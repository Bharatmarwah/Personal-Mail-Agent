from fastapi import FastAPI
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import httpx
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Mail Agent",
    description="AI-powered email agent that processes natural language requests and sends emails intelligently",
    version="1.0.0"
)


class Message(BaseModel):
    email: str = Field(..., description="User's email address")
    content: str = Field(..., description="User's request or message")
    words: int = Field(default=200, description="Maximum response length in words")


class EmailResponse(BaseModel):
    status: str
    service_response: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: Optional[str] = None
    status: Optional[str] = None
    service_response: Optional[Dict[str, Any]] = None


# Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_output_tokens=1024,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    logger.info("Gemini LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini LLM: {e}")
    raise

tools = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to the specified recipient with subject and body.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Recipient's email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content"
                    }
                },
                "required": ["email", "subject", "body"]
            }
        }
    }
]


async def call_email_service(to: str, subject: str, body: str) -> Dict[str, Any]:


    mail_service_url = os.getenv("MAIL_SERVICE_URL", "http://localhost:8080")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            logger.info(f"Calling email service for recipient: {to}")
            response = await client.post(
                f"{mail_service_url}/api/email",
                json={
                    "to": to,
                    "subject": subject,
                    "body": body
                }
            )

            response.raise_for_status()

            logger.info(f"Email sent successfully to {to}")
            return {
                "success": True,
                "data": response.json()
            }

        except httpx.HTTPStatusError as exc:
            error_msg = f"HTTP error: {exc.response.status_code}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "details": exc.response.text
            }

        except httpx.RequestError as exc:
            error_msg = "Spring service unreachable"
            logger.error(f"{error_msg}: {exc}")
            return {
                "success": False,
                "error": error_msg,
                "details": str(exc)
            }

        except Exception as exc:
            error_msg = "Unexpected error"
            logger.error(f"{error_msg}: {exc}")
            return {
                "success": False,
                "error": error_msg,
                "details": str(exc)
            }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):

    logger.info(f"Processing chat message from {message.email}")

    user_prompt = f"""You are an intelligent email assistant. Process the following user request regarding email communication.

User Email: {message.email}
User Request: {message.content}
Response Limit: {message.words} words maximum

Guidelines:
1. Carefully analyze what the user is asking for
2. If the user explicitly wants to send an email, use the send_email tool with an appropriate subject and body
3. Only use the tool when the intent to send an email is clear and unambiguous
4. If no email is needed, provide a helpful conversational response
5. Keep responses professional and concise
6. Do not make assumptions about email content - ask clarifying questions if needed
"""

    try:
        response = llm.invoke(
            [HumanMessage(content=user_prompt)],
            tools=tools
        )
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name == "send_email":
                logger.info(f"Agent decided to send email to {tool_args.get('email')}")
                result = await call_email_service(
                    to=tool_args["email"],
                    subject=tool_args["subject"],
                    body=tool_args["body"]
                )
                return ChatResponse(
                    status="Email Sent",
                    service_response=result
                )


        logger.info("Agent provided conversational response")
        return ChatResponse(reply=response.content)

    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return ChatResponse(reply=f"Error processing your request: {str(e)}")


@app.get("/")
async def root():
    return {
        "message": "Personal Mail Agent API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
