#!/usr/bin/env python3
"""
Citation Search Component - Search Domain Micro-Component
Single Responsibility: Execute citation-enhanced search operations
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Dict, Any, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class CitationSearchComponent:
    """
    Citation search operations using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def search_with_citations(self, query: str, project: str, limit: int = 5) -> Dict[str, Any]:
        """
        Execute citation search using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        from llama_index.core.query_engine import CitationQueryEngine
        
        if not self.intelligence.project_exists(project):
            return {"error": f"Project '{project}' not indexed"}
        
        try:
            # Get index from shared resource (no duplicate calls)
            index = self.intelligence.get_index(project)
            citation_engine = CitationQueryEngine(index.as_query_engine(similarity_top_k=limit))
            
            response = citation_engine.query(query)
            
            # Format citations
            citations = []
            if hasattr(response, 'source_nodes'):
                for i, node in enumerate(response.source_nodes, 1):
                    citations.append({
                        "citation_number": i,
                        "file": node.metadata.get('file_name', 'unknown'),
                        "score": node.score,
                        "text_preview": node.text[:200] + "..." if len(node.text) > 200 else node.text
                    })
            
            return {
                "answer": str(response),
                "citations": citations,
                "query": query,
                "project": project
            }
            
        except Exception as e:
            return {"error": str(e), "project": project}


# Component factory for easy instantiation
def create_citation_search() -> CitationSearchComponent:
    """Create citation search component with shared resources"""
    return CitationSearchComponent()


# Backward compatibility functions
def search_with_citations(query: str, project: str, limit: int = 5) -> Dict[str, Any]:
    """Backward compatible citation search function using component"""
    component = create_citation_search()
    return component.search_with_citations(query, project, limit)