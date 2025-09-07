#!/usr/bin/env python3
"""
Library Suggestions Component - Analysis Domain Micro-Component
Single Responsibility: Suggest libraries for specific tasks
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Optional
from ...resources import get_llm_resource, get_prompt_resource
from ...resources import LLMResourceManager, PromptResourceManager


class LibrarySuggestionsComponent:
    """
    Library suggestions analysis using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, 
                 llm_resource: Optional[LLMResourceManager] = None,
                 prompt_resource: Optional[PromptResourceManager] = None):
        """
        Initialize with shared resource managers
        Uses singletons if none provided (prevents duplicate resources)
        """
        self.llm = llm_resource or get_llm_resource()
        self.prompts = prompt_resource or get_prompt_resource()
    
    def suggest_libraries(self, task: str) -> str:
        """
        Suggest libraries for task using shared LLM and prompt resources
        No duplicate API calls - uses centralized resource managers
        """
        try:
            # Use shared prompt resource to get suggestion prompt
            prompt = self.prompts.get_suggestion_prompt(task)
            
            # Use shared LLM resource (cached connection)
            return self.llm.complete(prompt)
            
        except Exception as e:
            return f"Error generating suggestions: {str(e)}"
    
    def suggest_with_context(self, task: str, context: str = "") -> str:
        """
        Enhanced suggestions with additional context
        """
        try:
            enhanced_task = f"{task}\nContext: {context}" if context else task
            prompt = self.prompts.get_suggestion_prompt(enhanced_task)
            return self.llm.complete(prompt)
            
        except Exception as e:
            return f"Error generating contextual suggestions: {str(e)}"


# Component factory for easy instantiation
def create_library_suggestions() -> LibrarySuggestionsComponent:
    """Create library suggestions component with shared resources"""
    return LibrarySuggestionsComponent()


# Backward compatibility functions
def suggest_libraries(task: str) -> str:
    """Backward compatible suggestions function using component"""
    component = create_library_suggestions()
    return component.suggest_libraries(task)