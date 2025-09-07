#!/usr/bin/env python3
"""
Documentation Management Component - Documentation Domain Micro-Component
Single Responsibility: Manage framework documentation lifecycle  
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Dict, Any, List, Optional
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class DocumentationManagementComponent:
    """
    Documentation management using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def check_exists(self, component: str, framework: str = "llamaindex") -> Dict[str, Any]:
        """
        Fast existence check for components using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        collection_name = f"docs_{framework}"
        client = self.intelligence.intelligence.client
        
        if not client.collection_exists(collection_name):
            return {
                "exists": False,
                "error": f"Framework '{framework}' not indexed"
            }
        
        try:
            vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
            index = VectorStoreIndex.from_vector_store(vector_store)
            
            # Use retriever for fast checking
            retriever = index.as_retriever(similarity_top_k=1)
            nodes = retriever.retrieve(component)
            
            if nodes and nodes[0].score > 0.7:  # Confidence threshold
                return {
                    "exists": True,
                    "confidence": nodes[0].score,
                    "context": nodes[0].text[:500],
                    "framework": framework
                }
            
            return {
                "exists": False,
                "framework": framework,
                "message": f"Component '{component}' not found in {framework} docs"
            }
            
        except Exception as e:
            return {"exists": False, "error": str(e)}
    
    def list_frameworks(self) -> List[str]:
        """List all indexed documentation frameworks using shared client"""
        client = self.intelligence.intelligence.client
        collections = [c.name for c in client.get_collections().collections]
        return [c.replace('docs_', '') for c in collections if c.startswith('docs_')]
    
    def get_framework_info(self, framework: str) -> Dict[str, Any]:
        """Get information about an indexed framework using shared client"""
        collection_name = f"docs_{framework}"
        client = self.intelligence.intelligence.client
        
        if not client.collection_exists(collection_name):
            return {
                "framework": framework,
                "indexed": False,
                "error": "Not indexed"
            }
        
        collection = client.get_collection(collection_name)
        return {
            "framework": framework,
            "indexed": True,
            "documents": collection.points_count,
            "collection": collection_name
        }
    
    def refresh_docs(self, framework: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Refresh documentation using shared resources"""
        config = config or {}
        
        # Get framework config
        auto_index = config.get('auto_index', {})
        framework_config = auto_index.get(framework, {})
        
        if not framework_config.get('enabled', False):
            return {"error": f"Framework '{framework}' not enabled for indexing"}
        
        docs_url = framework_config.get('url')
        if not docs_url:
            return {"error": f"No URL configured for framework '{framework}'"}
        
        # Delegate to indexing component
        from .indexing import create_documentation_indexing
        indexing_component = create_documentation_indexing()
        return indexing_component.index_framework(framework, docs_url, config)


# Component factory for easy instantiation  
def create_documentation_management() -> DocumentationManagementComponent:
    """Create documentation management component with shared resources"""
    return DocumentationManagementComponent()