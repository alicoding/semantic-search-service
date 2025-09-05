#!/usr/bin/env python3
"""
SessionStart Hook - Inject Living Document Context
TRUE 95/5 Pattern: Just reads pre-generated document
"""

import json
import sys
from pathlib import Path

def main():
    """Inject living document as session context"""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    if input_data.get("hook_event_name") != "SessionStart":
        sys.exit(0)
    
    # Read living document if it exists
    living_doc_path = Path(".claude/living_document.md")
    
    if living_doc_path.exists():
        try:
            with open(living_doc_path, 'r') as f:
                living_doc = f.read()
            
            # Add timestamp and context info
            context = f"""📄 **Living Document Context** (Auto-injected on SessionStart)

{living_doc}

---
*This context was automatically generated from the current codebase state.*
*Use :research: in prompts for additional targeted semantic search.*
*Hooks configured: UserPromptSubmit, PreToolUse, PreCompact, SessionStart*
"""
            
            # Return as additional context
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }
            
            print(json.dumps(output))
            
        except Exception as e:
            print(f"Warning: Could not read living document: {e}", file=sys.stderr)
    else:
        # No living document - create one first
        print("📄 No living document found - will generate on next PreCompact", file=sys.stderr)
    
    sys.exit(0)

if __name__ == "__main__":
    main()