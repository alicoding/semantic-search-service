#!/usr/bin/env python3
"""
Resource Layer - Centralized Resource Management
Single Responsibility: Provide shared resources to prevent duplicate API calls
Pattern: Resource managers for efficient sharing across micro-components
"""

# Resource managers following 2025 DRY consolidation patterns
from .intelligence_manager import get_intelligence_resource, IntelligenceResourceManager
from .prompt_manager import get_prompt_resource, PromptResourceManager
from .config_manager import get_config_resource, ConfigurationResourceManager
from .qdrant_manager import get_qdrant_resource, QdrantResourceManager
from .llm_selector import get_llm_selector_resource, LLMSelectionResourceManager
from .cache_manager import get_cache_manager, CacheResourceManager
from .index_manager import get_index_manager, IndexResourceManager

# CONSOLIDATED: Use llm_selector as the single LLM resource (eliminates DRY violation)
# Backward compatibility alias for components still using old interface
get_llm_resource = get_llm_selector_resource
LLMResourceManager = LLMSelectionResourceManager

__all__ = [
    'get_intelligence_resource', 'IntelligenceResourceManager',
    'get_llm_resource', 'LLMResourceManager',  # Alias to llm_selector 
    'get_llm_selector_resource', 'LLMSelectionResourceManager',
    'get_prompt_resource', 'PromptResourceManager',
    'get_config_resource', 'ConfigurationResourceManager',
    'get_qdrant_resource', 'QdrantResourceManager',
    'get_cache_manager', 'CacheResourceManager',
    'get_index_manager', 'IndexResourceManager'
]