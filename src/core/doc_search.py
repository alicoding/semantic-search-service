#!/usr/bin/env python3
"""
Documentation Search - Context7 Tamer
Indexes library documentation for semantic search without context overload
NO INHERITANCE - Direct function calls only
"""

from typing import Dict, Any, List
from .semantic_search import index_project, search, list_projects, get_project_info

def index_library_docs(library_name: str, docs_path: str) -> Dict[str, Any]:
    """Index library documentation into dedicated collection."""
    collection_name = f"docs_{library_name.lower().replace('-', '_')}"
    return index_project(docs_path, collection_name)

def search_docs(query: str, library: str, examples_only: bool = False) -> str:
    """Search library documentation with Context7 routing - TRUE 95/5"""
    from .config import CONFIG
    
    # Get routing config
    routing = CONFIG.get('documentation', {}).get('routing', {})
    route_type = routing.get(library.lower(), routing.get('default', 'indexed'))
    
    # Context7 routing for configured libraries (native MCP integration)  
    if route_type == 'context7' and library.lower() == 'react':
        # Context7 integration placeholder - would use MCP in production
        # For now, return indication that Context7 routing is configured
        return f"🔄 Context7 routing configured for React queries: '{query}'\n\nThis would fetch from /reactjs/react.dev with latest React documentation and code examples.\n\nTo fully implement: configure MCP Context7 server connection."
    
    # Local indexed search (default)
    collection_name = f"docs_{library.lower().replace('-', '_')}"
    
    # Enhance query for better code example retrieval
    if examples_only:
        query = f"{query} code example implementation"
    
    return search(query, collection_name, limit=3)

def how_to(task: str, library: str) -> str:
    """Get specific implementation pattern for a task."""
    query = f"How to {task} with code example step by step implementation"
    result = search_docs(query, library, examples_only=True)
    
    # Simple formatting
    return f"# How to {task} in {library}\n\n{result}\n\n## Next Steps\n1. Copy the code example above\n2. Adapt to your specific use case\n3. Test the implementation"

def compare_libraries(task: str, libraries: List[str]) -> Dict[str, str]:
    """Compare how different libraries handle the same task."""
    comparisons = {}
    for library in libraries:
        collection_name = f"docs_{library.lower().replace('-', '_')}"
        if collection_name in list_projects():
            comparisons[library] = how_to(task, library)
        else:
            comparisons[library] = f"Library {library} not indexed yet"
    return comparisons

def list_indexed_docs() -> List[str]:
    """List all indexed documentation libraries."""
    # Filter for doc collections only
    all_projects = list_projects()
    return [p.replace('docs_', '') for p in all_projects if p.startswith('docs_')]

def get_library_info(library: str) -> Dict[str, Any]:
    """Get information about indexed library documentation."""
    collection_name = f"docs_{library.lower().replace('-', '_')}"
    return get_project_info(collection_name)

# Total: ~68 LOC (SRP compliant - no CLI mixing)
# NO INHERITANCE - just function composition
# NO EMBEDDING COMPLEXITY - Settings handles everything