#!/usr/bin/env python3
"""
Benchmark Research Hook Performance
Test how fast our semantic search is for hook integration
"""

import time
import json
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.semantic_search import search, check_exists, find_violations

def benchmark_search_operation(operation_name: str, operation_func, *args):
    """Benchmark a single search operation"""
    print(f"\n🔍 Testing {operation_name}...")
    
    start_time = time.time()
    try:
        result = operation_func(*args)
        duration_ms = (time.time() - start_time) * 1000
        
        print(f"✅ {operation_name}: {duration_ms:.1f}ms")
        if hasattr(result, '__len__'):
            print(f"   Results: {len(str(result))} characters")
        
        return duration_ms, True
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        print(f"❌ {operation_name}: {duration_ms:.1f}ms (ERROR: {e})")
        return duration_ms, False

def main():
    """Run performance benchmarks"""
    print("🚀 Benchmarking Research Hook Performance")
    print("=" * 50)
    
    project_name = "semantic-search-service"
    
    # Test queries that might come from hooks
    test_queries = [
        "implement user authentication",
        "create API endpoint", 
        "fix Settings initialization",
        "add health check"
    ]
    
    test_components = [
        "Settings",
        "FastAPI",
        "UserService",
        "AuthHandler"
    ]
    
    total_time = 0
    successful_ops = 0
    total_ops = 0
    
    # Test semantic search
    print("\n📊 Semantic Search Performance:")
    for query in test_queries:
        duration, success = benchmark_search_operation(
            f"search('{query}')", 
            search, query, project_name, 3
        )
        total_time += duration
        total_ops += 1
        if success:
            successful_ops += 1
    
    # Test component existence checks
    print("\n🔍 Component Existence Performance:")
    for component in test_components:
        duration, success = benchmark_search_operation(
            f"check_exists('{component}')",
            check_exists, component, project_name
        )
        total_time += duration
        total_ops += 1
        if success:
            successful_ops += 1
    
    # Test violations check
    print("\n⚠️ Violations Check Performance:")
    duration, success = benchmark_search_operation(
        "find_violations()",
        find_violations, project_name
    )
    total_time += duration
    total_ops += 1
    if success:
        successful_ops += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 PERFORMANCE SUMMARY:")
    print(f"Total operations: {total_ops}")
    print(f"Successful operations: {successful_ops}")
    print(f"Average time per operation: {total_time / total_ops:.1f}ms")
    print(f"Total time for typical research: {total_time:.1f}ms")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    avg_time = total_time / total_ops
    
    if avg_time < 50:
        print("✅ Performance excellent - safe for auto-research on every prompt")
    elif avg_time < 100:
        print("⚡ Performance good - auto-research with caching recommended") 
    elif avg_time < 500:
        print("⚠️ Performance moderate - explicit trigger recommended")
    else:
        print("🔴 Performance slow - optimize before enabling hooks")
    
    # Configuration suggestions
    suggested_config = {
        "enabled": True,
        "auto_research": avg_time < 100,
        "explicit_trigger": ":research:",
        "performance_threshold": min(200, avg_time * 2),
        "cache_enabled": True
    }
    
    print(f"\n⚙️ SUGGESTED CONFIG:")
    print(json.dumps(suggested_config, indent=2))

if __name__ == "__main__":
    main()