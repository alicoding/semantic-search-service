#!/usr/bin/env python
"""Test that ElectronHub is actually being used for LLM queries"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llama_index.core import Settings
from src.core.config import initialize_settings, load_config

def test_electronhub_config():
    """Test that ElectronHub is configured correctly"""
    
    # Reinitialize to ensure latest config
    config = load_config()
    initialize_settings(config)
    
    print("=" * 60)
    print("TESTING ELECTRONHUB INTEGRATION")
    print("=" * 60)
    
    # Check environment variables
    electronhub_key = os.getenv("ELECTRONHUB_API_KEY")
    electronhub_base = os.getenv("ELECTRONHUB_BASE_URL")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print("\n1. Environment Variables:")
    print(f"   ELECTRONHUB_API_KEY: {'✅ Set' if electronhub_key else '❌ Not set'}")
    print(f"   ELECTRONHUB_BASE_URL: {electronhub_base if electronhub_base else '❌ Not set'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    
    # Check LLM configuration
    print("\n2. LLM Configuration:")
    llm = Settings.llm
    print(f"   Type: {type(llm).__name__}")
    print(f"   Model: {llm.model if hasattr(llm, 'model') else 'N/A'}")
    
    if hasattr(llm, 'api_base'):
        print(f"   API Base: {llm.api_base}")
        if 'electronhub' in str(llm.api_base).lower():
            print("   ✅ Using ElectronHub!")
        else:
            print("   ⚠️ Using OpenAI directly")
    
    # Check Embedding configuration
    print("\n3. Embedding Configuration:")
    embed = Settings.embed_model
    print(f"   Type: {type(embed).__name__}")
    if hasattr(embed, 'model_name'):
        print(f"   Model: {embed.model_name}")
    elif hasattr(embed, 'model'):
        print(f"   Model: {embed.model}")
    
    # Make a test query to verify it works
    print("\n4. Testing LLM Query:")
    try:
        response = llm.complete("What model are you? Reply with just your model name.")
        print(f"   Response: {response.text.strip()}")
        
        # Check if response indicates Claude Opus
        if 'claude' in response.text.lower() or 'opus' in response.text.lower():
            print("   ✅ Claude Opus 4.1 confirmed!")
        elif 'gpt' in response.text.lower():
            print("   ⚠️ Still using GPT model")
        else:
            print(f"   ℹ️ Model identified as: {response.text.strip()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("CONFIGURATION SUMMARY")
    print("=" * 60)
    
    # Read config.yaml to show what's configured
    print("\nFrom config.yaml:")
    print(f"  openai_model: {config.get('openai_model')}")
    print(f"  openai_embed_model: {config.get('openai_embed_model')}")
    print(f"  llm_provider: {config.get('llm_provider')}")
    print(f"  embed_provider: {config.get('embed_provider')}")
    
    # Final verdict
    print("\n" + "=" * 60)
    if electronhub_key and electronhub_base and hasattr(llm, 'api_base') and 'electronhub' in str(llm.api_base).lower():
        print("✅ ELECTRONHUB INTEGRATION: ACTIVE")
        print(f"   Using model: {config.get('openai_model')}")
    else:
        print("❌ ELECTRONHUB INTEGRATION: NOT ACTIVE")
        print("   Check .env file and config.yaml")

if __name__ == "__main__":
    test_electronhub_config()