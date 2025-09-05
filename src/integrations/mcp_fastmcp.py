#!/usr/bin/env python3
"""
MCP Server using FastMCP
Exposes documentation intelligence as MCP tools for Claude and other AI agents
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastmcp import FastMCP
from src.core.doc_intelligence import get_doc_intelligence
from src.core import semantic_search

# Initialize FastMCP server
mcp = FastMCP("semantic-search-intelligence")

# Get shared DocIntelligence instance
doc_intel = get_doc_intelligence()

# Documentation Intelligence Tools

@mcp.tool()
def get_pattern(query: str, framework: str = "llamaindex") -> str:
    """
    Get precise implementation pattern for a query.
    Returns 200-500 tokens of actual code pattern, not guesses.
    
    Args:
        query: What you want to implement (e.g., "RouterQueryEngine with custom selector")
        framework: The framework to search (e.g., "nextjs", "react", "llamaindex")
    
    Returns:
        Actual code pattern from documentation, not guessed syntax
    """
    return doc_intel.search_pattern(query, framework)

@mcp.tool()
def check_component_exists(component: str, framework: str = "llamaindex") -> dict:
    """
    Check if a component/function/class exists in framework documentation.
    Used by task-enforcer to determine if something needs to be created or updated.
    
    Args:
        component: Name of the component to check (e.g., "getServerSideProps")
        framework: The framework to check in
    
    Returns:
        Dict with exists (bool), confidence (float), and context (str)
    """
    return doc_intel.check_exists(component, framework)

@mcp.tool()
def index_framework_docs(framework: str, url: str = None) -> dict:
    """
    Index a framework's documentation for offline use.
    One-time operation or refresh.
    
    Args:
        framework: Name of the framework (e.g., "nextjs")
        url: Documentation URL to crawl (optional if in config)
    
    Returns:
        Dict with indexing results
    """
    return doc_intel.index_framework(framework, url)

@mcp.tool()
def list_indexed_frameworks() -> list:
    """
    List all frameworks that have been indexed.
    
    Returns:
        List of framework names
    """
    return doc_intel.list_frameworks()

@mcp.tool()
def get_framework_info(framework: str) -> dict:
    """
    Get information about an indexed framework.
    
    Args:
        framework: Name of the framework
    
    Returns:
        Dict with framework info including document count
    """
    return doc_intel.get_framework_info(framework)

# Semantic Search Tools (existing functionality)

@mcp.tool()
def search_code(query: str, project: str, limit: int = 5) -> str:
    """
    Search for code patterns in an indexed project.
    
    Args:
        query: Search query
        project: Project name
        limit: Maximum results to return
    
    Returns:
        Relevant code snippets
    """
    return semantic_search.search(query, project, limit)

@mcp.tool()
def index_project(path: str, name: str) -> dict:
    """
    Index a project for semantic search.
    
    Args:
        path: Path to the project
        name: Name for the collection
    
    Returns:
        Dict with indexing results
    """
    return semantic_search.index_project(path, name)

@mcp.tool()
def check_exists(component: str, project: str) -> dict:
    """
    Check if a component exists in a project (not documentation).
    Fast existence check for task-enforcer.
    
    Args:
        component: Component to search for
        project: Project name
    
    Returns:
        Dict with existence info
    """
    return semantic_search.check_exists(component, project)

@mcp.tool()
def find_violations(project: str) -> list:
    """
    Find SOLID/DRY/DDD violations in a project.
    Used by temporal-hooks for real-time violation detection.
    
    Args:
        project: Project name
    
    Returns:
        List of violations found
    """
    return semantic_search.find_violations(project)

@mcp.tool()
def suggest_libraries(task: str) -> str:
    """
    Suggest libraries for a specific task.
    
    Args:
        task: Description of what you want to accomplish
    
    Returns:
        Library suggestions
    """
    return semantic_search.suggest_libraries(task)

if __name__ == "__main__":
    # Run the MCP server
    # Use stdio for Claude Desktop integration
    mcp.run(transport="stdio")
    
    # For HTTP/SSE server (uncomment if needed):
    # import asyncio
    # asyncio.run(mcp.run_sse(port=8001))