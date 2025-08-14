#!/usr/bin/env python3
"""
Quick test to verify the server is working
"""

import os
import sys

def test_server():
    """Test if the server can be imported and run."""
    
    print("Testing server import...")
    
    try:
        # Import the server module
        import server
        print("✅ Server imported successfully")
        
        # Check if environment variables are loaded
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        neo4j_database = os.getenv("NEO4J_DATABASE")
        
        print(f"✅ NEO4J_URI: {neo4j_uri}")
        print(f"✅ NEO4J_USER: {neo4j_user}")
        print(f"✅ NEO4J_DATABASE: {neo4j_database}")
        print(f"✅ NEO4J_PASSWORD: {'*' * len(neo4j_password) if neo4j_password else 'Not set'}")
        
        # Test the list_nodes function directly
        print("\nTesting list_nodes function...")
        result = server.list_nodes()
        print(f"✅ list_nodes result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_server()
    if success:
        print("\n🎉 Server is working correctly!")
    else:
        print("\n❌ Server has issues")
        sys.exit(1)
