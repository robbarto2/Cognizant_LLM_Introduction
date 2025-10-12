#!/bin/bash

# Configuration
FASTAPI_BASE_URL="${FASTAPI_BASE_URL:-http://localhost:8000}"
USER_ID="${USER_ID:-default}"

# Function to make streaming request to FastAPI
make_streaming_request() {
    local message="$1"
    
    curl "${FASTAPI_BASE_URL}/chat/stream" \
        -H "Content-Type: application/json" \
        -H "Accept: text/event-stream" \
        -d "{
            \"messages\": [{\"role\": \"user\", \"content\": \"${message}\"}],
            \"model\": \"${OPENAI_MODEL:-gpt-4o-mini}\",
            \"temperature\": 0.7,
            \"stream\": true,
            \"user_id\": \"${USER_ID}\"
        }" \
        --no-buffer
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
case "${1:-stream}" in
    "stream")
        echo "Making streaming request..."
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
        echo "Usage: $0 [stream|normal|usage|custom \"message\"]"
        echo "  stream  - Make streaming request (default)"
        echo "  normal  - Make non-streaming request"
        echo "  usage   - Check usage statistics"
        echo "  custom  - Make custom streaming request with your message"
        exit 1
        ;;
esac
