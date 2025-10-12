#!/bin/bash

# Configuration
FASTAPI_BASE_URL="${FASTAPI_BASE_URL:-http://localhost:8000}"
USER_ID="${USER_ID:-default}"

# Escape user input for safe embedding in JSON strings
json_escape() {
    local s="$1"
    s=${s//\\/\\\\}   # escape backslashes
    s=${s//\"/\\\"}   # escape double quotes
    s=${s//$'\n'/\\n}   # escape newlines
    echo "$s"
}

# Function to make request to FastAPI (non-streaming)
make_streaming_request() {
    local message="$1"
    local payload_message
    payload_message=$(json_escape "$message")
    
    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "{\n            \"messages\": [{\"role\": \"user\", \"content\": \"${payload_message}\"}],\n            \"model\": \"${OPENAI_MODEL:-gpt-4o-mini}\",\n            \"temperature\": 0.7,\n            \"stream\": false,\n            \"user_id\": \"${USER_ID}\"\n        }"
}

# Function to make non-streaming request to FastAPI
make_request() {
    local message="$1"
    local payload_message
    payload_message=$(json_escape "$message")
    
    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "{
            \"messages\": [{\"role\": \"user\", \"content\": \"${payload_message}\"}],
            \"model\": \"${OPENAI_MODEL:-gpt-4o-mini}\",
            \"temperature\": 0.9,
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
        read -rp "Enter your prompt: " USER_MESSAGE
        make_streaming_request "$USER_MESSAGE"
        ;;
    "normal")
        echo "Making normal request..."
        read -rp "Enter your prompt: " USER_MESSAGE
        make_request "$USER_MESSAGE"
        ;;
    "usage")
        echo "Checking usage stats..."
        check_usage
        ;;
    "custom")
        if [ -z "$2" ]; then
            read -rp "Enter your prompt: " USER_MESSAGE
        else
            USER_MESSAGE="$2"
        fi
        echo "Making custom non-streaming request..."
        make_request "$USER_MESSAGE"
        ;;
    *)
        echo "Usage: $0 [normal|stream|usage|custom \"message\"]"
        echo "  normal  - Make non-streaming request (interactive prompt) [default]"
        echo "  stream  - Make request via /chat (interactive prompt)"
        echo "  usage   - Check usage statistics"
        echo "  custom  - Make non-streaming request with provided message or interactive prompt"
        exit 1
        ;;
esac
