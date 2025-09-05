#!/usr/bin/env python3
"""
Index Helper - DRY pattern for index access
Enterprise by default with PropertyGraphIndex
Basic mode available when explicitly requested
"""

from llama_index.core import PropertyGraphIndex, StorageContext, Settings, VectorStoreIndex
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor, ImplicitPathExtractor
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client, CONFIG

# Global graph stores for enterprise mode
_graph_stores = {}

def get_graph_index(collection_name: str) -> PropertyGraphIndex:
    """
    Get PropertyGraphIndex - ENTERPRISE mode with knowledge graphs
    This is the DEFAULT for new projects
    """
    client = get_qdrant_client()
    
    # Get or create graph store
    if collection_name not in _graph_stores:
        _graph_stores[collection_name] = SimplePropertyGraphStore()
    
    # Setup vector store with Qdrant
    vector_store_kwargs = {
        'client': client, 
        'collection_name': collection_name
    }
    if CONFIG.get('enable_hybrid', False):
        vector_store_kwargs['enable_hybrid'] = True
    
    # Storage context with BOTH vector and graph stores
    storage_context = StorageContext.from_defaults(
        vector_store=QdrantVectorStore(**vector_store_kwargs),
        property_graph_store=_graph_stores[collection_name]
    )
    
    # Return PropertyGraphIndex for enterprise features
    return PropertyGraphIndex(
        nodes=[],
        storage_context=storage_context,
        show_progress=False
    )

def get_basic_index(collection_name: str) -> VectorStoreIndex:
    """
    Get VectorStoreIndex - BASIC mode for simple semantic search
    Use this only when explicitly needed for performance/simplicity
    """
    client = get_qdrant_client()
    
    vector_store_kwargs = {
        'client': client, 
        'collection_name': collection_name
    }
    if CONFIG.get('enable_hybrid', False):
        vector_store_kwargs['enable_hybrid'] = True
    
    return VectorStoreIndex.from_vector_store(
        QdrantVectorStore(**vector_store_kwargs)
    )

def get_index(collection_name: str, mode: str = None):
    """
    Get index based on mode configuration
    Default: Check config, fallback to 'basic' for existing collections without graphs
    """
    # Get mode from config or parameter
    if mode is None:
        mode = CONFIG.get('index_mode', 'auto')
    
    # Auto mode: Use graph for new, basic for existing
    if mode == 'auto':
        client = get_qdrant_client()
        if client.collection_exists(collection_name) and collection_name not in _graph_stores:
            # Existing collection without graph - use basic
            return get_basic_index(collection_name)
        else:
            # New or graph-enabled - use enterprise
            return get_graph_index(collection_name)
    elif mode == 'graph' or mode == 'enterprise':
        return get_graph_index(collection_name)
    else:  # 'basic' or fallback
        return get_basic_index(collection_name)

def index_exists(collection_name: str) -> bool:
    """Check if collection exists - one-liner"""
    return get_qdrant_client().collection_exists(collection_name)

def get_graph_data(collection_name: str) -> dict:
    """
    Get graph visualization data - Only works with enterprise mode
    Returns empty if collection not using graph mode
    """
    if collection_name not in _graph_stores:
        return {
            "error": "Collection not using graph mode",
            "hint": "Re-index with graph mode to enable visualization",
            "nodes": [],
            "edges": []
        }
    
    graph_store = _graph_stores[collection_name]
    # Get nodes and relationships from the graph store
    return {
        "nodes": graph_store.get_all_nodes() if hasattr(graph_store, 'get_all_nodes') else [],
        "edges": graph_store.get_all_relationships() if hasattr(graph_store, 'get_all_relationships') else [],
        "format": "native"
    }

def visualize_graph(collection_name: str):
    """
    Native ONE-LINER visualization using SimplePropertyGraphStore.visualize()
    Latest LlamaIndex pattern for 2024/2025
    """
    if collection_name not in _graph_stores:
        return {"error": "Collection not using graph mode"}
    
    # ONE-LINER: Native visualization as per latest docs
    return _graph_stores[collection_name].visualize()

def export_to_networkx(collection_name: str):
    """
    Export PropertyGraphIndex to NetworkX format
    Native LlamaIndex feature for graph analysis
    """
    if collection_name not in _graph_stores:
        return None
    
    try:
        import networkx as nx
        
        # Create NetworkX graph
        G = nx.DiGraph()  # Directed graph for relationships
        
        graph_store = _graph_stores[collection_name]
        
        # Add nodes if the store has them
        if hasattr(graph_store, '_graph_dict'):
            # Access internal graph structure
            for node_id, node_data in graph_store._graph_dict.items():
                G.add_node(node_id, **node_data)
        
        # Add edges if available
        if hasattr(graph_store, '_graph_dict_relations'):
            for source, targets in graph_store._graph_dict_relations.items():
                for relation, target in targets:
                    G.add_edge(source, target, relation=relation)
        
        # Export to various formats
        return {
            "networkx": G,
            "cytoscape": nx.cytoscape_data(G) if G.number_of_nodes() > 0 else None,
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "is_connected": nx.is_weakly_connected(G) if G.number_of_nodes() > 0 else False
        }
    except ImportError:
        return {"error": "NetworkX not installed. Run: pip install networkx"}
    except Exception as e:
        return {"error": f"Failed to export: {str(e)}"}