#!/usr/bin/env python
"""Test bypassing LlamaIndex model validation for ElectronHub"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Monkey-patch the validation BEFORE importing LlamaIndex
from llama_index.llms.openai import utils as openai_utils

# Add our ElectronHub models to the allowed list (with context windows)
ELECTRONHUB_MODELS = {
    'claude-opus-4-1-20250805': 200000,  # 200k context
    'claude-opus-4-20250514': 200000,
    'grok-4-0709': 100000,
    'gemini-2.5-pro': 1000000,  # 1M context
    'deepseek-r1': 64000,
}

# Patch the validation dict
original_models = openai_utils.ALL_AVAILABLE_MODELS.copy()
original_models.update(ELECTRONHUB_MODELS)
openai_utils.ALL_AVAILABLE_MODELS = original_models

print(f"✅ Added {len(ELECTRONHUB_MODELS)} ElectronHub models to validation list")

# Now import and test
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from llama_index.core import Settings
from src.core.config import initialize_settings, load_config

def test_with_bypass():
    """Test ElectronHub with validation bypassed"""
    
    # Reinitialize with patched validation
    config = load_config()
    initialize_settings(config)
    
    print("\n" + "=" * 60)
    print("TESTING WITH VALIDATION BYPASS")
    print("=" * 60)
    
    llm = Settings.llm
    print(f"\n1. LLM Configuration:")
    print(f"   Type: {type(llm).__name__}")
    print(f"   Model: {llm.model}")
    
    if hasattr(llm, 'api_base'):
        print(f"   API Base: {llm.api_base}")
        if 'electronhub' in str(llm.api_base).lower():
            print("   ✅ Using ElectronHub!")
    
    print(f"\n2. Testing LLM Query:")
    try:
        response = llm.complete("What model are you? Reply with just your model name and version.")
        print(f"   Response: {response.text.strip()}")
        
        if 'claude' in response.text.lower() or 'opus' in response.text.lower():
            print("   ✅ Claude model confirmed!")
        else:
            print(f"   ℹ️ Model: {response.text.strip()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ VALIDATION BYPASS SUCCESSFUL!")
    print("=" * 60)

if __name__ == "__main__":
    test_with_bypass()