#!/usr/bin/env python3
"""
MCP Server - 2025 Micro-Component Architecture
Single Responsibility: MCP transport layer only (zero business logic)
Pattern: Ultra-thin FastMCP using semantic_search facade (80 lines total)
"""

from pathlib import Path
import sys
import os
import logging
from typing import Dict, Any

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
os.chdir(project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from fastmcp import FastMCP

# Import the unified facade (contains all business logic)
from src.core import semantic_search, doc_search

# Initialize FastMCP server
mcp = FastMCP("semantic-search-intelligence")

# Initialize settings
try:
    logger.info("Initializing MCP server...")
    from src.core.config import initialize_settings, load_config
    config = load_config()
    initialize_settings(config)
    logger.info("MCP server initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize MCP server: {e}")
    raise

# === ULTRA-THIN MCP TOOLS (1-2 lines each) ===

@mcp.tool()
def get_pattern(query: str, framework: str = "llamaindex") -> str:
    """Get implementation pattern - pure transport wrapper"""
    return doc_search.search_docs(query, framework, examples_only=True)

@mcp.tool()
def check_component_exists(component: str, framework: str = "llamaindex") -> dict:
    """Check component existence - pure transport wrapper"""
    return semantic_search.check_exists(component, framework)

@mcp.tool()
def index_framework_docs(framework: str, url: str = None) -> dict:
    """Index framework docs - pure transport wrapper"""
    return doc_search.index_library_docs(framework, url or f"docs_{framework}")

@mcp.tool()
def list_indexed_frameworks() -> list:
    """List frameworks - pure transport wrapper"""
    return doc_search.list_indexed_docs()

@mcp.tool()
def search_code(query: str, project: str, limit: int = 5) -> str:
    """Search code - pure transport wrapper"""
    return semantic_search.search(query, project, limit)

@mcp.tool()
def index_project(path: str, name: str) -> dict:
    """Index project - pure transport wrapper"""
    return semantic_search.index_project(path, name)

@mcp.tool()
def find_violations(project: str) -> list:
    """Find violations - pure transport wrapper"""
    return semantic_search.find_violations(project)

@mcp.tool()
def suggest_libraries(task: str) -> str:
    """Suggest libraries - pure transport wrapper"""
    return semantic_search.suggest_libraries(task)

@mcp.tool()
def index_docs_url(url: str, collection_name: str) -> dict:
    """Index docs from URL - uses existing doc_search facade"""
    return doc_search.index_library_docs(collection_name, url)

@mcp.tool()
def query_docs(collection_name: str, query: str) -> dict:
    """Query docs - uses existing doc_search facade"""
    return {"result": doc_search.search_docs(query, collection_name)}

@mcp.tool()
def index_github_docs(repo: str, collection_name: str) -> dict:
    """Index GitHub docs - uses existing doc_search facade"""
    return doc_search.index_library_docs(collection_name, f"github:{repo}")

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")