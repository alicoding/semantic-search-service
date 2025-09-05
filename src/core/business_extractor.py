#!/usr/bin/env python3
"""
Business Logic Extractor - TRUE 95/5 Pattern
Extract business rules and logic from codebase using native LlamaIndex
"""

from .index_helper import get_index, index_exists
from typing import Dict, Any, List

def extract_business_logic(project: str) -> Dict[str, Any]:
    """
    Extract core business logic - TRUE 95/5 pattern
    Returns structured business rules and logic
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    # Native query for business logic extraction
    query = """
    Analyze the codebase and extract the core business logic.
    Provide:
    1. Main business rules (numbered list)
    2. Key business entities and their purposes
    3. Critical business processes and workflows
    4. Validation rules and constraints
    5. Business decisions and conditions
    Format as clear, non-technical language that a business analyst would understand.
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    return {
        "project": project,
        "business_logic": str(response),
        "extraction_type": "comprehensive"
    }

def extract_business_rules(project: str) -> List[str]:
    """
    Extract specific business rules - TRUE 95/5 pattern
    Returns list of business rules
    """
    if not index_exists(project):
        return [f"Error: Project '{project}' not indexed"]
    
    query = """
    List all business rules found in the code.
    Focus on:
    - Validation rules
    - Authorization rules
    - Business constraints
    - Calculation formulas
    - Decision criteria
    Output as numbered list, one rule per line.
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    # Parse response into list
    rules_text = str(response)
    rules = [rule.strip() for rule in rules_text.split('\n') if rule.strip()]
    return rules

def extract_domain_model(project: str) -> Dict[str, Any]:
    """
    Extract domain model - TRUE 95/5 pattern
    Returns entities and their relationships
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    query = """
    Extract the domain model from the codebase.
    Identify:
    1. Domain entities (e.g., User, Order, Product)
    2. Value objects (e.g., Money, Address)
    3. Aggregates and their boundaries
    4. Relationships between entities
    Output as structured JSON if possible.
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    return {
        "project": project,
        "domain_model": str(response),
        "model_type": "DDD"
    }

def extract_workflows(project: str) -> Dict[str, Any]:
    """
    Extract business workflows - TRUE 95/5 pattern
    Returns process flows and workflows
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    query = """
    Identify and describe the main business workflows in the code.
    For each workflow provide:
    1. Workflow name
    2. Trigger/Starting point
    3. Steps involved (in order)
    4. Decision points
    5. End states/outcomes
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    return {
        "project": project,
        "workflows": str(response),
        "workflow_type": "business_process"
    }

def extract_api_contracts(project: str) -> Dict[str, Any]:
    """
    Extract API contracts and interfaces - TRUE 95/5 pattern
    Returns API endpoints and their business purposes
    """
    if not index_exists(project):
        return {"error": f"Project '{project}' not indexed"}
    
    query = """
    Extract all API endpoints and their business purposes.
    For each endpoint provide:
    1. Endpoint path and method
    2. Business purpose (what business operation it performs)
    3. Required inputs and their business meaning
    4. Expected outputs and their business significance
    5. Business rules applied
    """
    
    response = get_index(project).as_query_engine().query(query)
    
    return {
        "project": project,
        "api_contracts": str(response),
        "contract_type": "REST_API"
    }

def generate_business_summary(project: str) -> str:
    """
    Generate executive summary of business logic - TRUE 95/5 pattern
    Returns brief business-focused summary
    """
    if not index_exists(project):
        return f"Error: Project '{project}' not indexed"
    
    query = """
    Generate a brief executive summary (3-5 paragraphs) of what this application does from a business perspective.
    Focus on:
    - Business problem it solves
    - Key features and capabilities
    - Main user workflows
    - Business value provided
    Write for a non-technical business stakeholder.
    """
    
    response = get_index(project).as_query_engine().query(query)
    return str(response)