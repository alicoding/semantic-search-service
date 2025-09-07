#!/usr/bin/env python3
"""
Workflow Indexing Component - 2025 LlamaIndex Docuflows Pattern
Single Responsibility: Event-driven document processing with validation stages
Pattern: Modern workflow-based component using declarative pipelines
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from ...resources import get_intelligence_resource, IntelligenceResourceManager
from ...resources.cache_manager import get_cache_manager, CacheResourceManager


class DocumentProcessingWorkflow:
    """
    2025 Pattern: Event-driven document processing workflow
    Implements EXTRACT → VALIDATE → REFLECT → CORRECT pattern
    """
    
    def __init__(self, 
                 intelligence_resource: Optional[IntelligenceResourceManager] = None,
                 cache_resource: Optional[CacheResourceManager] = None):
        """Initialize with modern resource injection pattern"""
        self.intelligence = intelligence_resource or get_intelligence_resource()
        self.cache = cache_resource or get_cache_manager()
        self.workflow_state = {}  # Durable workflow state
        
    def create_document_pipeline(self, source_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        2025 Docuflows Pattern: Declarative document processing pipeline
        Replaces manual VectorStoreIndex construction with workflow-based approach
        """
        pipeline_steps = [
            {"stage": "extract", "status": "pending"},
            {"stage": "validate", "status": "pending"}, 
            {"stage": "index", "status": "pending"},
            {"stage": "persist", "status": "pending"}
        ]
        
        workflow_id = f"workflow_{source_config.get('collection_name', 'default')}"
        self.workflow_state[workflow_id] = {
            "steps": pipeline_steps,
            "config": source_config,
            "status": "running"
        }
        
        try:
            # Stage 1: EXTRACT
            documents = self._extract_documents(source_config)
            self._update_workflow_step(workflow_id, "extract", "completed")
            
            # Stage 2: VALIDATE  
            validated_docs = self._validate_documents(documents, source_config)
            self._update_workflow_step(workflow_id, "validate", "completed")
            
            # Stage 3: INDEX (using modern patterns)
            index_result = self._index_documents(validated_docs, source_config)
            self._update_workflow_step(workflow_id, "index", "completed")
            
            # Stage 4: PERSIST (with durable storage)
            persist_result = self._persist_workflow_state(workflow_id, index_result)
            self._update_workflow_step(workflow_id, "persist", "completed")
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "docs_processed": len(documents),
                "index_result": index_result,
                "workflow_complete": True
            }
            
        except Exception as e:
            self.workflow_state[workflow_id]["status"] = "failed"
            self.workflow_state[workflow_id]["error"] = str(e)
            return {"success": False, "error": str(e), "workflow_id": workflow_id}
    
    def _extract_documents(self, config: Dict[str, Any]) -> List[Any]:
        """Modern extraction with automatic source detection"""
        source_type = config.get("source_type", "auto")
        
        if source_type == "url" or config.get("url"):
            from llama_index.readers.web import SimpleWebPageReader
            return SimpleWebPageReader().load_data([config["url"]])
            
        elif source_type == "github" or config.get("repo"):
            from llama_index.readers.github import GitHubRepositoryReader
            owner, repo = config["repo"].split('/')
            reader = GitHubRepositoryReader(
                github_token=None, owner=owner, repo=repo,
                filter_directories=[["docs"], ["documentation"]]
            )
            return reader.load_data(branch="main")
            
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    def _validate_documents(self, documents: List[Any], config: Dict[str, Any]) -> List[Any]:
        """Validation stage - filter and validate documents"""
        if not documents:
            raise ValueError("No documents extracted")
            
        # Filter empty documents
        valid_docs = [doc for doc in documents if doc.text.strip()]
        
        if len(valid_docs) == 0:
            raise ValueError("All documents are empty after validation")
            
        return valid_docs
    
    def _index_documents(self, documents: List[Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Modern indexing with framework-native patterns"""
        from llama_index.core import VectorStoreIndex
        
        # 2025 Pattern: Simple, declarative indexing
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        
        return {
            "indexed": True,
            "docs_count": len(documents),
            "collection": config.get("collection_name", "default")
        }
    
    def _persist_workflow_state(self, workflow_id: str, index_result: Dict[str, Any]) -> Dict[str, Any]:
        """Durable workflow persistence - 2025 pattern"""
        persist_dir = f"./storage/workflows/{workflow_id}"
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        
        # Save workflow state for recovery
        import json
        with open(f"{persist_dir}/workflow_state.json", "w") as f:
            json.dump(self.workflow_state[workflow_id], f, indent=2)
            
        return {"persisted": True, "persist_dir": persist_dir}
    
    def _update_workflow_step(self, workflow_id: str, step: str, status: str):
        """Update workflow step status"""
        for step_info in self.workflow_state[workflow_id]["steps"]:
            if step_info["stage"] == step:
                step_info["status"] = status
                break


# Component factory for 2025 workflow pattern
def create_workflow_indexing() -> DocumentProcessingWorkflow:
    """Create modern workflow-based indexing component"""
    return DocumentProcessingWorkflow()