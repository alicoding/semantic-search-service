#!/usr/bin/env python3
"""
Graph Visualization Functions
Single Responsibility: Handle graph visualization only
"""

from typing import Dict, Any


def export_to_networkx(project_name: str, intelligence) -> Dict[str, Any]:
    """Export PropertyGraphIndex to NetworkX format"""
    if not intelligence.project_exists(project_name):
        return {"error": f"Project '{project_name}' not indexed"}
    
    try:
        from .types import IndexMode
        import networkx as nx
        
        index = intelligence.get_index(project_name, IndexMode.GRAPH)
        if not hasattr(index, 'property_graph_store'):
            return {"error": "Project not using PropertyGraphIndex mode"}
        
        G = nx.DiGraph()
        graph_store = index.property_graph_store
        
        if hasattr(graph_store, 'get_triplets'):
            for triplet in graph_store.get_triplets():
                source = getattr(triplet.subject, 'name', str(triplet.subject))
                target = getattr(triplet.object, 'name', str(triplet.object))
                relation = getattr(triplet, 'predicate', 'related')
                
                G.add_edge(source, target, relation=relation)
        
        return {
            "networkx": G,
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "project": project_name
        }
        
    except ImportError:
        return {"error": "NetworkX not installed. Run: pip install networkx"}
    except Exception as e:
        return {"error": f"Failed to export: {str(e)}"}


def visualize_graph(project_name: str, intelligence) -> Dict[str, Any]:
    """Visualize PropertyGraphIndex"""
    if not intelligence.project_exists(project_name):
        return {"error": f"Project '{project_name}' not indexed"}
    
    try:
        from .types import IndexMode
        index = intelligence.get_index(project_name, IndexMode.GRAPH)
        
        if hasattr(index, 'property_graph_store'):
            graph_store = index.property_graph_store
            if hasattr(graph_store, 'visualize'):
                return graph_store.visualize()
        
        return {"error": "Visualization not available"}
    except Exception as e:
        return {"error": f"Failed to visualize: {str(e)}"}