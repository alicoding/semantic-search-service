#!/usr/bin/env python3
"""
PlantUML Diagram Component - Visualization Domain Micro-Component
Single Responsibility: Generate PlantUML format diagrams
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class PlantUMLDiagramComponent:
    """
    PlantUML diagram generation using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def generate_sequence_diagram(self, project: str) -> str:
        """
        Generate PlantUML sequence diagram using shared intelligence
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return f"Error: Project '{project}' not indexed"
        
        query = """
        Generate a PlantUML sequence diagram for the codebase.
        Start with @startuml and end with @enduml.
        Use proper PlantUML syntax for sequence diagrams.
        """
        
        try:
            return self.intelligence.search(query, project)
        except Exception as e:
            return f"Error generating PlantUML diagram: {str(e)}"


# Component factory
def create_plantuml_diagram() -> PlantUMLDiagramComponent:
    """Create PlantUML diagram component with shared resources"""
    return PlantUMLDiagramComponent()


# Backward compatibility functions
def generate_plantuml_diagram(project: str) -> str:
    """Backward compatible PlantUML generation using component"""
    component = create_plantuml_diagram()
    return component.generate_sequence_diagram(project)