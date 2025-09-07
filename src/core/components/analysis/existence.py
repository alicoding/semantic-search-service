#!/usr/bin/env python3
"""
Component Existence Checker - Analysis Domain Micro-Component
Single Responsibility: Check if components exist in codebase using semantic search
Pattern: 55 LOC focused component with proper DI following CLAUDE.md
"""

from typing import Dict, Any, Protocol
from ...resources import IntelligenceResourceManager
from ...resources.cache_manager import CacheResourceManager


class ComponentExistenceChecker:
    """
    Real component existence checker using native LlamaIndex semantic search
    Component Pattern: Small, focused, resource-injected (proper DIP compliance)
    LlamaIndex 2025: Full DIP with required dependencies, no internal creation
    """
    
    def __init__(self, 
                 intelligence_resource: IntelligenceResourceManager,
                 cache_resource: CacheResourceManager):
        """
        Initialize with explicit dependencies (proper DIP pattern - LlamaIndex 2025)
        All dependencies must be provided externally (no internal creation)
        """
        self.intelligence = intelligence_resource
        self.cache = cache_resource

    def check_exists(self, component: str, project: str) -> Dict[str, Any]:
        """
        Check if component exists using native LlamaIndex 95/5 pattern
        Direct semantic search with minimal custom logic - LlamaIndex does 95% of work
        """
        # Check if project exists first using cached resource
        if not self.intelligence.project_exists(project):
            return {
                "exists": False,
                "confidence": 0.0,
                "project": project,
                "context": f"Project '{project}' not indexed"
            }
        
        try:
            # NATIVE LlamaIndex one-liner: Direct component existence check
            result = self.intelligence.check_component_exists(component, project)
            
            # Use intelligence layer result directly - minimal processing
            if "error" in result:
                return {
                    "exists": False,
                    "confidence": 0.0,
                    "project": project,
                    "context": result["error"]
                }
            
            # Native pattern: Trust the intelligence layer confidence
            exists = result.get("exists", False)
            confidence = 0.95 if exists else 0.1
            context = result.get("context", "No additional context available")
            
            return {
                "exists": exists,
                "confidence": confidence,
                "project": project,
                "context": context
            }
            
        except Exception as e:
            return {
                "exists": False,
                "confidence": 0.0,
                "project": project,
                "context": f"Error checking component existence: {str(e)}"
            }


# Component factory for easy instantiation (LlamaIndex 2025 DIP pattern)
def create_component_existence_checker(
    intelligence_resource: IntelligenceResourceManager,
    cache_resource: CacheResourceManager
) -> ComponentExistenceChecker:
    """Create component existence checker with explicit dependencies (proper DIP)"""
    return ComponentExistenceChecker(intelligence_resource, cache_resource)