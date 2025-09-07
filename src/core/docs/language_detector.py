#!/usr/bin/env python3
"""
Language Detection Service - Documentation Domain
Single Responsibility: Detect languages and frameworks from project structure
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def detect_with_linguist(project_path: Path) -> Optional[Dict[str, List[str]]]:
    """Use GitHub Linguist for mature language detection"""
    try:
        result = subprocess.run(
            ['linguist', '--json', str(project_path)], 
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            languages = [f".{lang.lower()}" for lang in data.keys()]
            return {"languages": sorted(languages), "source": "linguist"}
    except Exception:
        pass
    
    return None


def detect_with_manifest_analysis(project_path: Path) -> Dict[str, List[str]]:
    """Fallback: Manifest-based detection (lightweight, reliable)"""
    languages = set()
    frameworks = set()
    
    # Industry-standard manifest files
    manifests = {
        'package.json': ['.js', '.ts'],
        'pyproject.toml': ['.py'], 
        'requirements.txt': ['.py'],
        'Cargo.toml': ['.rs'],
        'go.mod': ['.go'],
        'build.gradle': ['.java'],
        'pom.xml': ['.java'],
        'Gemfile': ['.rb'],
        'composer.json': ['.php'],
        'Dockerfile': ['docker']
    }
    
    # Parse manifests first (most reliable)
    for manifest_file, detected_langs in manifests.items():
        manifest_path = project_path / manifest_file
        if manifest_path.exists():
            languages.update(detected_langs)
            
            # Framework detection from manifests
            try:
                content = manifest_path.read_text(encoding='utf-8', errors='ignore').lower()
                if 'fastapi' in content or 'uvicorn' in content:
                    frameworks.add('FastAPI')
                elif 'express' in content and '.js' in detected_langs:
                    frameworks.add('Express') 
                elif 'django' in content:
                    frameworks.add('Django')
                elif 'react' in content:
                    frameworks.add('React')
            except Exception:
                continue
    
    # Quick file scan for additional languages (lightweight)
    common_extensions = {'.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.cs'}
    for file_path in project_path.rglob("*"):
        if len(languages) > 10:  # Stop early for performance
            break
        if file_path.is_file() and file_path.suffix.lower() in common_extensions:
            languages.add(file_path.suffix.lower())
    
    return {
        "languages": sorted(list(languages)),
        "frameworks": sorted(list(frameworks)) if frameworks else ["Generic"],
        "source": "manifest_analysis"
    }


def detect_languages_and_frameworks(project_path: Path) -> Dict[str, List[str]]:
    """
    Universal Language Detection - Priority: 1) Linguist, 2) Manifest analysis
    """
    # Try mature solution first (GitHub Linguist)
    result = detect_with_linguist(project_path)
    if result:
        print(f"🎯 Using GitHub Linguist for language detection")
        return result
    
    # Fallback to reliable manifest analysis
    print(f"📋 Using manifest analysis (Linguist not available)")
    return detect_with_manifest_analysis(project_path)