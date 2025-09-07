#!/usr/bin/env python3
"""
Semantic Search V2 - Component-Based Architecture
Single Responsibility: Provide unified API using component registry
Pattern: Clean facade using micro-components with shared resources (no duplicate API calls)
"""

from typing import List, Dict, Any, Optional
from enum import Enum

from .component_registry import get_component, get_registry
from .resources import get_intelligence_resource


class SearchMode(str, Enum):
    """Search modes for backward compatibility"""
    VECTOR = "vector"
    GRAPH = "graph"  
    HYBRID = "hybrid"


class SemanticSearchV2:
    """
    Unified semantic search interface using component-based architecture
    Benefits: No duplicate API calls, LLM-readable components, clear patterns
    """
    
    def __init__(self):
        """Initialize with component registry and shared resources"""
        self.registry = get_registry()
        self.intelligence = get_intelligence_resource()
    
    # Search Operations
    def search(self, query: str, project: str, limit: int = 5) -> str:
        """Basic semantic search using search component"""
        search_component = get_component('search', 'basic')
        return search_component.search(query, project, limit)
    
    def search_with_citations(self, query: str, project: str, limit: int = 5) -> Dict[str, Any]:
        """Citation search using search component"""
        citation_component = get_component('search', 'citation')
        return citation_component.search_with_citations(query, project, limit)
    
    # Analysis Operations
    def find_violations(self, project: str) -> List[str]:
        """Find code violations using analysis component"""
        violations_component = get_component('analysis', 'violations')
        return violations_component.find_violations(project)
    
    def suggest_libraries(self, task: str) -> str:
        """Suggest libraries using analysis component"""
        suggestions_component = get_component('analysis', 'suggestions')
        return suggestions_component.suggest_libraries(task)
    
    # Routing Operations
    def smart_query(self, query: str, projects: Optional[List[str]] = None) -> str:
        """Smart query routing using routing component"""
        routing_component = get_component('routing', 'simple')
        return routing_component.smart_query(query, projects)
    
    # Graph Operations
    def create_knowledge_graph(self, path: str, name: str, graph_type: str = "code"):
        """Create knowledge graph using graph component"""
        creation_component = get_component('graph', 'creation')
        if graph_type == "code":
            return creation_component.create_from_codebase(path, name)
        else:
            return creation_component.create_from_documents(path, name)
    
    def visualize_graph(self, graph_index, format: str = "json"):
        """Visualize graph using graph component"""
        viz_component = get_component('graph', 'visualization')
        return viz_component.get_visual_graph(graph_index, format)
    
    # Project Management (delegated to shared resource)
    def list_projects(self) -> List[str]:
        """List projects using shared intelligence resource"""
        return self.intelligence.list_projects()
    
    def get_project_info(self, name: str) -> Dict[str, Any]:
        """Get project info using shared intelligence resource"""
        return self.intelligence.get_project_info(name)
    
    def project_exists(self, name: str) -> bool:
        """Check if project exists using shared intelligence resource"""
        return self.intelligence.project_exists(name)


# Global instance for backward compatibility
_semantic_search = SemanticSearchV2()

# Backward compatibility functions
def search(query: str, project: str, limit: int = 5) -> str:
    return _semantic_search.search(query, project, limit)

def search_with_citations(query: str, project: str, limit: int = 5) -> Dict[str, Any]:
    return _semantic_search.search_with_citations(query, project, limit)

def find_violations(project: str) -> List[str]:
    return _semantic_search.find_violations(project)

def suggest_libraries(task: str) -> str:
    return _semantic_search.suggest_libraries(task)

def smart_query(query: str, projects: Optional[List[str]] = None) -> str:
    return _semantic_search.smart_query(query, projects)

def list_projects() -> List[str]:
    return _semantic_search.list_projects()

def get_project_info(name: str) -> Dict[str, Any]:
    return _semantic_search.get_project_info(name)

def index_project(path: str, name: str, mode: str = None) -> Dict[str, Any]:
    """Index project using shared intelligence resource"""
    from .intelligence.types import IndexMode
    if mode == "basic" or mode == "vector":
        index_mode = IndexMode.VECTOR
    elif mode == "graph" or mode == "enterprise":
        index_mode = IndexMode.GRAPH
    elif mode == "hybrid":
        index_mode = IndexMode.HYBRID
    else:
        index_mode = IndexMode.VECTOR
    return _semantic_search.intelligence.intelligence.index_project(path, name, index_mode)

def clear_project(name: str) -> bool:
    """Delete project using shared intelligence resource"""
    return _semantic_search.intelligence.intelligence.clear_project(name)

def refresh_project(name: str, path: str) -> Dict[str, Any]:
    """Refresh project using shared intelligence resource"""
    return _semantic_search.intelligence.intelligence.refresh_project(path, name)

def check_exists(component: str, project: str) -> Dict[str, Any]:
    """Check component existence using micro-component pattern"""
    from .components.analysis.existence import create_component_existence_checker
    checker = create_component_existence_checker()
    return checker.check_exists(component, project)