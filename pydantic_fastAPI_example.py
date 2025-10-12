from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import requests
import os

app = FastAPI()

class LLMRequest(BaseModel):
    user_message: str = Field(..., max_length=4000, min_length=1)
    temperature: float = Field(0.2, ge=0, le=2)

    @field_validator('user_message')
    def sanitize_message(cls, v: str) -> str:
        if any(keyword in v.lower() for keyword in ['ignore previous', 'system:']):
            raise ValueError('Potential prompt injection detected')
        return v.strip()

@app.post("/chat")
def chat_endpoint(request: LLMRequest):
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": request.user_message},
                ],
                "temperature": request.temperature,
            },
            timeout=60
        )
        resp.raise_for_status()
    except requests.HTTPError as http_err:
        # Bubble up OpenAI error body to the client for easier debugging
        detail = getattr(resp, "text", str(http_err))
        raise HTTPException(status_code=resp.status_code if resp is not None else 502, detail=detail)
    except requests.RequestException as req_err:
        raise HTTPException(status_code=502, detail=str(req_err))
    return resp.json()