#!/usr/bin/env python3
"""
Sequence Diagram Component - Visualization Domain Micro-Component
Single Responsibility: Generate sequence diagrams from project graph data
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

import json
from typing import Dict, Any, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class SequenceDiagramComponent:
    """
    Sequence diagram generation using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def generate_native_sequence(self, project: str) -> Dict[str, Any]:
        """
        Generate sequence diagram using PropertyGraphIndex native visualization
        No duplicate API calls - uses centralized resource manager
        """
        if not self.intelligence.project_exists(project):
            return {"error": f"Project '{project}' not indexed"}
        
        try:
            # Get the PropertyGraphIndex via shared resource
            index = self.intelligence.get_index(project)
            
            # Native PropertyGraphIndex visualization pattern
            if hasattr(index, 'property_graph_store') and hasattr(index.property_graph_store, 'get_triplets'):
                triplets = index.property_graph_store.get_triplets()
                
                # Convert triplets to sequence diagram format
                sequence_data = []
                for i, triplet in enumerate(triplets[:20]):  # Limit for readability
                    sequence_data.append({
                        "source": triplet.subject.name if hasattr(triplet.subject, 'name') else str(triplet.subject),
                        "destination": triplet.object.name if hasattr(triplet.object, 'name') else str(triplet.object), 
                        "action": triplet.predicate if hasattr(triplet, 'predicate') else "interacts_with",
                        "order": i + 1
                    })
                
                return {
                    "project": project,
                    "sequence": sequence_data,
                    "format": "native_graph",
                    "diagram_type": "sequence",
                    "triplets_count": len(triplets)
                }
            else:
                return self._generate_fallback_sequence(project)
                
        except Exception as e:
            return {"error": str(e), "project": project}
    
    def _generate_fallback_sequence(self, project: str) -> Dict[str, Any]:
        """Fallback sequence generation using query-based approach"""
        query = """
        Analyze the codebase and extract the sequence of function calls and interactions.
        Output as JSON array with format:
        [{"source": "function_or_class", "destination": "called_function", "action": "method_name", "order": 1}]
        Focus on main execution flow and important interactions.
        """
        
        try:
            response = self.intelligence.search(query, project)
            sequence_data = json.loads(response)
            return {
                "project": project,
                "sequence": sequence_data,
                "format": "query_based",
                "diagram_type": "sequence"
            }
        except json.JSONDecodeError:
            return {
                "project": project,
                "sequence": response,
                "format": "text",
                "diagram_type": "sequence"
            }
        except Exception as e:
            return {"error": str(e), "project": project}


# Component factory
def create_sequence_diagram() -> SequenceDiagramComponent:
    """Create sequence diagram component with shared resources"""
    return SequenceDiagramComponent()