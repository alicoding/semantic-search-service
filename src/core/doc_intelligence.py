#!/usr/bin/env python3
"""
Documentation Intelligence V2 - Component-Based Architecture
Single Responsibility: Provide unified documentation intelligence API using component registry
Pattern: Clean facade using micro-components with shared resources (no duplicate API calls)
"""

from typing import Dict, Any, List, Optional
from .component_registry import get_component
from .resources import get_intelligence_resource


class DocIntelligenceV2:
    """
    Unified documentation intelligence interface using component-based architecture
    Benefits: No duplicate API calls, LLM-readable components, clear patterns
    """
    
    def __init__(self):
        """Initialize with component registry and shared resources"""
        self.intelligence = get_intelligence_resource()
    
    def index_framework(self, framework: str, docs_url: Optional[str] = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Index framework documentation using indexing component"""
        indexing_component = get_component('documentation', 'indexing')
        return indexing_component.index_framework(framework, docs_url, config or {})
    
    def search_pattern(self, query: str, framework: str = "llamaindex", config: Dict[str, Any] = None) -> str:
        """Search for precise implementation patterns using search component"""
        search_component = get_component('documentation', 'search')
        return search_component.search_pattern(query, framework, config or {})
    
    def check_exists(self, component: str, framework: str = "llamaindex") -> Dict[str, Any]:
        """Check if component exists using management component"""
        management_component = get_component('documentation', 'management')
        return management_component.check_exists(component, framework)
    
    def refresh_docs(self, framework: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Refresh documentation using management component"""
        management_component = get_component('documentation', 'management')
        return management_component.refresh_docs(framework, config or {})
    
    def list_frameworks(self) -> List[str]:
        """List all indexed frameworks using management component"""
        management_component = get_component('documentation', 'management')
        return management_component.list_frameworks()
    
    def get_framework_info(self, framework: str) -> Dict[str, Any]:
        """Get framework information using management component"""
        management_component = get_component('documentation', 'management')
        return management_component.get_framework_info(framework)


# Global instance for backward compatibility  
_doc_intelligence = DocIntelligenceV2()

# Backward compatibility functions
def get_doc_intelligence() -> DocIntelligenceV2:
    """Get or create the global DocIntelligence instance"""
    return _doc_intelligence

def index_framework(framework: str, docs_url: Optional[str] = None) -> Dict[str, Any]:
    """Backward compatible function"""
    return _doc_intelligence.index_framework(framework, docs_url)

def search_pattern(query: str, framework: str = "llamaindex") -> str:
    """Backward compatible function"""
    return _doc_intelligence.search_pattern(query, framework)

def check_exists(component: str, framework: str = "llamaindex") -> Dict[str, Any]:
    """Backward compatible function"""
    return _doc_intelligence.check_exists(component, framework)

def list_frameworks() -> List[str]:
    """Backward compatible function"""
    return _doc_intelligence.list_frameworks()

def get_framework_info(framework: str) -> Dict[str, Any]:
    """Backward compatible function"""
    return _doc_intelligence.get_framework_info(framework)