#!/usr/bin/env python3
"""
Semantic Search Component - Semantic Domain Micro-Component
Single Responsibility: Wrapper for unified semantic search operations
Pattern: 30-50 LOC component using existing semantic_search facade
"""

from typing import Dict, Any, List, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class SemanticSearchComponent:
    """
    Semantic search using shared resources and existing facade
    Component Pattern: Small, focused wrapper around semantic_search.py
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def search(self, query: str, project: str, limit: int = 5) -> str:
        """Basic semantic search using existing facade"""
        from ...semantic_search import search
        return search(query, project, limit)
    
    def index_project(self, path: str, name: str) -> Dict[str, Any]:
        """Index project using existing facade"""
        from ...semantic_search import index_project
        return index_project(path, name)
    
    def check_exists(self, component: str, project: str) -> Dict[str, Any]:
        """Check component exists using existing facade"""
        from ...semantic_search import check_exists
        return check_exists(component, project)
    
    def find_violations(self, project: str) -> List[str]:
        """Find violations using existing facade"""
        from ...semantic_search import find_violations
        return find_violations(project)
    
    def suggest_libraries(self, task: str) -> str:
        """Suggest libraries using existing facade"""
        from ...semantic_search import suggest_libraries
        return suggest_libraries(task)


# Component factory for easy instantiation
def create_semantic_search() -> SemanticSearchComponent:
    """Create semantic search component with shared resources"""
    return SemanticSearchComponent()