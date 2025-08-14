#!/usr/bin/env python3
"""
Debug script to identify issues with server.py
"""

import sys
import os

def test_imports():
    """Test each import step by step."""
    
    print("🔍 Debugging server.py imports...")
    print("=" * 40)
    
    # Test 1: Basic Python imports
    try:
        import os
        print("✅ os imported")
    except Exception as e:
        print(f"❌ os import failed: {e}")
        return False
    
    try:
        import logging
        print("✅ logging imported")
    except Exception as e:
        print(f"❌ logging import failed: {e}")
        return False
    
    try:
        from typing import Optional, Dict, Any, List
        print("✅ typing imported")
    except Exception as e:
        print(f"❌ typing import failed: {e}")
        return False
    
    # Test 2: FastMCP import
    try:
        from fastmcp import FastMCP
        print("✅ FastMCP imported")
    except Exception as e:
        print(f"❌ FastMCP import failed: {e}")
        return False
    
    # Test 3: Neo4j import
    try:
        from neo4j import GraphDatabase
        print("✅ GraphDatabase imported")
    except Exception as e:
        print(f"❌ GraphDatabase import failed: {e}")
        return False
    
    # Test 4: dotenv import
    try:
        from dotenv import load_dotenv
        print("✅ dotenv imported")
    except Exception as e:
        print(f"❌ dotenv import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variable loading."""
    
    print("\n🔍 Testing environment variables...")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("❌ .env file missing")
        return False
    
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ dotenv.load_dotenv() executed")
        
        # Check environment variables
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        neo4j_database = os.getenv("NEO4J_DATABASE")
        
        print(f"✅ NEO4J_URI: {neo4j_uri}")
        print(f"✅ NEO4J_USER: {neo4j_user}")
        print(f"✅ NEO4J_DATABASE: {neo4j_database}")
        print(f"✅ NEO4J_PASSWORD: {'*' * len(neo4j_password) if neo4j_password else 'Not set'}")
        
        if all([neo4j_uri, neo4j_user, neo4j_password, neo4j_database]):
            print("✅ All environment variables loaded")
            return True
        else:
            print("❌ Some environment variables missing")
            return False
            
    except Exception as e:
        print(f"❌ Error loading environment variables: {e}")
        return False

def test_fastmcp_server():
    """Test FastMCP server creation."""
    
    print("\n🔍 Testing FastMCP server creation...")
    print("=" * 40)
    
    try:
        from fastmcp import FastMCP
        mcp = FastMCP("neo4j-mcp-server")
        print("✅ FastMCP server created")
        return True
    except Exception as e:
        print(f"❌ FastMCP server creation failed: {e}")
        return False

def test_neo4j_connection():
    """Test Neo4j connection."""
    
    print("\n🔍 Testing Neo4j connection...")
    print("=" * 40)
    
    try:
        from neo4j import GraphDatabase
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "C0wb0ys1!")
        database = os.getenv("NEO4J_DATABASE", "neo4j")
        
        print(f"Connecting to: {uri}")
        print(f"User: {user}")
        print(f"Database: {database}")
        
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session(database=database) as session:
            result = session.run("RETURN 1 as test")
            test_value = result.single()
            print(f"✅ Neo4j connection successful: {test_value['test']}")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        return False

def main():
    """Main debug function."""
    
    print("🚀 Server.py Debug Tool")
    print("=" * 50)
    
    # Test each component
    tests = [
        ("Import Dependencies", test_imports),
        ("Environment Variables", test_environment),
        ("FastMCP Server", test_fastmcp_server),
        ("Neo4j Connection", test_neo4j_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Server.py should work correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\n💡 Common fixes:")
        print("1. Install missing dependencies: pip install fastmcp neo4j python-dotenv")
        print("2. Create .env file: run setup_env.py")
        print("3. Start Neo4j database")
        print("4. Check Neo4j connection details")

if __name__ == "__main__":
    main()
