#!/usr/bin/env python3
"""
Research Hook - Configurable semantic search integration for Claude Code
Prevents hallucination and DRY violations through automatic research
"""

import json
import sys
import time
import re
import os
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.core.semantic_search import search, check_exists, find_violations
    from src.core.redis_cache import query_cache
except ImportError as e:
    # Graceful fallback if imports fail
    print(f"Warning: Could not import search functions: {e}", file=sys.stderr)
    sys.exit(0)

# Default configuration
DEFAULT_CONFIG = {
    "enabled": True,
    "auto_research": True,
    "explicit_trigger": ":research:",
    "performance_threshold": 100,  # milliseconds
    "cache_enabled": True,
    "coding_keywords": ["implement", "create", "add", "fix", "build", "write", "make", "setup", "configure"],
    "debug": False
}

def load_config() -> Dict[str, Any]:
    """Load research hook configuration"""
    # Try to load from CLAUDE.md or use defaults
    claude_md_path = project_root / "CLAUDE.md"
    config = DEFAULT_CONFIG.copy()
    
    if claude_md_path.exists():
        try:
            with open(claude_md_path, 'r') as f:
                content = f.read()
                # Simple extraction of research_hooks config (could be enhanced)
                if "research_hooks:" in content:
                    # For now, use defaults - could parse YAML section later
                    pass
        except Exception:
            pass
    
    return config

def hash_prompt_intent(prompt: str) -> str:
    """Create a hash key for similar prompts to enable caching"""
    # Extract key coding concepts for caching
    coding_words = []
    for word in DEFAULT_CONFIG["coding_keywords"]:
        if word in prompt.lower():
            coding_words.append(word)
    
    # Simple intent hash - could be enhanced with embedding similarity
    intent = "_".join(sorted(coding_words))
    return f"research_intent:{intent}"

def has_coding_keywords(prompt: str) -> bool:
    """Check if prompt contains coding-related keywords"""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in DEFAULT_CONFIG["coding_keywords"])

def can_research_fast(prompt: str, threshold_ms: int) -> bool:
    """Test if research can be done within performance threshold"""
    cache_key = hash_prompt_intent(prompt)
    
    # Check if we have cached results
    if query_cache.get(cache_key, "research_cache"):
        return True  # Cache hit = super fast
    
    # Quick estimation - if index is "warm" and prompt is simple
    # For now, be conservative
    return False

def perform_research(prompt: str, project_name: str = "semantic-search-service") -> Dict[str, Any]:
    """Perform semantic search research on the prompt"""
    start_time = time.time()
    research_results = {}
    
    try:
        # Extract key concepts for searching
        search_query = extract_search_terms(prompt)
        
        if search_query:
            # Semantic search for existing implementations
            search_results = search(search_query, project_name, limit=3)
            research_results["search"] = search_results
            
            # Check for component existence
            components = extract_components(prompt)
            for comp in components:
                exists_result = check_exists(comp, project_name)
                research_results[f"exists_{comp}"] = exists_result
            
            # Check for violations if implementing something new
            if any(word in prompt.lower() for word in ["create", "implement", "add"]):
                violations = find_violations(project_name)
                research_results["violations"] = violations[:3]  # Top 3 violations
        
        # Cache results for future use
        cache_key = hash_prompt_intent(prompt)
        query_cache.set(cache_key, "research_cache", research_results)
        
    except Exception as e:
        research_results["error"] = str(e)
    
    research_results["timing_ms"] = int((time.time() - start_time) * 1000)
    return research_results

def extract_search_terms(prompt: str) -> str:
    """Extract key terms for semantic search"""
    # Simple extraction - could be enhanced with NLP
    terms = []
    
    # Look for "implement X", "create Y", etc.
    patterns = [
        r"implement (\w+)",
        r"create (\w+)",
        r"add (\w+)",
        r"fix (\w+)",
        r"build (\w+)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, prompt, re.IGNORECASE)
        terms.extend(matches)
    
    return " ".join(terms) if terms else prompt.split()[:5]  # First 5 words as fallback

def extract_components(prompt: str) -> list:
    """Extract component names to check for existence"""
    # Look for capitalized words that might be component names
    components = re.findall(r'\b[A-Z]\w+(?:Service|Handler|Manager|Controller|API|Endpoint)\b', prompt)
    return components[:3]  # Limit to 3 components

def should_research(prompt: str, config: Dict[str, Any]) -> Tuple[bool, str]:
    """Determine if research should be performed based on prompt and config"""
    
    if not config.get("enabled", True):
        return False, "disabled"
    
    # Explicit trigger always wins
    trigger = config.get("explicit_trigger", ":research:")
    if trigger in prompt:
        return True, "explicit"
    
    # Auto-research if enabled
    if config.get("auto_research", False):
        if has_coding_keywords(prompt):
            threshold = config.get("performance_threshold", 100)
            if can_research_fast(prompt, threshold):
                return True, "auto_cached"
            else:
                return True, "auto_uncached"  # Still do it, but note it might be slow
    
    return False, "skipped"

def format_research_context(research_results: Dict[str, Any]) -> str:
    """Format research results into context for Claude"""
    context_parts = []
    
    context_parts.append("🔍 **Automatic Research Results:**")
    
    if "search" in research_results:
        context_parts.append(f"**Existing implementations found:**\n{research_results['search']}")
    
    # Component existence checks
    for key, value in research_results.items():
        if key.startswith("exists_"):
            comp_name = key.replace("exists_", "")
            exists = value.get("exists", False)
            status = "✅ EXISTS" if exists else "❌ NOT FOUND"
            context_parts.append(f"**{comp_name}**: {status}")
            if exists and "file" in value:
                context_parts.append(f"  Found in: {value['file']}")
    
    if "violations" in research_results:
        context_parts.append("**⚠️ Current violations to avoid:**")
        for violation in research_results["violations"]:
            context_parts.append(f"- {violation}")
    
    if "timing_ms" in research_results:
        timing = research_results["timing_ms"]
        context_parts.append(f"_Research completed in {timing}ms_")
    
    return "\n\n".join(context_parts)

def main():
    """Main hook execution"""
    try:
        # Load input from Claude Code
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    prompt = input_data.get("prompt", "")
    if not prompt:
        sys.exit(0)
    
    # Load configuration
    config = load_config()
    
    # Determine if research should be performed
    should_do_research, reason = should_research(prompt, config)
    
    if config.get("debug", False):
        print(f"Research decision: {should_do_research} (reason: {reason})", file=sys.stderr)
    
    if not should_do_research:
        sys.exit(0)  # No research needed
    
    # Perform research
    research_results = perform_research(prompt)
    
    # Format results as additional context
    if research_results and not research_results.get("error"):
        context = format_research_context(research_results)
        
        # Check if research took too long
        timing = research_results.get("timing_ms", 0)
        if timing > config.get("performance_threshold", 100):
            context += f"\n\n⚠️ Research took {timing}ms (above {config['performance_threshold']}ms threshold)"
        
        # Use JSON output to add context
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context
            },
            "suppressOutput": False  # Show in transcript for debugging
        }
        
        print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()