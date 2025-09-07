#!/usr/bin/env python3
"""
Documentation Generator - Documentation Domain Core Service
Single Responsibility: Generate documentation from codebase using intelligence abstractions
"""

from pathlib import Path
from datetime import datetime
from typing import Dict

from ..intelligence import get_codebase_intelligence
from ..intelligence.types import IndexMode
from ..config import get_llm
from ..prompts import get_prompt
from .language_detector import detect_languages_and_frameworks
from .doc_reader import get_multi_language_reader


def generate_api_reference(project_path: str = ".") -> Dict:
    """
    Universal Documentation Generator - Uses intelligence abstractions (DIP compliant)
    """
    print(f"📚 Generating universal documentation for: {project_path}")
    start_time = datetime.now()
    
    project_path = Path(project_path)
    if not project_path.exists():
        raise FileNotFoundError(f"Project path not found: {project_path}")
    
    # Step 1: Detect languages and frameworks (Domain Service)
    detection_info = detect_languages_and_frameworks(project_path)
    languages = detection_info["languages"]
    frameworks = detection_info["frameworks"]
    
    print(f"🔍 Detected languages: {', '.join(languages) if languages else 'None'}")
    print(f"🎯 Detected frameworks: {', '.join(frameworks)}")
    
    # Step 2: Load documents (Domain-specific reader)
    try:
        reader = get_multi_language_reader(str(project_path))
        documents = reader.load_data()
    except Exception as e:
        print(f"⚠️ Error reading directory: {e}")
        from ..config import get_configured_reader
        reader = get_configured_reader(str(project_path))
        documents = reader.load_data()
    
    print(f"📄 Found {len(documents)} files across {len(languages)} languages")
    
    if not documents:
        return {
            "generated": False,
            "error": "No documents found in codebase",
            "path": str(project_path)
        }
    
    # Step 3: Use intelligence abstractions (DIP - depend on abstractions)
    intelligence = get_codebase_intelligence()
    collection_name = f"docs_{project_path.name}_{int(datetime.now().timestamp())}"
    
    # Create temporary index using intelligence
    try:
        result = intelligence._get_strategy(IndexMode.VECTOR).create_index(documents, collection_name)
        index = result
    except Exception as e:
        print(f"⚠️ Using fallback index creation: {e}")
        from llama_index.core import VectorStoreIndex
        index = VectorStoreIndex.from_documents(documents)
    
    # Step 4: Generate documentation with prompts
    documentation_prompt = _get_documentation_prompt(languages, frameworks, project_path.name)
    
    # Step 5: Query using intelligence
    query_engine = index.as_query_engine(llm=get_llm("fast"), similarity_top_k=10)
    response = query_engine.query(documentation_prompt)
    
    print(f"✅ Generated universal documentation from {len(documents)} files")
    
    # Step 6: Format and save results
    execution_time = (datetime.now() - start_time).total_seconds()
    result = _format_documentation_output(response, languages, frameworks, project_path, documents, execution_time)
    
    return result


def _get_documentation_prompt(languages, frameworks, project_name):
    """Get documentation prompt from centralized prompts or fallback"""
    try:
        return get_prompt("documentation", "universal_extraction", 
                         languages=', '.join(languages),
                         frameworks=', '.join(frameworks),
                         project_name=project_name)
    except KeyError:
        return f"""
        Analyze this {', '.join(languages)} codebase using {', '.join(frameworks)} frameworks.
        Generate comprehensive API documentation including:
        1. All API endpoints, functions, and classes
        2. Code structure and architecture overview  
        3. Usage examples and integration patterns
        4. Multi-language components if present
        
        Organize by logical categories and provide clear, developer-friendly documentation.
        Include file locations and practical examples.
        """


def _format_documentation_output(response, languages, frameworks, project_path, documents, execution_time):
    """Format the documentation output"""
    api_reference = f"""# Universal Documentation

*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Multi-language documentation*

## Project Overview
- **Languages**: {', '.join(languages) if languages else 'Auto-detected'}
- **Frameworks**: {', '.join(frameworks)}
- **Files Analyzed**: {len(documents)}
- **Project**: {project_path.name}

{response}

## Generation Details  
- **Method**: LlamaIndex with Intelligence Abstractions (DIP compliant)
- **Languages detected**: {len(languages)} ({', '.join(languages)})
- **Files processed**: {len(documents)}
- **Project path**: {project_path}
- **Execution time**: {execution_time:.2f} seconds
- **Architecture**: SOLID-compliant Documentation Domain
"""
    
    output_path = Path("docs/API_REFERENCE.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(api_reference)
    
    print(f"✅ Universal documentation generated: {output_path}")
    print(f"⚡ Execution time: {execution_time:.2f} seconds")
    print(f"🎯 Method: Documentation Domain with Intelligence Abstractions")
    print(f"📊 Languages: {', '.join(languages)}, Frameworks: {', '.join(frameworks)}")
    
    return {
        "generated": True,
        "output": str(output_path),
        "execution_time": execution_time,
        "files_scanned": len(documents),
        "languages_detected": languages,
        "frameworks_detected": frameworks,
        "method": "documentation_domain_with_intelligence_abstractions",
        "architecture": "SOLID-compliant Documentation Domain"
    }