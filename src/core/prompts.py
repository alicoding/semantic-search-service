#!/usr/bin/env python3
"""
Prompts loader - Centralized prompt management
Following OCP principle - extend via YAML, not code changes
"""

import yaml
from pathlib import Path
from typing import Dict, Any

# Load prompts once at module import
PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"

def load_prompts() -> Dict[str, Any]:
    """Load prompts from YAML - TRUE 95/5"""
    with open(PROMPTS_FILE, 'r') as f:
        return yaml.safe_load(f)

# Load once at import
PROMPTS = load_prompts()

def get_prompt(category: str, name: str, **kwargs) -> str:
    """Get a prompt by category and name with variable substitution"""
    prompt_template = PROMPTS.get(category, {}).get(name, "")
    return prompt_template.format(**kwargs) if kwargs else prompt_template

# Convenience functions for common prompts
def get_violation_prompt(check_type: str = "solid_check") -> str:
    """Get violation checking prompt"""
    return get_prompt("violations", check_type)

def get_suggestion_prompt(task: str, project_type: str = None) -> str:
    """Get library suggestion prompt"""
    if project_type:
        return get_prompt("library_suggestions", "with_context", task=task, project_type=project_type)
    return get_prompt("library_suggestions", "default", task=task)