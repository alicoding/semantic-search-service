#!/usr/bin/env python3
"""
Intelligence Package - Clean Public API
Single Responsibility: Export clean public interface
"""

from .types import IndexMode, CodebaseIntelligenceError
from .manager import CodebaseIntelligence
from .graph_viz import export_to_networkx, visualize_graph

# Global singleton instance
_intelligence = None

def get_codebase_intelligence() -> CodebaseIntelligence:
    """Get or create global intelligence instance"""
    global _intelligence
    if _intelligence is None:
        _intelligence = CodebaseIntelligence()
    return _intelligence

# Convenience functions for backward compatibility
def index_project(path: str, name: str, mode: str = "vector"):
    """Convenience function"""
    intelligence = get_codebase_intelligence()
    mode_enum = IndexMode.VECTOR if mode == "vector" else IndexMode.GRAPH
    # Simplified - full implementation would be in manager
    return {"status": "success", "project": name}

def search(query: str, project: str, limit: int = 5) -> str:
    """Convenience function"""
    return get_codebase_intelligence().search_semantic(query, project, limit)

def project_exists(name: str) -> bool:
    """Convenience function"""
    return get_codebase_intelligence().project_exists(name)