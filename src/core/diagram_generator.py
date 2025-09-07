#!/usr/bin/env python3
"""
Diagram Generator API - Component-Based Architecture
Single Responsibility: Unified API for all diagram generation using micro-components
Pattern: 50-80 LOC API delegating to domain components (no duplicate API calls)
"""

from typing import Dict, Any
from .components.visualization.sequence import create_sequence_diagram
from .components.visualization.mermaid import create_mermaid_diagram
from .components.visualization.plantuml import create_plantuml_diagram
from .components.visualization.structural import create_structural_diagram


# Main API functions using component delegation
def generate_sequence_diagram(project: str) -> Dict[str, Any]:
    """Generate sequence diagram using sequence component"""
    component = create_sequence_diagram()
    return component.generate_native_sequence(project)

def generate_mermaid_diagram(project: str) -> str:
    """Generate Mermaid.js diagram using mermaid component"""
    component = create_mermaid_diagram()
    return component.generate_sequence_diagram(project)

def generate_plantuml_diagram(project: str) -> str:
    """Generate PlantUML diagram using plantuml component"""
    component = create_plantuml_diagram()
    return component.generate_sequence_diagram(project)

def generate_class_diagram(project: str) -> Dict[str, Any]:
    """Generate class diagram using structural component"""
    component = create_structural_diagram()
    return component.generate_class_diagram(project)

def generate_architecture_diagram(project: str) -> Dict[str, Any]:
    """Generate architecture diagram using structural component"""
    component = create_structural_diagram()
    return component.generate_architecture_diagram(project)

# Legacy compatibility - delegates to mermaid component
def generate_mermaid_from_graph(sequence_data: list) -> str:
    """Legacy compatibility function for mermaid generation"""
    from .components.visualization.mermaid import generate_mermaid_from_graph
    return generate_mermaid_from_graph(sequence_data)

# Legacy compatibility - delegates to sequence component fallback
def generate_native_sequence_diagram(project: str) -> Dict[str, Any]:
    """Legacy compatibility function for native sequence generation"""
    return generate_sequence_diagram(project)