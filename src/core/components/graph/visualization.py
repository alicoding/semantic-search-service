#!/usr/bin/env python3
"""
Graph Visualization Component - Graph Domain Micro-Component
Single Responsibility: Generate visual representations of knowledge graphs
Pattern: 50-80 LOC component focused on graph visualization formats
"""

from typing import Dict, Any, Optional


class GraphVisualizationComponent:
    """
    Knowledge graph visualization operations
    Component Pattern: Small, focused, stateless visualization logic
    """
    
    def __init__(self):
        """Initialize visualization component (stateless)"""
        pass
    
    def get_visual_graph(self, graph_index, format: str = "json") -> Dict[str, Any]:
        """
        Get visual representation of the knowledge graph
        Supports multiple formats: json, cytoscape, mermaid, jupyter
        """
        if not graph_index:
            return {"error": "No graph index provided"}
        
        # Get the property graph store
        graph_store = graph_index.property_graph_store
        
        if format == "jupyter":
            # For Jupyter notebooks - native visualization
            try:
                return graph_store.show_jupyter_graph()
            except:
                return {"error": "Not in Jupyter environment"}
        
        elif format == "cytoscape":
            # For web visualization (Cytoscape.js format)
            return self._format_cytoscape(graph_store)
        
        elif format == "mermaid":
            # Generate Mermaid diagram
            return self._format_mermaid(graph_store)
        
        else:
            # Raw JSON format
            return {
                "nodes": graph_store.get_nodes(),
                "edges": graph_store.get_edges(),
                "format": "json"
            }
    
    def _format_cytoscape(self, graph_store) -> Dict[str, Any]:
        """Format graph data for Cytoscape.js visualization"""
        nodes = []
        edges = []
        
        # Extract nodes
        for node_id, node_data in graph_store.get_nodes().items():
            nodes.append({
                "data": {
                    "id": node_id,
                    "label": node_data.get("label", node_id),
                    "type": node_data.get("type", "unknown"),
                    **node_data
                }
            })
        
        # Extract edges
        for edge in graph_store.get_edges():
            edges.append({
                "data": {
                    "source": edge["source"],
                    "target": edge["target"],
                    "label": edge.get("relation", "related"),
                    **edge
                }
            })
        
        return {
            "elements": {"nodes": nodes, "edges": edges},
            "format": "cytoscape"
        }
    
    def _format_mermaid(self, graph_store) -> Dict[str, Any]:
        """Format graph data for Mermaid diagram"""
        mermaid = ["graph TD"]
        
        for edge in graph_store.get_edges():
            source = edge["source"].replace(" ", "_")
            target = edge["target"].replace(" ", "_")
            relation = edge.get("relation", "-->")
            mermaid.append(f"    {source}[{edge['source']}] {relation} {target}[{edge['target']}]")
        
        return {
            "diagram": "\n".join(mermaid),
            "format": "mermaid"
        }


# Component factory for easy instantiation
def create_graph_visualization() -> GraphVisualizationComponent:
    """Create graph visualization component"""
    return GraphVisualizationComponent()