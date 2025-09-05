#!/usr/bin/env python3
"""
Diagram Generator - TRUE Native PropertyGraphIndex 2025 Patterns
Generate native visualizations using PropertyGraphIndex graph structure
Real native patterns, not text generation
"""

from .index_helper import get_index, index_exists
from llama_index.core import SimpleDirectoryReader, PropertyGraphIndex
from pathlib import Path
import json
from typing import Dict, Any, Optional

def generate_native_sequence_diagram(project: str) -> Dict[str, Any]:
    """
    Generate sequence diagram using PropertyGraphIndex native visualization - TRUE 2025 pattern
    Uses actual graph structure, not text generation
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    # Get the PropertyGraphIndex to access graph structure
    index = get_index(project)
    
    # Native PropertyGraphIndex visualization pattern
    if hasattr(index, 'property_graph_store') and hasattr(index.property_graph_store, 'get_triplets'):
        # Extract actual graph triplets (native pattern)
        triplets = index.property_graph_store.get_triplets()
        
        # Convert triplets to sequence diagram format
        sequence_data = []
        for i, triplet in enumerate(triplets[:20]):  # Limit to first 20 for readability
            sequence_data.append({
                "source": triplet.subject.name if hasattr(triplet.subject, 'name') else str(triplet.subject),
                "destination": triplet.object.name if hasattr(triplet.object, 'name') else str(triplet.object), 
                "action": triplet.predicate if hasattr(triplet, 'predicate') else "interacts_with",
                "order": i + 1
            })
        
        # Generate Mermaid sequence diagram from native graph
        mermaid_diagram = generate_mermaid_from_graph(sequence_data)
        
        return {
            "project": project,
            "sequence": sequence_data,
            "mermaid": mermaid_diagram,
            "format": "native_graph",
            "diagram_type": "sequence",
            "triplets_count": len(triplets)
        }
    else:
        # Fallback to query-based approach
        return generate_sequence_diagram_fallback(project)

def generate_mermaid_from_graph(sequence_data: list) -> str:
    """Convert native graph structure to Mermaid sequence diagram - TRUE native pattern"""
    if not sequence_data:
        return "sequenceDiagram\n    Note right of System: No interactions found"
    
    mermaid = "sequenceDiagram\n"
    
    # Extract unique participants
    participants = set()
    for item in sequence_data:
        participants.add(item["source"])
        participants.add(item["destination"])
    
    # Add participant declarations
    for participant in sorted(participants):
        clean_name = participant.replace(" ", "_").replace("-", "_")[:20]
        mermaid += f"    participant {clean_name}\n"
    
    # Add interactions
    mermaid += "\n"
    for item in sequence_data:
        source = item["source"].replace(" ", "_").replace("-", "_")[:20]
        dest = item["destination"].replace(" ", "_").replace("-", "_")[:20]
        action = item["action"][:30]  # Limit action length
        mermaid += f"    {source}->>{dest}: {action}\n"
    
    return mermaid

def generate_sequence_diagram_fallback(project: str) -> Dict[str, Any]:
    """
    Fallback sequence diagram generation using query analysis
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    # Query-based approach for sequence extraction
    query = """
    Analyze the codebase and extract the sequence of function calls and interactions.
    Output as JSON array with format:
    [{"source": "function_or_class", "destination": "called_function", "action": "method_name", "order": 1}]
    Focus on main execution flow and important interactions.
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    try:
        # Try to parse as JSON
        sequence_data = json.loads(str(response))
        return {
            "project": project,
            "sequence": sequence_data,
            "format": "query_based",
            "diagram_type": "sequence"
        }
    except json.JSONDecodeError:
        # Return as text if JSON parsing fails
        return {
            "project": project,
            "sequence": str(response),
            "format": "text",
            "diagram_type": "sequence"
        }

def generate_sequence_diagram(project: str) -> Dict[str, Any]:
    """
    Main sequence diagram generator - uses native patterns first
    """
    # Try native PropertyGraphIndex visualization first
    native_result = generate_native_sequence_diagram(project)
    if "error" not in native_result:
        return native_result
    
    # Fallback to analysis-based generation
    return generate_sequence_diagram_fallback(project)

def generate_mermaid_diagram(project: str) -> str:
    """
    Generate Mermaid.js sequence diagram - TRUE 95/5 pattern
    Returns Mermaid syntax that can be rendered
    """
    if not index_exists(project):
        return f"Error: Project '{project}' not indexed"
    
    # Query for Mermaid format directly
    query = """
    Generate a Mermaid.js sequence diagram for the main execution flow.
    Start with 'sequenceDiagram' and use proper Mermaid syntax.
    Focus on the most important interactions.
    Example format:
    sequenceDiagram
        participant A as ClassA
        participant B as ClassB
        A->>B: method_call()
        B-->>A: return result
    """
    
    response = get_index(project).as_query_engine().query(query)
    return str(response)

def generate_plantuml_diagram(project: str) -> str:
    """
    Generate PlantUML sequence diagram - TRUE 95/5 pattern
    Returns PlantUML syntax
    """
    if not index_exists(project):
        return f"Error: Project '{project}' not indexed"
    
    query = """
    Generate a PlantUML sequence diagram for the codebase.
    Start with @startuml and end with @enduml.
    Use proper PlantUML syntax for sequence diagrams.
    """
    
    response = get_index(project).as_query_engine().query(query)
    return str(response)

def generate_class_diagram(project: str) -> Dict[str, Any]:
    """
    Generate class diagram structure - TRUE 95/5 pattern
    Returns JSON with class relationships
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    query = """
    Extract all classes and their relationships.
    Output as JSON:
    {
        "classes": [{"name": "ClassName", "methods": [], "attributes": []}],
        "relationships": [{"from": "ClassA", "to": "ClassB", "type": "inherits|uses|contains"}]
    }
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    try:
        return json.loads(str(response))
    except json.JSONDecodeError:
        return {"raw_response": str(response)}

def generate_architecture_diagram(project: str) -> Dict[str, Any]:
    """
    Generate high-level architecture diagram - TRUE 95/5 pattern
    Returns component structure
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    query = """
    Identify the main architectural components and their interactions.
    Output as JSON:
    {
        "components": [{"name": "component", "type": "service|module|database", "description": ""}],
        "connections": [{"from": "component1", "to": "component2", "protocol": "HTTP|gRPC|direct"}]
    }
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    try:
        return json.loads(str(response))
    except json.JSONDecodeError:
        return {"raw_response": str(response)}