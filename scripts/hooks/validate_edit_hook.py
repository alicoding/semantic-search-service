#!/usr/bin/env python3
"""
Validate Edit Hook - Prevents incomplete context and DRY violations
Runs before Edit/Write/MultiEdit to ensure proper research
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.core.semantic_search import search, check_exists
except ImportError as e:
    # Graceful fallback if imports fail
    print(f"Warning: Could not import search functions: {e}", file=sys.stderr)
    sys.exit(0)

def should_validate_edit(tool_name: str, tool_input: Dict[str, Any]) -> bool:
    """Check if this edit operation should be validated"""
    # Only validate file edits
    if tool_name not in ["Edit", "Write", "MultiEdit"]:
        return False
    
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return False
    
    # Skip validation for certain file types
    skip_extensions = [".md", ".txt", ".json", ".yaml", ".yml", ".log"]
    if any(file_path.endswith(ext) for ext in skip_extensions):
        return False
    
    return True

def validate_full_context(tool_name: str, tool_input: Dict[str, Any]) -> Optional[str]:
    """Validate that we have full file context for edits"""
    if tool_name == "Edit":
        old_string = tool_input.get("old_string", "")
        
        # Check for signs of incomplete context
        incomplete_indicators = [
            len(old_string) < 10,  # Very short old_string
            "..." in old_string,   # Truncation indicator
            "# TODO" in old_string,  # Placeholder code
        ]
        
        if any(incomplete_indicators):
            return "⚠️ Incomplete context detected. Consider reading the full file first to ensure proper understanding of the code structure."
    
    return None

def check_for_existing_implementations(tool_input: Dict[str, Any]) -> Optional[str]:
    """Check if similar implementations already exist"""
    file_path = tool_input.get("file_path", "")
    new_string = tool_input.get("new_string", "") or tool_input.get("content", "")
    
    if not new_string:
        return None
    
    # Extract function/class names from new code
    import re
    functions = re.findall(r'def\s+(\w+)', new_string)
    classes = re.findall(r'class\s+(\w+)', new_string)
    
    existing_implementations = []
    
    try:
        for func in functions:
            result = check_exists(func, "semantic-search-service")
            if result.get("exists", False):
                existing_implementations.append(f"Function '{func}' exists in {result.get('file', 'unknown')}")
        
        for cls in classes:
            result = check_exists(cls, "semantic-search-service")
            if result.get("exists", False):
                existing_implementations.append(f"Class '{cls}' exists in {result.get('file', 'unknown')}")
    
    except Exception as e:
        return f"Could not check existing implementations: {str(e)}"
    
    if existing_implementations:
        return "🔍 **Existing implementations found:**\n" + "\n".join(f"- {impl}" for impl in existing_implementations)
    
    return None

def main():
    """Main hook execution"""
    try:
        # Load input from Claude Code
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    if not should_validate_edit(tool_name, tool_input):
        sys.exit(0)  # No validation needed
    
    validation_messages = []
    
    # Check for incomplete context
    context_warning = validate_full_context(tool_name, tool_input)
    if context_warning:
        validation_messages.append(context_warning)
    
    # Check for existing implementations
    existing_impl = check_for_existing_implementations(tool_input)
    if existing_impl:
        validation_messages.append(existing_impl)
    
    if validation_messages:
        # Provide feedback to Claude but don't block the edit
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "\n\n".join(validation_messages)
            },
            "suppressOutput": False
        }
        
        print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()