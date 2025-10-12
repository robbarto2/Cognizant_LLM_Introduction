#!/bin/bash

# Configuration
FASTAPI_BASE_URL="${FASTAPI_BASE_URL:-http://localhost:8000}"
USER_ID="${USER_ID:-default}"

# Function to make request to FastAPI (non-streaming)
make_streaming_request() {
    local message="$1"
    
    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "{\n            \"messages\": [{\"role\": \"user\", \"content\": \"${message}\"}],\n            \"model\": \"${OPENAI_MODEL:-gpt-4o-mini}\",\n            \"temperature\": 0.7,\n            \"stream\": false,\n            \"user_id\": \"${USER_ID}\"\n        }"
}

# Function to make non-streaming request to FastAPI
make_request() {
    local message="$1"
    
    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "{
            \"messages\": [{\"role\": \"user\", \"content\": \"${message}\"}],
            \"model\": \"${OPENAI_MODEL:-gpt-4o-mini}\",
            \"temperature\": 0.7,
            \"stream\": false,
            \"user_id\": \"${USER_ID}\"
        }"
}

# Function to check usage stats
check_usage() {
    curl "${FASTAPI_BASE_URL}/usage/${USER_ID}" \
        -H "Accept: application/json"
}

# Main script logic
case "${1:-normal}" in
    "stream")
        echo "Making request (non-streaming via former streaming function)..."
        make_streaming_request "Explain Q-LoRA in 3 steps."
        ;;
    "normal")
        echo "Making normal request..."
        make_request "Explain Q-LoRA in 3 steps."
        ;;
    "usage")
        echo "Checking usage stats..."
        check_usage
        ;;
    "custom")
        if [ -z "$2" ]; then
            echo "Usage: $0 custom \"Your message here\""
            exit 1
        fi
        echo "Making custom streaming request..."
        make_streaming_request "$2"
        ;;
    *)
        echo "Usage: $0 [normal|stream|usage|custom \"message\"]"
        echo "  normal  - Make non-streaming request (default)"
        echo "  stream  - Make request via /chat (configured non-streaming)"
        echo "  usage   - Check usage statistics"
        echo "  custom  - Make custom non-streaming request with your message"
        exit 1
        ;;
esac
