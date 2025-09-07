#!/usr/bin/env python3
"""
Documentation Configuration - Micro-Component
Single Responsibility: Provide configuration access for docs components
Pattern: 20 LOC DIP-compliant configuration accessor
"""

from typing import Dict, Any
from ..config import load_config, get_qdrant_client, get_configured_reader


def get_docs_config() -> Dict[str, Any]:
    """Get documentation-specific configuration"""
    config = load_config()
    return config.get('documentation', {})


# Re-export core config functions for backward compatibility
# Following DIP: Don't create dependencies, expose them for injection
__all__ = [
    'get_docs_config',
    'get_qdrant_client', 
    'get_configured_reader',
    'CONFIG'
]

# Backward compatibility
CONFIG = load_config()