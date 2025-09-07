#!/usr/bin/env python3
"""
Intelligence Resource Manager - Centralized Resource Layer
Single Responsibility: Manage shared intelligence resources (prevent duplicate API calls)
Pattern: Singleton resource manager for efficient resource sharing across components
"""

from typing import Dict, Any, Optional
from ..intelligence import get_codebase_intelligence, CodebaseIntelligence


class IntelligenceResourceManager:
    """
    Centralized intelligence resource manager
    Prevents duplicate API calls by sharing single intelligence instance
    """
    
    _instance: Optional['IntelligenceResourceManager'] = None
    _intelligence: Optional[CodebaseIntelligence] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def intelligence(self) -> CodebaseIntelligence:
        """Get shared intelligence instance (lazy initialization)"""
        if self._intelligence is None:
            self._intelligence = get_codebase_intelligence()
        return self._intelligence
    
    def search(self, query: str, project: str, limit: int = 5) -> str:
        """Centralized search to prevent duplicate calls"""
        return self.intelligence.search_semantic(query, project, limit)
    
    def project_exists(self, project: str) -> bool:
        """Centralized project check"""
        return self.intelligence.project_exists(project)
    
    def get_index(self, project: str, mode=None):
        """Centralized index access"""
        return self.intelligence.get_index(project, mode)
    
    def list_projects(self) -> list:
        """Centralized project listing"""
        return self.intelligence.list_projects()
    
    def get_project_info(self, project: str) -> Dict[str, Any]:
        """Centralized project info"""
        return self.intelligence.get_project_info(project)
    
    def check_component_exists(self, component: str, project: str) -> Dict[str, Any]:
        """Centralized component existence check"""
        return self.intelligence.check_component_exists(component, project)
    
    def clear_cache(self):
        """Clear internal caches if needed"""
        # Reset intelligence instance to force refresh
        self._intelligence = None


# Global instance for component sharing
_resource_manager = IntelligenceResourceManager()

def get_intelligence_resource() -> IntelligenceResourceManager:
    """Get shared intelligence resource manager"""
    return _resource_manager