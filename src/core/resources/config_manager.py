#!/usr/bin/env python3
"""
Configuration Resource Manager - Centralized Resource Layer
Single Responsibility: Manage shared configuration resources (prevent duplicate loading)
Pattern: Singleton resource manager for efficient config sharing across components
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Load .env file once
load_dotenv()


class AppConfig(BaseSettings):
    """
    Modern Pydantic configuration (2025 pattern)
    Eliminates hardcoded defaults, provides type validation and documentation
    """
    # LLM Configuration
    llm_provider: str = "openai"
    embed_provider: str = "openai"
    ollama_model: str = "llama3.1:latest"
    openai_model: str = "gpt-4"
    openai_embed_model: str = "text-embedding-3-small"
    fast_model: str = "gemini-2.5-flash"
    complex_model: str = "claude-opus-4-1-20250805"
    complex_alt_model: str = "gemini-2.5-pro"
    
    # Service Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_request_timeout: float = 120.0
    ollama_context_window: int = 8000
    num_workers: int = 4
    
    # Indexing Configuration
    chunk_size: int = 512
    chunk_overlap: int = 50
    
    # Storage Configuration
    qdrant_url: str = "http://localhost:6333"
    collection_prefix: str = "ai_intelligence_"
    redis_host: str = "localhost"
    redis_port: int = 6380
    cache_ttl: int = 3600
    
    # API Configuration
    openai_api_key: Optional[str] = None
    electronhub_api_key: Optional[str] = None
    electronhub_base_url: Optional[str] = None
    spider_api_key: Optional[str] = None
    confluence_user: Optional[str] = None
    confluence_pass: Optional[str] = None
    
    # Additional Configuration
    ollama_embed_model: str = "nomic-embed-text"
    index_mode: str = "auto"
    redis_enabled: bool = True
    enable_hybrid: bool = False
    crawl_depth: int = 3
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    debug_mode: bool = False
    
    # Performance Configuration  
    target_hook_response_ms: int = 100
    target_exists_response_ms: int = 200
    target_context_response_ms: int = 500
    violation_snippet_length: int = 300
    
    # Complex nested configs (allow extra)
    indexing: Optional[Dict[str, Any]] = None
    documentation: Optional[Dict[str, Any]] = None
    
    class Config:
        env_file = '.env'
        case_sensitive = False
        extra = 'allow'  # Allow extra fields for backward compatibility


class ConfigurationResourceManager:
    """
    Centralized configuration resource manager using Pydantic BaseSettings (2025 pattern)
    Eliminates hardcoded defaults and provides type validation
    """
    
    _instance: Optional['ConfigurationResourceManager'] = None
    _config: Optional[AppConfig] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def config(self) -> AppConfig:
        """Get shared Pydantic config (lazy initialization)"""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def _load_config(self) -> AppConfig:
        """
        Load configuration using modern Pydantic BaseSettings (2025 pattern)
        Framework handles: type validation, env var parsing, defaults
        We handle: YAML override logic only (5%)
        """
        config_path = Path("config.yaml")
        
        if config_path.exists():
            # YAML overrides (optional)
            with open(config_path) as f:
                yaml_config = yaml.safe_load(f)
                # Replace environment variables in YAML
                for key, value in yaml_config.items():
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]
                        yaml_config[key] = os.getenv(env_var, value)
                return AppConfig(**yaml_config)
        else:
            # Pure Pydantic - framework does 95% of work
            return AppConfig()
    
    def initialize_settings(self, config: Optional[AppConfig] = None) -> None:
        """Initialize LlamaIndex Settings - Native way (called once)"""
        if self._initialized:
            return
            
        if config is None:
            config = self.config
        
        self._setup_llm_models(config)
        self._setup_embeddings(config)
        self._setup_node_parser(config)
        
        # Store config in Settings for other uses
        Settings._config = config
        self._initialized = True
    
    def _setup_llm_models(self, config: AppConfig) -> None:
        """Setup LLM models based on configuration"""
        electronhub_key = os.getenv("ELECTRONHUB_API_KEY")
        electronhub_base = os.getenv("ELECTRONHUB_BASE_URL")
        
        if config.llm_provider == "ollama":
            # Ollama setup - single model
            Settings.llm = Settings.llm_fast = Settings.llm_complex = Ollama(
                model=config.ollama_model,
                base_url=config.ollama_base_url,
                request_timeout=config.ollama_request_timeout,
                context_window=config.ollama_context_window,
            )
        elif electronhub_key and electronhub_base:
            self._setup_electronhub_models(config, electronhub_key, electronhub_base)
        else:
            # Fallback to standard OpenAI
            Settings.llm = Settings.llm_fast = Settings.llm_complex = OpenAI(
                model=config.openai_model,
                api_key=os.getenv("OPENAI_API_KEY"),
            )
    
    def _setup_electronhub_models(self, config: AppConfig, api_key: str, api_base: str) -> None:
        """Setup ElectronHub dual-model configuration"""
        # Fast model - Gemini 2.5 Flash
        Settings.llm_fast = OpenAILike(
            model=config.fast_model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=60.0,
        )
        
        # Complex model - Claude Opus 4.1
        Settings.llm_complex = OpenAILike(
            model=config.complex_model, 
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=120.0,
        )
        
        # Alternative complex model - Gemini 2.5 Pro
        Settings.llm_complex_alt = OpenAILike(
            model=config.complex_alt_model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=True,
            max_requests_per_minute=30,
            request_timeout=90.0,
        )
        
        # Default to fast model
        Settings.llm = Settings.llm_fast
    
    def _setup_embeddings(self, config: AppConfig) -> None:
        """Setup embedding models based on configuration"""
        if config.embed_provider == "ollama":
            Settings.embed_model = OllamaEmbedding(
                model_name=config.ollama_embed_model,
                base_url=config.ollama_base_url,
            )
        else:
            Settings.embed_model = OpenAIEmbedding(
                model=config.openai_embed_model,
                api_key=os.getenv("OPENAI_API_KEY"),
                max_requests_per_minute=60,  # Prevent rate limiting
                max_query_length=8191,
            )
    
    def _setup_node_parser(self, config: AppConfig) -> None:
        """Setup node parser based on configuration"""
        Settings.node_parser = SentenceSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
    
    def get_collection_name(self, project: str) -> str:
        """Get collection name with configured prefix"""
        prefix = self.config.collection_prefix
        return f"{prefix}{project}"
    
    def get_configured_reader(self, path: str, filename_as_id: bool = False):
        """Get SimpleDirectoryReader with config settings"""
        from llama_index.core import SimpleDirectoryReader
        from pathlib import Path
        index_config = self.config.get('indexing', {})
        
        # Native 2025 pattern: Use explicit include paths if configured
        include_paths = index_config.get('include_paths')
        if include_paths and isinstance(include_paths, list):
            # Collect all file paths from include_paths (native LlamaIndex approach)
            base_path = Path(path)
            file_paths = []
            file_exts = set(index_config.get('file_extensions', ['.py', '.js', '.md']))
            
            for include_path in include_paths:
                abs_path = base_path / include_path
                
                if abs_path.is_file():
                    # Individual file
                    file_paths.append(str(abs_path))
                elif abs_path.is_dir():
                    # Directory - collect all matching files recursively
                    for file_path in abs_path.rglob("*"):
                        if file_path.is_file() and file_path.suffix in file_exts:
                            file_paths.append(str(file_path))
                else:
                    print(f"Warning: Include path {abs_path} does not exist")
            
            if file_paths:
                # Use native input_files for explicit file inclusion
                return SimpleDirectoryReader(
                    input_files=file_paths,
                    filename_as_id=filename_as_id
                )
        
        # Fallback to traditional directory + exclude pattern
        return SimpleDirectoryReader(
            path,
            recursive=index_config.get('recursive', True),
            required_exts=index_config.get('file_extensions', ['.py', '.js', '.md']),
            exclude=index_config.get('exclude_patterns', ['node_modules', '__pycache__', '.git']),
            filename_as_id=filename_as_id
        )


# Global instance for component sharing
_config_manager = ConfigurationResourceManager()

def get_config_resource() -> ConfigurationResourceManager:
    """Get shared configuration resource manager"""
    return _config_manager