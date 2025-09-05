#!/usr/bin/env python3
"""
Context7 MCP Server - Thin wrapper
"""

from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP("Semantic Search")

# Import functions directly
from src.core import semantic_search

@mcp.tool()
def index_project(project_path: str, collection_name: Optional[str] = None) -> str:
    """Index a project for semantic search."""
    name = collection_name or Path(project_path).name
    semantic_search.index_project(project_path, name)
    return f"Indexed project '{name}'"

@mcp.tool()
def search_code(project_name: str, query: str, limit: int = 5) -> str:
    """Search for similar code patterns."""
    return semantic_search.search(query, project_name, limit)

@mcp.tool()
def find_violations(project_name: str) -> str:
    """Find SOLID/DRY/DDD violations."""
    violations = semantic_search.find_violations(project_name)
    return "\n".join(violations)

@mcp.tool()
def suggest_libraries(task: str) -> str:
    """Suggest libraries for a task."""
    return semantic_search.suggest_libraries(task)

@mcp.tool()
def check_exists(component: str, project: str) -> dict:
    """Check if a component exists in the indexed codebase."""
    return semantic_search.check_exists(component, project)

if __name__ == "__main__":
    mcp.run()