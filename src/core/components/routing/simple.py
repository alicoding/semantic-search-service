#!/usr/bin/env python3
"""
Simple Routing Component - Routing Domain Micro-Component
Single Responsibility: Simple query routing across projects
Pattern: 50-80 LOC component with injected shared resources (no duplicate API calls)
"""

from typing import List, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class SimpleRoutingComponent:
    """
    Simple query routing using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def smart_query(self, query: str, projects: Optional[List[str]] = None) -> str:
        """
        Smart query routing using shared intelligence resource
        No duplicate API calls - uses centralized resource manager
        """
        if projects is None:
            projects = self.intelligence.list_projects()
        
        router = self.create_router(projects)
        if not router:
            return "No indexed projects available"
        
        try:
            response = router.query(query)
            return str(response)
        except Exception as e:
            return f"Error during routing: {str(e)}"
    
    def create_router(self, projects: List[str]):
        """Create RouterQueryEngine using shared intelligence resource"""
        from llama_index.core.query_engine import RouterQueryEngine
        from llama_index.core.selectors import PydanticSingleSelector
        from llama_index.core.tools import QueryEngineTool
        
        tools = []
        for project in projects:
            if self.intelligence.project_exists(project):
                # Determine project type for descriptions
                is_docs = project.startswith('docs_')
                is_conversation = 'conversation' in project or 'memory' in project
                
                if is_docs:
                    description = f"Documentation for {project.replace('docs_', '')} library. Use for API references, examples, and how-to guides."
                elif is_conversation:
                    description = f"Conversation history and decisions from {project}. Use for past context and decisions."
                else:
                    description = f"Source code for {project} project. Use for code analysis, implementations, and technical details."
                
                try:
                    # Get index from shared resource (no duplicate calls)
                    index = self.intelligence.get_index(project)
                    tool = QueryEngineTool.from_defaults(
                        query_engine=index.as_query_engine(),
                        description=description,
                        name=project
                    )
                    tools.append(tool)
                except Exception as e:
                    print(f"Warning: Could not create tool for project {project}: {e}")
        
        if not tools:
            return None
        
        return RouterQueryEngine(
            selector=PydanticSingleSelector.from_defaults(),
            query_engine_tools=tools,
            verbose=True
        )


# Component factory for easy instantiation
def create_simple_routing() -> SimpleRoutingComponent:
    """Create simple routing component with shared resources"""
    return SimpleRoutingComponent()


# Backward compatibility functions
def smart_query(query: str, projects: Optional[List[str]] = None) -> str:
    """Backward compatible smart query function using component"""
    component = create_simple_routing()
    return component.smart_query(query, projects)

def create_router(projects: List[str]):
    """Backward compatible router creation using component"""
    component = create_simple_routing()
    return component.create_router(projects)