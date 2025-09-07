#!/usr/bin/env python3
"""
Component Registry - Auto-Discovery System (FIXES dual system)
Single Responsibility: Dynamically discover ALL components with smart injection
Pattern: <80 LOC with auto-discovery (no manual registration - includes ALL components)
"""

import importlib
import inspect
from typing import Dict, Any
from pathlib import Path
from .resources import get_intelligence_resource, get_llm_resource, get_prompt_resource, get_qdrant_resource


class ComponentRegistry:
    """Auto-discovering registry - FIXES dual system by including ALL components"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get_component(self, domain: str, component: str):
        """Get component with auto-discovery, caching, and smart resource injection"""
        cache_key = f"{domain}.{component}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            # Dynamic import
            module = importlib.import_module(f"src.core.components.{domain}.{component}")
            
            # Try factory function first (preferred pattern)
            factory = getattr(module, f"create_{component}", None)
            if factory:
                instance = factory()
            else:
                # Fallback: auto-detect and instantiate component class with resource injection
                component_class = self._find_component_class(module)
                instance = self._inject_resources(component_class)
            
            self._cache[cache_key] = instance
            return instance
            
        except ImportError as e:
            raise ValueError(f"Component {domain}.{component} not found: {e}")
    
    def list_available_components(self) -> Dict[str, list]:
        """Auto-discover all components by scanning filesystem - NO manual registration"""
        available = {}
        components_dir = Path(__file__).parent / "components"
        
        for domain_dir in components_dir.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith('_'):
                components = [f.stem for f in domain_dir.glob("*.py") if not f.name.startswith('_')]
                if components:
                    available[domain_dir.name] = components
        return available
    
    def _find_component_class(self, module):
        """Find component class using naming conventions"""
        # Try common patterns, fallback to any class ending with 'Component'
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isclass(attr) and attr_name.endswith('Component'):
                return attr
        raise ValueError("No component class found")
    
    def _inject_resources(self, component_class):
        """Smart resource injection based on constructor parameter names"""
        sig = inspect.signature(component_class.__init__)
        params = list(sig.parameters.keys())[1:]  # Skip 'self'
        
        kwargs = {}
        resource_map = {
            'intelligence': get_intelligence_resource,
            'llm': get_llm_resource,
            'prompt': get_prompt_resource, 
            'qdrant': get_qdrant_resource
        }
        
        for param in params:
            for resource_type, getter in resource_map.items():
                if resource_type in param.lower():
                    kwargs[param] = getter()
                    break
        
        return component_class(**kwargs)


# Global registry instance
_registry = ComponentRegistry()

def get_registry() -> ComponentRegistry:
    """Get global component registry"""
    return _registry

def get_component(domain: str, component: str):
    """Get component - FIXES dual system with auto-discovery"""
    return _registry.get_component(domain, component)

def list_available_components() -> Dict[str, list]:
    """List all discoverable components"""
    return _registry.list_available_components()