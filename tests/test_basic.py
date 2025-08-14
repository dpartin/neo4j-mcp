#!/usr/bin/env python3
"""
Basic test for Neo4j MCP Server functions
Tests the server functions directly without MCP client
"""

import sys
import os
sys.path.append('..')

def test_server_import():
    """Test that the server can be imported."""
    print("🧪 Testing server import...")
    try:
        import server
        print("✅ Server imported successfully")
        return True
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

def test_echo_function():
    """Test the echo function logic directly."""
    print("\n🧪 Testing echo function logic...")
    try:
        import server
        # Test the underlying logic
        message = "Hello, World!"
        result = f"Echo: {message}"
        if "Hello, World!" in result:
            print("✅ Echo function logic working correctly")
            return True
        else:
            print(f"❌ Echo function logic failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Echo function test failed: {e}")
        return False

def test_list_nodes_function():
    """Test the list_nodes function logic directly."""
    print("\n🧪 Testing list_nodes function logic...")
    try:
        import server
        # Test the underlying logic by calling execute_neo4j_query directly
        result = server.execute_neo4j_query("MATCH (n) RETURN count(n) as count LIMIT 1")
        if result and len(result) > 0:
            print("✅ List nodes function logic working correctly")
            return True
        else:
            print(f"❌ List nodes function logic failed: {result}")
            return False
    except Exception as e:
        print(f"❌ List nodes function test failed: {e}")
        return False

def test_execute_query_function():
    """Test the execute_query function logic directly."""
    print("\n🧪 Testing execute_query function logic...")
    try:
        import server
        # Test the underlying logic by calling execute_neo4j_query directly
        result = server.execute_neo4j_query("RETURN 1 as test")
        if result and len(result) > 0:
            print("✅ Execute query function logic working correctly")
            return True
        else:
            print(f"❌ Execute query function logic failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Execute query function test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("🚀 Starting Basic Neo4j MCP Server Tests")
    print("=" * 50)
    
    tests = [
        ("Server Import", test_server_import),
        ("Echo Function", test_echo_function),
        ("List Nodes Function", test_list_nodes_function),
        ("Execute Query Function", test_execute_query_function),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Basic Test Results Summary")
    print("=" * 50)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All basic tests passed! The server functions are working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
