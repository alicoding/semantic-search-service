#!/usr/bin/env python3
"""
Core Types and Enums
Single Responsibility: Define data types and enums only
"""

from enum import Enum


class IndexMode(Enum):
    """Supported indexing modes"""
    VECTOR = "vector"
    GRAPH = "graph" 
    HYBRID = "hybrid"


class CodebaseIntelligenceError(Exception):
    """Base exception for codebase intelligence operations"""
    pass