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
    version="2.0.0",
    credits="Bharat Marwah"
)


class Message(BaseModel):
    email: str = Field(..., description="Recipient email")
    content: str = Field(..., description="What the email should be about")
    words: int = Field(default=150, description="Minimum word count")


class ChatResponse(BaseModel):
    status: Optional[str] = None
    service_response: Optional[Dict[str, Any]] = None


def extract_text(resp):
    content = resp.content
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content)
    return content


def word_count(text: str):
    return len(text.split())



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.8,
    max_output_tokens=2048,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

logger.info("Gemini initialized")



async def call_email_service(to: str, subject: str, body: str):

    mail_service_url = os.getenv("MAIL_SERVICE_URL", "http://localhost:8080")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                f"{mail_service_url}/api/email",
                json={
                    "to": to,
                    "subject": subject,
                    "body": body
                }
            )

            response.raise_for_status()

            # Avoid JSON parsing error if empty
            if response.content:
                try:
                    data = response.json()
                except:
                    data = response.text
            else:
                data = "Email sent successfully"

            return {
                "success": True,
                "data": data
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }



@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):

    logger.info(f"Generating email for {message.email}")

    base_prompt = f"""
You are a professional email writer.

The sender's name is Bharat.
The email should be written as if Bharat is sending it.

Email Topic: {message.content}

Requirements:
- Minimum {message.words} words
- Include greeting
- End the email with:

Warm regards,
Bharat    
"""
# add your name in the end
    try:

        response = llm.invoke([HumanMessage(content=base_prompt)])
        email_body = extract_text(response)

        if word_count(email_body) < message.words:
            logger.info("Regenerating due to short length")

            stronger_prompt = base_prompt + "\nThe previous response was too short. Expand significantly."

            response = llm.invoke([HumanMessage(content=stronger_prompt)])
            email_body = extract_text(response)

        subject = "Regarding: " + message.content[:50]

        result = await call_email_service(
            to=message.email,
            subject=subject,
            body=email_body
        )

        return ChatResponse(
            status="Email Sent",
            service_response=result
        )

    except Exception as e:
        logger.error(f"Agent error: {e}")
        return ChatResponse(
            status="Error"
        )
