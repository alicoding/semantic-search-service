#!/usr/bin/env python3
"""
Prompt Resource Manager - Centralized Resource Layer
Single Responsibility: Manage shared prompt resources (prevent duplicate loading)
Pattern: Cached prompt manager for efficient prompt sharing across components
"""

from typing import Dict, Optional
from ..prompts import get_violation_prompt, get_suggestion_prompt


class PromptResourceManager:
    """
    Centralized prompt resource manager
    Prevents duplicate prompt loading by caching prompts
    """
    
    _instance: Optional['PromptResourceManager'] = None
    _prompt_cache: Dict[str, str] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._prompt_cache = {}
        return cls._instance
    
    def get_violation_prompt(self) -> str:
        """Get cached violation prompt"""
        if 'violation' not in self._prompt_cache:
            self._prompt_cache['violation'] = get_violation_prompt()
        return self._prompt_cache['violation']
    
    def get_suggestion_prompt(self, task: str) -> str:
        """Get suggestion prompt (dynamic, so not cached)"""
        return get_suggestion_prompt(task)
    
    def clear_cache(self):
        """Clear prompt cache if needed"""
        self._prompt_cache.clear()


# Global instance for component sharing
_prompt_manager = PromptResourceManager()

def get_prompt_resource() -> PromptResourceManager:
    """Get shared prompt resource manager"""
    return _prompt_manager