#!/usr/bin/env python3
"""
PreCompact Hook - TRUE 95/5 Pattern
Uses existing API to generate living document
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Generate living document using our existing API"""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    if input_data.get("hook_event_name") != "PreCompact":
        sys.exit(0)
    
    # Use our existing overview API - TRUE 95/5!
    try:
        result = subprocess.run([
            "curl", "-s", "-X", "POST", 
            "http://localhost:8000/analyze/overview",
            "-H", "Content-Type: application/json",
            "-d", '{"project_path": ".", "include": ["structure", "violations", "patterns"]}'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            api_data = json.loads(result.stdout)
            
            # Format as living document
            living_doc = f"""# Semantic Search Service - Living Document
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🏗️ Project Structure (Native API)
{api_data.get('structure', 'Structure unavailable')}

## 🎯 Detected Patterns
{chr(10).join(f'- {p}' for p in api_data.get('patterns', ['No patterns detected']))}

## ⚠️ Code Analysis
{chr(10).join(f'- {v}' for v in api_data.get('violations', ['No violations found']))}

## 📄 Important Files
{chr(10).join(f'**{k}**: {", ".join(v) if v else "None"}' for k, v in api_data.get('important_files', {}).items())}

---
*Generated via native API endpoint /analyze/overview*
*TRUE 95/5 Pattern: API does the work, hook just calls it*
"""
            
            # Save living document
            living_doc_path = Path(".claude/living_document.md")
            living_doc_path.parent.mkdir(exist_ok=True)
            
            with open(living_doc_path, 'w') as f:
                f.write(living_doc)
            
            print(f"✅ Living document generated: {len(living_doc)} chars", file=sys.stderr)
        else:
            print("❌ API call failed", file=sys.stderr)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
    
    sys.exit(0)

if __name__ == "__main__":
    main()