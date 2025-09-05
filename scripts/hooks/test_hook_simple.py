#!/usr/bin/env python3
"""
Simple Hook Test - Test hook functionality without slow semantic search
"""

import json
import sys
import time

def main():
    """Test hook that responds quickly"""
    try:
        # Load input from Claude Code
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    hook_event = input_data.get("hook_event_name", "")
    
    if hook_event == "UserPromptSubmit":
        prompt = input_data.get("prompt", "")
        
        # Check for :research: trigger
        if ":research:" in prompt:
            context = f"""🔍 **Research Hook Triggered** (Test Mode)
            
**Prompt analyzed**: {prompt[:100]}...
**Performance**: Hook responded in ~5ms
**Status**: Semantic search disabled due to performance issues (>2min timeout)

**Next Steps**: 
- Optimize semantic search for <100ms response time
- Enable auto_research in config when performance improved
- Use explicit :research: trigger for now

_This is a test response to verify hook integration works._"""
            
            # Use JSON output to add context
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit", 
                    "additionalContext": context
                }
            }
            
            print(json.dumps(output))
    
    elif hook_event == "PreToolUse":
        tool_name = input_data.get("tool_name", "")
        
        if tool_name in ["Edit", "Write", "MultiEdit"]:
            # Simple validation message
            message = f"🔍 **Edit Validation Hook** - {tool_name} operation detected\n\nReminder: Ensure full file context before editing."
            
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow", 
                    "permissionDecisionReason": message
                }
            }
            
            print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()