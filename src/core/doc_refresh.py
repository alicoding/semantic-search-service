#!/usr/bin/env python3
"""
Documentation Auto-Refresh - Native LlamaIndex refresh patterns
Following TRUE 95/5 principle - LlamaIndex refresh_ref_docs() does everything
"""

import time
import threading
from typing import Dict, List
from pathlib import Path
from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .config import get_qdrant_client, CONFIG, get_configured_reader

def refresh_documentation_collection(collection_name: str, docs_path: str) -> Dict:
    """Refresh documentation using native LlamaIndex refresh_ref_docs - TRUE 95/5"""
    client = get_qdrant_client()
    
    if not client.collection_exists(collection_name):
        return {"error": f"Collection {collection_name} does not exist"}
    
    try:
        # Use centralized reader configuration
        reader = get_configured_reader(docs_path)
        documents = reader.load_data()
        
        # Ensure documents have unique IDs for refresh to work
        for i, doc in enumerate(documents):
            if not doc.doc_id:
                doc.doc_id = f"{collection_name}_doc_{i}"
        
        # Create index from existing collection
        vector_store = QdrantVectorStore(
            client=client, 
            collection_name=collection_name
        )
        index = VectorStoreIndex.from_vector_store(vector_store)
        
        # Native LlamaIndex refresh - one-liner!
        refreshed_flags = index.refresh_ref_docs(documents, update_kwargs={"show_progress": True})
        
        refreshed_count = sum(1 for flag in refreshed_flags if flag)
        
        return {
            "collection": collection_name,
            "total_documents": len(documents),
            "refreshed_documents": refreshed_count,
            "path": docs_path
        }
        
    except Exception as e:
        return {"error": f"Failed to refresh {collection_name}: {str(e)}"}

def get_refresh_schedule() -> Dict:
    """Get refresh schedule from config"""
    doc_config = CONFIG.get('documentation', {})
    refresh_config = doc_config.get('refresh', {})
    
    return {
        "enabled": refresh_config.get('enabled', False),
        "schedule": refresh_config.get('schedule', 'weekly'),
        "frameworks": refresh_config.get('frameworks', [])
    }

def calculate_next_refresh_time(schedule: str) -> int:
    """Calculate seconds until next refresh"""
    schedule_intervals = {
        'daily': 24 * 60 * 60,      # 24 hours
        'weekly': 7 * 24 * 60 * 60, # 7 days  
        'monthly': 30 * 24 * 60 * 60 # 30 days
    }
    
    return schedule_intervals.get(schedule, 7 * 24 * 60 * 60)  # Default to weekly

def start_refresh_scheduler():
    """Start background refresh scheduler - simple Python threading"""
    refresh_config = get_refresh_schedule()
    
    if not refresh_config['enabled']:
        print("📅 Doc refresh scheduler disabled in config")
        return
    
    print(f"📅 Starting doc refresh scheduler: {refresh_config['schedule']}")
    
    def refresh_worker():
        while True:
            try:
                # Refresh each configured framework
                for framework in refresh_config['frameworks']:
                    collection_name = f"docs_{framework}"
                    # Use centralized docs location from config
                    shared_path = CONFIG.get('documentation', {}).get('shared_docs_path', '/Volumes/AliDev/ai-shared-docs/frameworks')
                    docs_path = Path(shared_path) / framework
                    
                    if Path(docs_path).exists():
                        print(f"🔄 Refreshing {framework} docs...")
                        result = refresh_documentation_collection(collection_name, docs_path)
                        
                        if 'error' in result:
                            print(f"❌ Error refreshing {framework}: {result['error']}")
                        else:
                            print(f"✅ Refreshed {framework}: {result['refreshed_documents']}/{result['total_documents']} documents updated")
                    else:
                        print(f"⚠️ Docs path not found for {framework}: {docs_path}")
                
                # Sleep until next refresh
                sleep_time = calculate_next_refresh_time(refresh_config['schedule'])
                print(f"⏰ Next refresh in {sleep_time//3600} hours")
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ Refresh scheduler error: {e}")
                # Sleep 1 hour on error then retry
                time.sleep(3600)
    
    # Start background thread
    refresh_thread = threading.Thread(target=refresh_worker, daemon=True)
    refresh_thread.start()
    
    return refresh_thread

# For manual testing
def refresh_all_configured_docs():
    """Manually refresh all configured documentation"""
    refresh_config = get_refresh_schedule()
    results = {}
    
    for framework in refresh_config['frameworks']:
        collection_name = f"docs_{framework}"
        # Use centralized docs location from config
        shared_path = CONFIG.get('documentation', {}).get('shared_docs_path', '/Volumes/AliDev/ai-shared-docs/frameworks')
        docs_path = str(Path(shared_path) / framework)
        
        if Path(docs_path).exists():
            results[framework] = refresh_documentation_collection(collection_name, docs_path)
        else:
            results[framework] = {"error": f"Docs path not found: {docs_path}"}
    
    return results

if __name__ == "__main__":
    # Test manual refresh
    print("Testing documentation refresh...")
    results = refresh_all_configured_docs()
    for framework, result in results.items():
        print(f"{framework}: {result}")