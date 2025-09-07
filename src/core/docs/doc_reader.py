#!/usr/bin/env python3
"""
Documentation Reader - Documentation Domain
Single Responsibility: Create specialized readers for documentation generation
"""

from llama_index.core import SimpleDirectoryReader


def get_multi_language_reader(project_path: str) -> SimpleDirectoryReader:
    """Get configured reader with multi-language support for documentation"""
    # Focus on code files only for performance - exclude docs/config for speed
    code_extensions = [
        ".py", ".js", ".ts", ".tsx", ".jsx",  # Python, JavaScript, TypeScript
        ".java", ".go", ".rs", ".cpp", ".c", ".cs",  # Java, Go, Rust, C/C++, C#
        ".php", ".rb", ".swift", ".kt", ".scala"  # PHP, Ruby, Swift, Kotlin, Scala
    ]
    
    return SimpleDirectoryReader(
        input_dir=project_path,
        recursive=True,
        required_exts=code_extensions,
        exclude=["__pycache__", ".git", "venv", ".venv", "node_modules", "target", "build", "dist",
                "storage", "docs", "tests", "test", "spec"]  # Exclude large dirs for speed
    )