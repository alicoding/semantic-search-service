#!/usr/bin/env python3
"""
Auto-Docs Setup Integration - Hook Installation Service
95/5 Pattern: Creates minimal git hooks that delegate to our semantic-search service
Single Responsibility: Install git hooks for external projects (claude-parser, lnla-hooks)
"""

from pathlib import Path
from typing import Dict, Any
import subprocess
import os


class AutoDocsSetupService:
    """Service for setting up auto-docs git hooks in external projects"""
    
    def __init__(self, service_url: str = "http://localhost:8000"):
        self.service_url = service_url
    
    def setup_project_hooks(self, project_path: str) -> Dict[str, Any]:
        """
        Setup git hooks for auto-docs and violation detection
        95/5 Pattern: Creates minimal hooks that delegate everything to our service
        """
        project_path = Path(project_path).resolve()
        
        if not project_path.exists():
            return {"success": False, "error": f"Project path not found: {project_path}"}
        
        git_dir = project_path / ".git"
        if not git_dir.exists():
            return {"success": False, "error": f"Not a git repository: {project_path}"}
        
        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        project_name = project_path.name
        
        try:
            # Create pre-commit hook (3 lines - true 95/5)
            pre_commit_hook = self._create_pre_commit_hook(project_name)
            self._write_hook(hooks_dir / "pre-commit", pre_commit_hook)
            
            # Create post-commit hook for violation detection
            post_commit_hook = self._create_post_commit_hook(project_name)
            self._write_hook(hooks_dir / "post-commit", post_commit_hook)
            
            return {
                "success": True,
                "project": project_name,
                "hooks_installed": ["pre-commit", "post-commit"],
                "service_url": self.service_url,
                "path": str(project_path)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Hook installation failed: {str(e)}"}
    
    def _create_pre_commit_hook(self, project_name: str) -> str:
        """Create minimal pre-commit hook - 95/5 delegation pattern"""
        return f"""#!/bin/sh
# Auto-docs generation (95/5 pattern - service does everything)
curl -X POST {self.service_url}/api/auto-docs/generate -d '{{"project":"{project_name}"}}' -H "Content-Type: application/json" || echo "Auto-docs generation failed"
"""
    
    def _create_post_commit_hook(self, project_name: str) -> str:
        """Create minimal post-commit hook for violation detection"""
        return f"""#!/bin/sh
# LNLA violation detection (95/5 pattern)
curl -X POST {self.service_url}/api/violations/check -d '{{"project":"{project_name}"}}' -H "Content-Type: application/json" || echo "Violation check failed"
"""
    
    def _write_hook(self, hook_path: Path, content: str) -> None:
        """Write hook file and make executable"""
        hook_path.write_text(content)
        os.chmod(hook_path, 0o755)


# Factory function for easy instantiation
def create_auto_docs_setup_service() -> AutoDocsSetupService:
    """Create auto-docs setup service"""
    return AutoDocsSetupService()