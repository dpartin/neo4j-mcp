#!/usr/bin/env python3
"""
Simple test to verify the server can start properly
"""

import subprocess
import time
import os

def test_server_startup():
    """Test if the server can start properly."""
    
    print("🧪 Testing server startup...")
    
    try:
        # Start the server in a subprocess using uv run
        process = subprocess.Popen(
            ["uv", "run", "python", "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Server started successfully and is running")
            
            # Terminate the process
            process.terminate()
            process.wait()
            print("✅ Server terminated cleanly")
        else:
            # Get output if the process failed
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            
    except Exception as e:
        print(f"❌ Error testing server startup: {e}")

def test_environment_variables():
    """Test if environment variables are loaded correctly."""
    
    print("\n🧪 Testing environment variables...")
    
    try:
        # Import the server module to trigger dotenv loading
        import server
        
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
            print("✅ All environment variables loaded correctly")
        else:
            print("⚠️  Some environment variables are missing")
            
    except Exception as e:
        print(f"❌ Error testing environment variables: {e}")

def main():
    """Main test function."""
    
    print("🚀 Simple Server Test")
    print("=" * 30)
    
    test_environment_variables()
    test_server_startup()

if __name__ == "__main__":
    main()
