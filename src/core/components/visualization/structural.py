#!/usr/bin/env python3
"""
Structural Diagram Component - Visualization Domain Micro-Component
Single Responsibility: Generate class and architecture diagrams
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

import json
from typing import Dict, Any, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class StructuralDiagramComponent:
    """
    Structural diagram generation using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def generate_class_diagram(self, project: str) -> Dict[str, Any]:
        """
        Generate class diagram structure using shared intelligence
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return {"error": f"Project '{project}' not indexed"}
        
        query = """
        Extract all classes and their relationships.
        Output as JSON:
        {
            "classes": [{"name": "ClassName", "methods": [], "attributes": []}],
            "relationships": [{"from": "ClassA", "to": "ClassB", "type": "inherits|uses|contains"}]
        }
        """
        
        try:
            response = self.intelligence.search(query, project)
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}
        except Exception as e:
            return {"error": str(e), "project": project}
    
    def generate_architecture_diagram(self, project: str) -> Dict[str, Any]:
        """
        Generate high-level architecture diagram using shared intelligence
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return {"error": f"Project '{project}' not indexed"}
        
        query = """
        Identify the main architectural components and their interactions.
        Output as JSON:
        {
            "components": [{"name": "component", "type": "service|module|database", "description": ""}],
            "connections": [{"from": "component1", "to": "component2", "protocol": "HTTP|gRPC|direct"}]
        }
        """
        
        try:
            response = self.intelligence.search(query, project)
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}
        except Exception as e:
            return {"error": str(e), "project": project}


# Component factory
def create_structural_diagram() -> StructuralDiagramComponent:
    """Create structural diagram component with shared resources"""
    return StructuralDiagramComponent()


# Backward compatibility functions
def generate_class_diagram(project: str) -> Dict[str, Any]:
    """Backward compatible class diagram using component"""
    component = create_structural_diagram()
    return component.generate_class_diagram(project)

def generate_architecture_diagram(project: str) -> Dict[str, Any]:
    """Backward compatible architecture diagram using component"""
    component = create_structural_diagram()
    return component.generate_architecture_diagram(project)