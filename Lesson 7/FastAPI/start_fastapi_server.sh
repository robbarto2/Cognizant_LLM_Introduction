#!/bin/bash

# Start the FastAPI server for ChatGPT API routing

echo "Starting ChatGPT API Router..."

# Set default environment variables if not set
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-4o-mini}"
export FASTAPI_HOST="${FASTAPI_HOST:-0.0.0.0}"
export FASTAPI_PORT="${FASTAPI_PORT:-8000}"

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY environment variable is not set!"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key-here'"
    echo "The server will start but API calls will fail."
fi

echo "Starting server on ${FASTAPI_HOST}:${FASTAPI_PORT}"
echo "API documentation available at: http://${FASTAPI_HOST}:${FASTAPI_PORT}/docs"
echo "Press Ctrl+C to stop the server"

# Start the FastAPI server
python openai_fastapi_router.py
