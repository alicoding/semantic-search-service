#!/usr/bin/env python
"""Test direct OpenAI client with ElectronHub"""

import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create direct OpenAI client with ElectronHub
client = OpenAI(
    api_key=os.getenv("ELECTRONHUB_API_KEY"),
    base_url=os.getenv("ELECTRONHUB_BASE_URL"),
)

print("Testing direct OpenAI client with ElectronHub...")
print(f"Base URL: {client.base_url}")
print(f"API Key: {client.api_key[:10]}...")

try:
    # Make a test request
    response = client.chat.completions.create(
        model="claude-opus-4-1-20250805",
        messages=[
            {"role": "user", "content": "What model are you? Reply with just your model name."}
        ],
        max_tokens=50
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model used: {response.model}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")