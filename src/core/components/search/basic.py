#!/usr/bin/env python3
"""
Basic Search Component - Search Domain Micro-Component
Single Responsibility: Execute basic semantic search operations
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class BasicSearchComponent:
    """
    Basic search operations using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def search(self, query: str, project: str, limit: int = 5) -> str:
        """
        Execute basic semantic search using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return f"Error: Project '{project}' not indexed"
        
        try:
            return self.intelligence.search(query, project, limit)
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def validate_project(self, project: str) -> bool:
        """Validate project exists using shared resource"""
        return self.intelligence.project_exists(project)
    
    def get_project_info(self, project: str) -> dict:
        """Get project information using shared resource"""
        return self.intelligence.get_project_info(project)


# Component factory for easy instantiation
def create_basic_search() -> BasicSearchComponent:
    """Create basic search component with shared resources"""
    return BasicSearchComponent()


# Backward compatibility functions
def search(query: str, project: str, limit: int = 5) -> str:
    """Backward compatible search function using component"""
    component = create_basic_search()
    return component.search(query, project, limit)