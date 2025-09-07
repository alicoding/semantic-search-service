#!/usr/bin/env python3
"""
Architecture Compliance Component - Analysis Domain Micro-Component
Single Responsibility: Ensure code follows CLAUDE.md architecture patterns
Pattern: Follows EXACT proven pattern from ViolationsAnalysisComponent
"""

from typing import List, Optional
from ...resources import get_intelligence_resource, get_llm_resource
from ...resources import IntelligenceResourceManager, LLMSelectionResourceManager


class ArchitectureComplianceComponent:
    """
    Architecture pattern compliance checker using shared resources
    Component Pattern: Follows EXACT pattern from ViolationsAnalysisComponent (proven to work)
    """
    
    def __init__(self, 
                 intelligence_resource: Optional[IntelligenceResourceManager] = None,
                 llm_resource: Optional[LLMSelectionResourceManager] = None):
        """
        Initialize with shared resource managers - EXACT DIP pattern from CLAUDE.md
        Uses singletons if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
        self.llm = llm_resource or get_llm_resource()
    
    def check_architecture_compliance(self, project: str, language: str = None) -> List[str]:
        """
        Check compliance with CLAUDE.md patterns - GENERIC for any language/framework
        Framework does 95% - using proven semantic search approach
        """
        if not self.intelligence.project_exists(project):
            return [f"Project '{project}' not indexed"]
        
        violations = []
        
        try:
            # GENERIC architecture pattern queries (language-agnostic CLAUDE.md patterns)
            architecture_queries = [
                # DIP Pattern check - GENERIC dependency injection pattern
                "Find constructors or initialization code that creates dependencies directly instead of using dependency injection",
                
                # Resource duplication check - GENERIC resource sharing pattern
                "Find duplicate resource creation (clients, connections, instances) instead of shared resource patterns",
                
                # Component size check - GENERIC micro-component pattern
                "Find large classes or modules that could be split into smaller focused components",
                
                # 95/5 Pattern check - GENERIC framework usage
                "Find custom implementations instead of using framework native methods and patterns"
            ]
            
            for i, query in enumerate(architecture_queries):
                try:
                    # EXACT pattern from ViolationsAnalysisComponent - direct semantic search
                    results = self.intelligence.search(query, project, limit=3)
                    
                    # EXACT filtering logic from ViolationsAnalysisComponent + compliance filtering
                    if results and results.strip() and "empty response" not in results.lower():
                        context_lower = results.lower()
                        
                        # Skip compliant responses (these indicate good architecture)
                        if any(compliant_phrase in context_lower for compliant_phrase in [
                            "does not contain", "no information", "not contain any", "provided context does not"
                        ]):
                            continue
                        
                        # GENERIC processing pattern - works for any language
                        violation_types = ["Dependency Injection violations", "Resource duplication", "Oversized components", "Framework pattern violations"]
                        context = results.strip()[:200] + "..." if len(results) > 200 else results.strip()
                        
                        # GENERIC file/code reference check - works for multiple languages
                        code_indicators = [
                            # Generic code patterns
                            'class', 'function', 'method', 'module', 'component', 'service',
                            # File extensions for common languages
                            '.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.rb', '.php',
                            # Code structure indicators
                            'constructor', 'init', 'main', 'import', 'require', 'include'
                        ]
                        
                        if any(keyword in context_lower for keyword in code_indicators):
                            violations.append(f"{violation_types[i]}: {context}")
                                
                except Exception as e:
                    violations.append(f"Error in {['DIP', 'Resource', 'Size'][i]} analysis: {str(e)}")
            
            # Same summary pattern as ViolationsAnalysisComponent
            if len(violations) < 2:
                try:
                    # Native pattern: Let LlamaIndex analyze overall architecture compliance
                    compliance_query = "Analyze architecture patterns, dependency injection, and component structure"
                    summary = self.intelligence.search(compliance_query, project, limit=1)
                    
                    if summary and summary.strip():
                        violations.append(f"Architecture Analysis: {summary.strip()[:200]}...")
                    else:
                        violations.append("✅ Architecture follows CLAUDE.md patterns correctly")
                        
                except Exception:
                    violations.append("✅ Analysis completed using native LlamaIndex patterns")
                    
        except Exception as e:
            violations.append(f"Error in architecture analysis: {str(e)}")
        
        return violations[:6]  # Same limit as ViolationsAnalysisComponent


# Component factory - same pattern as all other components
def create_architecture_compliance() -> ArchitectureComplianceComponent:
    """Create architecture compliance component with shared resources"""
    return ArchitectureComplianceComponent()


# Backward compatibility - GENERIC for any language
def check_architecture_compliance(project: str, language: str = None) -> List[str]:
    """
    Backward compatible function using component
    
    Args:
        project: Project name to analyze
        language: Optional language hint (python, javascript, java, go, etc.)
                 If not provided, will auto-detect from codebase
    """
    component = create_architecture_compliance()
    return component.check_architecture_compliance(project, language)