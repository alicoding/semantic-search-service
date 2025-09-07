#!/usr/bin/env python3
"""
AutoDocsGenerator Micro-Component - Documentation Domain Component
Single Responsibility: Generate documentation automatically using native LlamaIndex 2025 patterns
Pattern: 50-80 LOC micro-component with 95/5 principle - LlamaIndex does 95% of work
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from ...resources import get_intelligence_resource, get_llm_resource
from ...resources import IntelligenceResourceManager, LLMResourceManager


class AutoDocsGeneratorComponent:
    """
    Automated documentation generator using NATIVE LlamaIndex 2025 patterns
    Component Pattern: Small, focused, resource-injected (95/5 principle)
    """
    
    def __init__(self, 
                 intelligence_resource: Optional[IntelligenceResourceManager] = None,
                 llm_resource: Optional[LLMResourceManager] = None):
        """
        Initialize with shared resource managers - NATIVE LlamaIndex pattern
        Uses singletons if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
        self.llm = llm_resource or get_llm_resource()
    
    def generate_docs(self, project_path: str, doc_type: str = "api") -> Dict[str, Any]:
        """
        Generate documentation using NATIVE LlamaIndex 2025 patterns
        95/5 approach: LlamaIndex handles extraction, synthesis, and formatting
        """
        if not Path(project_path).exists():
            return {"error": f"Project path not found: {project_path}", "generated": False}
        
        project_name = Path(project_path).name
        
        # Check if project is indexed using shared intelligence resource
        if not self.intelligence.project_exists(project_name):
            return {"error": f"Project '{project_name}' not indexed. Please index first.", "generated": False}
        
        try:
            # NATIVE LlamaIndex pattern: Semantic documentation queries (2025)
            doc_queries = self._get_documentation_queries(doc_type)
            
            generated_sections = {}
            for section, query in doc_queries.items():
                try:
                    # Direct semantic search using shared intelligence - 95/5 pattern
                    result = self.intelligence.search(query, project_name, limit=5)
                    
                    if result and result.strip():
                        generated_sections[section] = result.strip()
                        
                except Exception as e:
                    generated_sections[section] = f"Error generating {section}: {str(e)}"
            
            # Native LlamaIndex document synthesis pattern
            documentation = self._synthesize_documentation(
                project_name, doc_type, generated_sections
            )
            
            # Save documentation file
            output_path = self._save_documentation(project_name, doc_type, documentation)
            
            return {
                "generated": True,
                "output_path": str(output_path),
                "sections": len(generated_sections),
                "project": project_name,
                "doc_type": doc_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Documentation generation failed: {str(e)}", "generated": False}
    
    def _get_documentation_queries(self, doc_type: str) -> Dict[str, str]:
        """Get semantic queries based on Perplexity research for 2025 patterns"""
        if doc_type == "api":
            return {
                "overview": "Summarize the project architecture, main components, and purpose",
                "endpoints": "Extract all API endpoints, functions, and public methods with their parameters",
                "classes": "Find all classes and their responsibilities, methods, and relationships",
                "usage": "Provide usage examples, installation instructions, and getting started guide"
            }
        elif doc_type == "readme":
            return {
                "description": "Describe what this project does and its main purpose",
                "installation": "How to install and set up this project",
                "usage": "Basic usage examples and common use cases",
                "architecture": "High-level architecture and component overview"
            }
        else:
            return {
                "overview": f"Generate {doc_type} documentation for this codebase",
                "details": f"Extract detailed information relevant to {doc_type} documentation"
            }
    
    def _synthesize_documentation(self, project_name: str, doc_type: str, sections: Dict[str, str]) -> str:
        """Native LlamaIndex document synthesis - minimal custom formatting"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        doc = f"""# {project_name.replace('-', ' ').title()} - {doc_type.upper()} Documentation

*Auto-generated on {timestamp} using LlamaIndex native patterns*

"""
        
        for section_name, content in sections.items():
            if content:
                doc += f"""## {section_name.title()}

{content}

"""
        
        doc += f"""
---
*Generated using AutoDocsGenerator micro-component with native LlamaIndex 2025 patterns*
*Project: {project_name} | Type: {doc_type} | Generated: {timestamp}*
"""
        
        return doc
    
    def _save_documentation(self, project_name: str, doc_type: str, content: str) -> Path:
        """Save generated documentation to appropriate location"""
        docs_dir = Path("docs/generated")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{project_name}_{doc_type}_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = docs_dir / filename
        
        output_path.write_text(content, encoding='utf-8')
        return output_path


# Component factory for easy instantiation
def create_auto_docs_generator() -> AutoDocsGeneratorComponent:
    """Create auto docs generator component with shared resources"""
    return AutoDocsGeneratorComponent()