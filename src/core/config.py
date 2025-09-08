#!/usr/bin/env python3
"""
Configuration V2 - Component-Based Architecture
Single Responsibility: Provide unified configuration API using resource managers
Pattern: Clean facade using resource managers with shared resources (no duplicate loading)
"""

from typing import Optional, Dict, Any
from .resources.config_manager import get_config_resource
from .resources.qdrant_manager import get_qdrant_resource
from .resources.llm_selector import get_llm_selector_resource


# Resource managers for shared access
_config_resource = get_config_resource()
_qdrant_resource = get_qdrant_resource()
_llm_selector_resource = get_llm_selector_resource()

# Initialize settings on import
_config_resource.initialize_settings()

# Backward compatibility functions using resource managers
def load_config() -> Dict[str, Any]:
    """Load configuration using shared resource manager"""
    return _config_resource.config

def initialize_settings(config: Optional[Dict[str, Any]] = None) -> None:
    """Initialize LlamaIndex Settings using shared resource manager"""
    _config_resource.initialize_settings(config)

def get_qdrant_client():
    """Get Qdrant client using shared resource manager"""
    return _qdrant_resource.client

def get_async_qdrant_client():
    """Get async Qdrant client using shared resource manager"""
    return _qdrant_resource.async_client

def close_qdrant_client():
    """Close Qdrant client using shared resource manager"""
    _qdrant_resource.close_client()

def get_collection_name(project: str) -> str:
    """Get collection name using shared resource manager"""
    return _qdrant_resource.get_collection_name(project)

def get_configured_reader(path: str, filename_as_id: bool = False):
    """Get configured reader using shared resource manager"""
    return _config_resource.get_configured_reader(path, filename_as_id)

def get_llm(task_type: str = "fast"):
    """Get LLM using shared resource manager"""
    return _llm_selector_resource.get_llm(task_type)

def should_use_complex_model(task_description: str) -> str:
    """Determine model complexity using shared resource manager"""
    return _llm_selector_resource.should_use_complex_model(task_description)

# Export config as dict for backward compatibility with .get() calls
CONFIG = _config_resource.config.model_dump()