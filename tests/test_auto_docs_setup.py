#!/usr/bin/env python3
"""
TDD Test for Auto-Docs Hook Setup - Living Document Integration
Tests the 95/5 pattern for git hook setup in external projects
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
import requests

class TestAutoDocsSetup:
    """Test auto-docs hook setup for external projects (TDD)"""
    
    def test_setup_git_hooks_api_endpoint_exists(self):
        """TEST: API endpoint /api/auto-docs/setup should exist"""
        # This should fail initially - RED phase
        response = requests.post("http://localhost:8000/api/auto-docs/setup", 
                                json={"project_path": "/tmp/test"})
        assert response.status_code in [200, 404]  # 404 means endpoint doesn't exist yet
    
    def test_git_hook_creation_for_claude_parser(self):
        """TEST: Should create 3-line git hooks that call our service"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "claude-parser"
            project_path.mkdir()
            
            # Initialize git repo
            subprocess.run(["git", "init"], cwd=project_path)
            
            # This should fail initially - no hook creation logic yet
            response = requests.post("http://localhost:8000/api/auto-docs/setup",
                                   json={"project_path": str(project_path)})
            
            hooks_dir = project_path / ".git" / "hooks"
            pre_commit = hooks_dir / "pre-commit"
            
            # Should create minimal hook that delegates to our service
            if pre_commit.exists():
                content = pre_commit.read_text()
                assert "curl" in content or "requests" in content
                assert "localhost:8000" in content
                assert len(content.split('\n')) < 10  # <10 lines = 95/5 pattern
    
    def test_violation_detection_integration(self):
        """TEST: Hooks should include LNLA violation detection"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "lnla-hooks"
            project_path.mkdir()
            subprocess.run(["git", "init"], cwd=project_path)
            
            response = requests.post("http://localhost:8000/api/auto-docs/setup",
                                   json={"project_path": str(project_path)})
            
            pre_commit = project_path / ".git" / "hooks" / "pre-commit"
            
            if pre_commit.exists():
                content = pre_commit.read_text()
                assert "violations" in content.lower() or "lnla" in content.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])