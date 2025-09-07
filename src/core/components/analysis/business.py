#!/usr/bin/env python3
"""
Business Analysis Component - Analysis Domain Micro-Component
Single Responsibility: Extract and analyze business logic from codebases
Pattern: 50-80 LOC component with injected shared resources
"""

from typing import Dict, Any, List, Optional
from ...resources import get_intelligence_resource, IntelligenceResourceManager


class BusinessAnalysisComponent:
    """
    Business analysis using shared resources
    Component Pattern: Small, focused, resource-injected
    """
    
    def __init__(self, intelligence_resource: Optional[IntelligenceResourceManager] = None):
        """
        Initialize with shared resource manager
        Uses singleton if none provided (prevents duplicate resources)
        """
        self.intelligence = intelligence_resource or get_intelligence_resource()
    
    def extract_business_logic(self, project: str) -> Dict[str, Any]:
        """Extract core business logic using native intelligence"""
        if not self.intelligence.project_exists(project):
            return {"error": f"Project '{project}' not indexed"}
        
        query = """Analyze the codebase and extract the core business logic.
        Provide:
        1. Main business rules (numbered list)
        2. Key business entities and their purposes
        3. Critical business processes and workflows
        4. Validation rules and constraints
        5. Business decisions and conditions
        Format as clear, non-technical language that a business analyst would understand."""
        
        result = self.intelligence.intelligence.search_semantic(query, project)
        return {"business_logic": result, "project": project}
    
    def extract_business_rules(self, project: str) -> List[str]:
        """Extract business rules using native intelligence"""
        query = "Find all business rules, validation logic, and business constraints in the code"
        result = self.intelligence.intelligence.search_semantic(query, project)
        return result.split('\n') if result else []
    
    def extract_domain_model(self, project: str) -> Dict[str, Any]:
        """Extract domain model using native intelligence"""
        query = "Identify domain entities, value objects, and domain services"
        result = self.intelligence.intelligence.search_semantic(query, project)
        return {"domain_model": result, "project": project}
    
    def extract_workflows(self, project: str) -> Dict[str, Any]:
        """Extract business workflows using native intelligence"""
        query = "Find business processes, workflows, and process flows"
        result = self.intelligence.intelligence.search_semantic(query, project)
        return {"workflows": result, "project": project}
    
    def extract_api_contracts(self, project: str) -> Dict[str, Any]:
        """Extract API contracts using native intelligence"""
        query = "Find API endpoints, request/response schemas, and integration contracts"
        result = self.intelligence.intelligence.search_semantic(query, project)
        return {"api_contracts": result, "project": project}
    
    def generate_business_summary(self, project: str) -> str:
        """Generate comprehensive business summary"""
        query = "Provide a comprehensive business summary of what this application does"
        return self.intelligence.intelligence.search_semantic(query, project)


# Component factory for easy instantiation
def create_business_analysis() -> BusinessAnalysisComponent:
    """Create business analysis component with shared resources"""
    return BusinessAnalysisComponent()