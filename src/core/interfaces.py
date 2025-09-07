#!/usr/bin/env python3
"""
Interfaces - DIP Abstractions
Single Responsibility: Define contracts for dependency injection
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IntelligenceInterface(ABC):
    """Abstract interface for intelligence operations (DIP compliance)"""
    
    @abstractmethod
    def search_semantic(self, query: str, project: str, limit: int = 5) -> str:
        pass
    
    @abstractmethod
    def project_exists(self, project_name: str) -> bool:
        pass
    
    @abstractmethod
    def get_index(self, project_name: str, mode=None):
        pass
    
    @abstractmethod
    def list_projects(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_project_info(self, project_name: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def check_component_exists(self, component: str, project: str) -> Dict[str, Any]:
        pass


class LLMInterface(ABC):
    """Abstract interface for LLM operations (DIP compliance)"""
    
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass


class PromptsInterface(ABC):
    """Abstract interface for prompt operations (DIP compliance)"""
    
    @abstractmethod
    def get_violation_prompt(self) -> str:
        pass
    
    @abstractmethod
    def get_suggestion_prompt(self, task: str) -> str:
        pass