#!/usr/bin/env python3
"""
FastAPI Dependencies - 2025 Native Dependency Injection Patterns
Single Responsibility: Provide shared dependencies using native FastAPI DI
Pattern: Stateless dependency injection with resource manager sharing
"""

from typing import Generator
from src.core.resources import (
    get_cache_manager, get_index_manager, get_intelligence_resource,
    get_llm_resource, get_qdrant_resource
)
from src.core.resources.cache_manager import CacheResourceManager
from src.core.resources.index_manager import IndexResourceManager
from src.core.resources.intelligence_manager import IntelligenceResourceManager
from src.core.resources.llm_selector import LLMSelectionResourceManager
from src.core.resources.qdrant_manager import QdrantResourceManager


# Native FastAPI dependency injection using resource managers
def get_cache_dependency() -> CacheResourceManager:
    """Get cache resource manager dependency"""
    return get_cache_manager()


def get_index_dependency() -> IndexResourceManager:
    """Get index resource manager dependency"""
    return get_index_manager()


def get_intelligence_dependency() -> IntelligenceResourceManager:
    """Get intelligence resource manager dependency"""
    return get_intelligence_resource()


def get_llm_dependency() -> LLMSelectionResourceManager:
    """Get LLM resource manager dependency"""
    return get_llm_resource()


def get_qdrant_dependency() -> QdrantResourceManager:
    """Get Qdrant resource manager dependency"""
    return get_qdrant_resource()


# Composite dependencies for common patterns
def get_search_dependencies() -> dict:
    """Get common search dependencies as a dict for convenience"""
    return {
        "index_manager": get_index_manager(),
        "intelligence": get_intelligence_resource(),
        "cache": get_cache_manager()
    }