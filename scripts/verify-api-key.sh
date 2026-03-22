#!/bin/bash

# Load GEMINI_API_KEY from .env
if [ -f .env ]; then
    # Careful with non-standard .env formats, but grep + xargs is what mingo-env.sh does
    export $(grep '^GEMINI_API_KEY=' .env | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY not found in .env"
    exit 1
fi

echo "Testing API key (first 4 chars: ${GEMINI_API_KEY:0:4})..."

curl -v https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{"text": "Write a short poem about a cat."}]
      }]
    }'
