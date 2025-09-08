#!/usr/bin/env python3
"""
Index Resource Manager - DRY pattern for index access
Single Responsibility: Manage index creation and access with native patterns
Pattern: 50-80 LOC resource manager for centralized index operations
"""

from llama_index.core import PropertyGraphIndex, VectorStoreIndex, StorageContext
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .qdrant_manager import get_qdrant_resource
from .config_manager import get_config_resource
from typing import Union, Dict, Any


class IndexResourceManager:
    """
    Index resource manager for centralized index operations
    Resource Pattern: Unified index access with mode switching
    """
    
    def __init__(self):
        """Initialize with resource managers"""
        self.qdrant = get_qdrant_resource()
        self.config = get_config_resource()
        self._graph_stores = {}  # Cache for graph stores
    
    def get_graph_index(self, collection_name: str) -> PropertyGraphIndex:
        """Get PropertyGraphIndex - ENTERPRISE mode with knowledge graphs"""
        client = self.qdrant.client
        
        # Get or create graph store
        if collection_name not in self._graph_stores:
            self._graph_stores[collection_name] = SimplePropertyGraphStore()
        
        # Setup vector store with Qdrant - Native LlamaIndex pattern with async support
        vector_store = QdrantVectorStore(
            client=client, 
            aclient=self.qdrant.async_client,  # NATIVE: Pass async client for full async support
            collection_name=collection_name,
            enable_hybrid=True
        )
        
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            property_graph_store=self._graph_stores[collection_name]
        )
        
        # Create PropertyGraphIndex
        return PropertyGraphIndex([], storage_context=storage_context, show_progress=True)
    
    def get_basic_index(self, collection_name: str) -> VectorStoreIndex:
        """Get basic VectorStoreIndex for simple vector search"""
        client = self.qdrant.client
        # Native LlamaIndex pattern: Pass both sync and async clients for full support
        vector_store = QdrantVectorStore(
            client=client, 
            aclient=self.qdrant.async_client,
            collection_name=collection_name
        )
        return VectorStoreIndex([], storage_context=StorageContext.from_defaults(vector_store=vector_store))
    
    def get_index(self, collection_name: str, mode: str = None) -> Union[PropertyGraphIndex, VectorStoreIndex]:
        """Get index based on mode - enterprise by default"""
        mode = mode or self.config.config.index_mode
        
        if mode in ['basic', 'vector']:
            return self.get_basic_index(collection_name)
        else:  # enterprise, graph, hybrid
            return self.get_graph_index(collection_name)
    
    def index_exists(self, collection_name: str) -> bool:
        """Check if index/collection exists"""
        return self.qdrant.client.collection_exists(collection_name)
    
    def get_graph_data(self, collection_name: str) -> Dict[str, Any]:
        """Get graph data for visualization"""
        if collection_name in self._graph_stores:
            store = self._graph_stores[collection_name]
            # Extract basic graph data (simplified for now)
            return {"nodes": [], "edges": [], "collection": collection_name}
        return {"error": f"No graph data found for {collection_name}"}
    
    def export_to_networkx(self, collection_name: str) -> Dict[str, Any]:
        """Export graph to NetworkX format using native LlamaIndex pattern"""
        try:
            index = self.get_graph_index(collection_name)
            # Native LlamaIndex one-liner for NetworkX export
            networkx_graph = index.get_networkx_graph()
            return {
                "success": True,
                "networkx": networkx_graph,
                "nodes": len(networkx_graph.nodes),
                "edges": len(networkx_graph.edges)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def visualize_graph(self, collection_name: str) -> Dict[str, Any]:
        """Visualize graph using native LlamaIndex + PyVis pattern"""
        try:
            index = self.get_graph_index(collection_name)
            # Native LlamaIndex one-liner
            g = index.get_networkx_graph()
            
            # Native visualization pattern with PyVis
            from pyvis.network import Network
            net = Network(notebook=False, cdn_resources="in_line", directed=True)
            net.from_nx(g)
            
            # Save to temp file
            import tempfile
            import os
            temp_file = os.path.join(tempfile.gettempdir(), f"{collection_name}_graph.html")
            net.show(temp_file)
            
            return {
                "success": True,
                "file_path": temp_file,
                "nodes": len(g.nodes),
                "edges": len(g.edges)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global index manager instance (singleton pattern)
_index_manager = None

def get_index_manager() -> IndexResourceManager:
    """Get global index resource manager (singleton)"""
    global _index_manager
    if _index_manager is None:
        _index_manager = IndexResourceManager()
    return _index_manager