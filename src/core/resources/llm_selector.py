#!/usr/bin/env python3
"""
LLM Selection Resource Manager - Centralized Resource Layer  
Single Responsibility: Manage LLM model selection logic (prevent duplicate selection code)
Pattern: Singleton resource manager for intelligent LLM routing across components
"""

from typing import Optional
from llama_index.core import Settings
from .config_manager import get_config_resource


class LLMSelectionResourceManager:
    """
    Centralized LLM selection resource manager
    Prevents duplicate selection logic by sharing intelligent routing
    """
    
    _instance: Optional['LLMSelectionResourceManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_llm(self, task_type: str = "fast"):
        """
        Get appropriate LLM for task type - TRUE 95/5 principle
        
        Args:
            task_type: "fast" (default), "complex", or "complex_alt"
        
        Returns:
            Appropriate LLM instance for the task
        """
        # Ensure settings are initialized
        config_manager = get_config_resource()
        config_manager.initialize_settings()
        
        if task_type == "complex":
            return getattr(Settings, 'llm_complex', Settings.llm)
        elif task_type == "complex_alt": 
            return getattr(Settings, 'llm_complex_alt', Settings.llm)
        else:  # "fast" or default
            return getattr(Settings, 'llm_fast', Settings.llm)
    
    def should_use_complex_model(self, task_description: str) -> str:
        """
        Determine if task needs complex model - Native pattern
        
        Args:
            task_description: Description of the task
            
        Returns:
            "fast", "complex", or "complex_alt"
        """
        # Complex reasoning indicators
        complex_keywords = [
            "analyze", "reasoning", "planning", "workflow", "business logic",
            "architecture", "design patterns", "violations", "entity extraction",
            "relationships", "graph", "property graph", "code analysis"
        ]
        
        # Simple task indicators  
        simple_keywords = [
            "search", "find", "get", "list", "health", "status", "exists",
            "simple", "basic", "quick", "fast", "documentation", "function signatures"
        ]
        
        task_lower = task_description.lower()
        
        # Check for simple tasks first
        if any(keyword in task_lower for keyword in simple_keywords):
            return "fast"
        
        # Check for complex tasks
        if any(keyword in task_lower for keyword in complex_keywords):
            return "complex"
        
        # Default to fast model (cost optimization)
        return "fast"
    
    def get_smart_llm(self, task_description: str):
        """Get LLM based on intelligent task analysis"""
        task_type = self.should_use_complex_model(task_description)
        return self.get_llm(task_type)
    
    def complete(self, prompt: str, llm_type: str = "fast") -> str:
        """
        Centralized LLM completion - backward compatibility method
        Consolidates functionality from old LLMResourceManager
        """
        llm = self.get_llm(llm_type)
        return str(llm.complete(prompt))
    
    def clear_cache(self):
        """Clear any internal caches - backward compatibility method"""
        # LLM selection doesn't maintain cache currently, but method exists for compatibility
        pass


# Global instance for component sharing
_llm_selector = LLMSelectionResourceManager()

def get_llm_selector_resource() -> LLMSelectionResourceManager:
    """Get shared LLM selection resource manager"""
    return _llm_selector