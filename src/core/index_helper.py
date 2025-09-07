#!/usr/bin/env python3
"""
TEMPORARY SHIM: index_helper compatibility layer
This file exists only to prevent import errors during migration.
All functionality has been moved to resources/index_manager.py
"""

from .resources.index_manager import get_index_manager

# Create shared manager instance
_manager = get_index_manager()

# Export functions for backward compatibility
get_index = _manager.get_index
index_exists = _manager.index_exists
export_to_networkx = _manager.export_to_networkx
visualize_graph = _manager.visualize_graph

# TODO: Remove this compatibility shim after all imports are updated