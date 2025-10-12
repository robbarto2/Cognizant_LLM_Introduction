from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
import requests
import os
import json
import time
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChatGPT API Router",
    description="A FastAPI router to control and manage ChatGPT API usage",
    version="1.0.0"
)

# In-memory storage for API usage tracking (in production, use Redis or a database)
api_usage_tracker = {
    "requests_per_minute": {},
    "daily_usage": {},
    "blocked_users": set()
}

# Custom handler to provide clearer 422 messages
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return a more descriptive 422 response when request validation fails.

    Adds human-friendly hints for common cases like temperature being out of range.
    """
    errors = exc.errors()
    detailed_errors = []

    for err in errors:
        loc = err.get("loc", [])
        loc_str = ".".join(str(x) for x in loc)
        msg = err.get("msg")
        typ = err.get("type")
        ctx = err.get("ctx") or {}

        hint = None
        # Provide specific guidance for temperature range violations
        if "temperature" in loc_str:
            ge = ctx.get("ge")
            le = ctx.get("le")
            if ge is not None and le is not None:
                hint = f"Temperature must be between {ge} and {le}."
            elif ge is not None:
                hint = f"Temperature must be >= {ge}."
            elif le is not None:
                hint = f"Temperature must be <= {le}."

        detailed_errors.append({
            "field": loc_str,
            "message": msg,
            "type": typ,
            "hint": hint
        })

    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "error": "Unprocessable Entity",
            "method": request.method,
            "path": str(request.url.path),
            # Original FastAPI/Pydantic validation details
            "detail": errors,
            # Enhanced, human-friendly details with hints
            "enhanced_detail": detailed_errors,
            "explanation": "Your request body failed validation. Fix the invalid fields and try again."
        },
    )

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1, max_length=10000)

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., min_items=1, max_items=50)
    model: Optional[str] = Field("gpt-4o-mini", pattern="^(gpt-4o|gpt-4o-mini|gpt-3.5-turbo)$")
    temperature: float = Field(0.7, ge=0.5, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)
    stream: bool = Field(False)
    user_id: Optional[str] = Field(None, max_length=100)

    @field_validator('messages')
    def validate_messages(cls, v):
        if not v:
            raise ValueError('At least one message is required')
        
        # Check for prompt injection attempts
        for message in v:
            content_lower = message.content.lower()
            suspicious_patterns = [
                'ignore previous', 'system:', 'assistant:', 'forget everything',
                'new instructions:', 'override:', 'jailbreak', 'roleplay'
            ]
            if any(pattern in content_lower for pattern in suspicious_patterns):
                raise ValueError('Potential prompt injection detected')
        
        return v

class UsageStats(BaseModel):
    total_requests: int
    requests_this_minute: int
    requests_today: int
    is_blocked: bool

def check_rate_limit(user_id: str = "default") -> bool:
    """Check if user has exceeded rate limits"""
    current_time = time.time()
    current_minute = int(current_time // 60)
    current_day = int(current_time // 86400)
    
    # Check daily limit (100 requests per day)
    if user_id not in api_usage_tracker["daily_usage"]:
        api_usage_tracker["daily_usage"][user_id] = {}
    
    if current_day not in api_usage_tracker["daily_usage"][user_id]:
        api_usage_tracker["daily_usage"][user_id][current_day] = 0
    
    if api_usage_tracker["daily_usage"][user_id][current_day] >= 100:
        return False
    
    # Check per-minute limit (10 requests per minute)
    if user_id not in api_usage_tracker["requests_per_minute"]:
        api_usage_tracker["requests_per_minute"][user_id] = {}
    
    if current_minute not in api_usage_tracker["requests_per_minute"][user_id]:
        api_usage_tracker["requests_per_minute"][user_id][current_minute] = 0
    
    if api_usage_tracker["requests_per_minute"][user_id][current_minute] >= 10:
        return False
    
    return True

def update_usage_stats(user_id: str = "default"):
    """Update usage statistics"""
    current_time = time.time()
    current_minute = int(current_time // 60)
    current_day = int(current_time // 86400)
    
    # Update daily usage
    if user_id not in api_usage_tracker["daily_usage"]:
        api_usage_tracker["daily_usage"][user_id] = {}
    if current_day not in api_usage_tracker["daily_usage"][user_id]:
        api_usage_tracker["daily_usage"][user_id][current_day] = 0
    api_usage_tracker["daily_usage"][user_id][current_day] += 1
    
    # Update per-minute usage
    if user_id not in api_usage_tracker["requests_per_minute"]:
        api_usage_tracker["requests_per_minute"][user_id] = {}
    if current_minute not in api_usage_tracker["requests_per_minute"][user_id]:
        api_usage_tracker["requests_per_minute"][user_id][current_minute] = 0
    api_usage_tracker["requests_per_minute"][user_id][current_minute] += 1

@app.get("/")
async def root():
    return {"message": "ChatGPT API Router", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/usage/{user_id}")
async def get_usage_stats(user_id: str) -> UsageStats:
    """Get usage statistics for a user"""
    current_time = time.time()
    current_minute = int(current_time // 60)
    current_day = int(current_time // 86400)
    
    requests_this_minute = api_usage_tracker["requests_per_minute"].get(user_id, {}).get(current_minute, 0)
    requests_today = api_usage_tracker["daily_usage"].get(user_id, {}).get(current_day, 0)
    total_requests = sum(api_usage_tracker["daily_usage"].get(user_id, {}).values())
    is_blocked = user_id in api_usage_tracker["blocked_users"]
    
    return UsageStats(
        total_requests=total_requests,
        requests_this_minute=requests_this_minute,
        requests_today=requests_today,
        is_blocked=is_blocked
    )

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Non-streaming chat endpoint"""
    user_id = request.user_id or "default"
    
    # Check if user is blocked
    if user_id in api_usage_tracker["blocked_users"]:
        raise HTTPException(status_code=403, detail="User is blocked from using the API")
    
    # Check rate limits
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Update usage stats
    update_usage_stats(user_id)
    
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    
    # Prepare OpenAI request
    openai_request = {
        "model": request.model,
        "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        "temperature": request.temperature,
        "stream": False
    }
    
    if request.max_tokens:
        openai_request["max_tokens"] = request.max_tokens
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=openai_request,
            timeout=60
        )
        response.raise_for_status()
        
        logger.info(f"Chat request completed for user {user_id}")
        return response.json()
        
    except requests.HTTPError as http_err:
        logger.error(f"OpenAI API error: {http_err}")
        detail = response.text if hasattr(response, 'text') else str(http_err)
        raise HTTPException(status_code=response.status_code if response else 502, detail=detail)
    except requests.RequestException as req_err:
        logger.error(f"Request error: {req_err}")
        raise HTTPException(status_code=502, detail=str(req_err))

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint"""
    user_id = request.user_id or "default"
    
    # Check if user is blocked
    if user_id in api_usage_tracker["blocked_users"]:
        raise HTTPException(status_code=403, detail="User is blocked from using the API")
    
    # Check rate limits
    if not check_rate_limit(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Update usage stats
    update_usage_stats(user_id)
    
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    
    # Prepare OpenAI request
    openai_request = {
        "model": request.model,
        "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        "temperature": request.temperature,
        "stream": True
    }
    
    if request.max_tokens:
        openai_request["max_tokens"] = request.max_tokens
    
    def generate_stream():
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json=openai_request,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = line_str[6:]  # Remove 'data: ' prefix
                        if data.strip() == '[DONE]':
                            break
                        yield f"data: {data}\n\n"
            
            logger.info(f"Streaming chat request completed for user {user_id}")
            
        except requests.HTTPError as http_err:
            logger.error(f"OpenAI API streaming error: {http_err}")
            error_data = {
                "error": {
                    "message": str(http_err),
                    "type": "api_error"
                }
            }
            yield f"data: {json.dumps(error_data)}\n\n"
        except requests.RequestException as req_err:
            logger.error(f"Request streaming error: {req_err}")
            error_data = {
                "error": {
                    "message": str(req_err),
                    "type": "request_error"
                }
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.post("/admin/block-user/{user_id}")
async def block_user(user_id: str):
    """Block a user from using the API"""
    api_usage_tracker["blocked_users"].add(user_id)
    logger.info(f"User {user_id} has been blocked")
    return {"message": f"User {user_id} has been blocked"}

@app.delete("/admin/unblock-user/{user_id}")
async def unblock_user(user_id: str):
    """Unblock a user"""
    api_usage_tracker["blocked_users"].discard(user_id)
    logger.info(f"User {user_id} has been unblocked")
    return {"message": f"User {user_id} has been unblocked"}

@app.delete("/admin/reset-usage/{user_id}")
async def reset_user_usage(user_id: str):
    """Reset usage statistics for a user"""
    if user_id in api_usage_tracker["requests_per_minute"]:
        del api_usage_tracker["requests_per_minute"][user_id]
    if user_id in api_usage_tracker["daily_usage"]:
        del api_usage_tracker["daily_usage"][user_id]
    api_usage_tracker["blocked_users"].discard(user_id)
    logger.info(f"Usage statistics reset for user {user_id}")
    return {"message": f"Usage statistics reset for user {user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
