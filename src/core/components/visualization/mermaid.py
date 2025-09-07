#!/usr/bin/env python3
"""
Mermaid Diagram Component - Visualization Domain Micro-Component
Single Responsibility: Generate Mermaid.js format diagrams
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Optional, List, Dict, Any
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class MermaidDiagramComponent:
    """
    Mermaid diagram generation using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def generate_from_graph(self, sequence_data: List[Dict[str, Any]]) -> str:
        """Convert native graph structure to Mermaid sequence diagram"""
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
    
    def generate_sequence_diagram(self, project: str) -> str:
        """
        Generate Mermaid.js sequence diagram using shared intelligence
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return f"Error: Project '{project}' not indexed"
        
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
        
        try:
            return self.intelligence.search(query, project)
        except Exception as e:
            return f"Error generating Mermaid diagram: {str(e)}"


# Component factory
def create_mermaid_diagram() -> MermaidDiagramComponent:
    """Create mermaid diagram component with shared resources"""
    return MermaidDiagramComponent()


# Backward compatibility functions
def generate_mermaid_from_graph(sequence_data: List[Dict[str, Any]]) -> str:
    """Backward compatible mermaid generation using component"""
    component = create_mermaid_diagram()
    return component.generate_from_graph(sequence_data)

def generate_mermaid_diagram(project: str) -> str:
    """Backward compatible mermaid diagram using component"""
    component = create_mermaid_diagram()
    return component.generate_sequence_diagram(project)