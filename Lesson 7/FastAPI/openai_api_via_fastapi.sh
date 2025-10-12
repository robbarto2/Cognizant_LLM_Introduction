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

# Normalize temperature input (e.g., '.9' -> '0.9') so it's valid JSON number
normalize_temp() {
    local t="$1"
    # trim leading/trailing whitespace
    t="${t##+([[:space:]])}"
    t="${t%%+([[:space:]])}"
    if [[ "$t" =~ ^\.[0-9]+$ ]]; then
        echo "0$t"
    else
        echo "$t"
    fi
}

# Function to make request to FastAPI (non-streaming)
make_streaming_request() {
    local message="$1"
    local temperature="$2"
    local payload_message
    payload_message=$(json_escape "$message")
    
    local payload
    payload=$(printf '{"messages":[{"role":"user","content":"%s"}],"model":"%s","temperature":%s,"stream":false,"user_id":"%s"}' \
        "$payload_message" "${OPENAI_MODEL:-gpt-4o-mini}" "$temperature" "$USER_ID")

    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

# Function to make non-streaming request to FastAPI
make_request() {
    local message="$1"
    local temperature="$2"
    local payload_message
    payload_message=$(json_escape "$message")
    
    local payload
    payload=$(printf '{"messages":[{"role":"user","content":"%s"}],"model":"%s","temperature":%s,"stream":false,"user_id":"%s"}' \
        "$payload_message" "${OPENAI_MODEL:-gpt-4o-mini}" "$temperature" "$USER_ID")

    curl "${FASTAPI_BASE_URL}/chat" \
        -H "Content-Type: application/json" \
        -d "$payload"
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
        read -rp "Enter temperature (0.5-1.0) [default 0.9]: " USER_TEMP
        USER_TEMP=${USER_TEMP:-0.9}
        USER_TEMP=$(normalize_temp "$USER_TEMP")
        make_streaming_request "$USER_MESSAGE" "$USER_TEMP"
        ;;
    "normal")
        echo "Making normal request..."
        read -rp "Enter your prompt: " USER_MESSAGE
        read -rp "Enter temperature (0.5-1.0) [default 0.9]: " USER_TEMP
        USER_TEMP=${USER_TEMP:-0.9}
        USER_TEMP=$(normalize_temp "$USER_TEMP")
        make_request "$USER_MESSAGE" "$USER_TEMP"
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
        read -rp "Enter temperature (0.5-1.0) [default 0.9]: " USER_TEMP
        USER_TEMP=${USER_TEMP:-0.9}
        USER_TEMP=$(normalize_temp "$USER_TEMP")
        echo "Making custom non-streaming request..."
        make_request "$USER_MESSAGE" "$USER_TEMP"
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
