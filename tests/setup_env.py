#!/usr/bin/env python3
"""
Setup script to create .env file for Neo4j MCP Server
"""

import os

def create_env_file():
    """Create a .env file with default Neo4j configuration."""
    
    env_content = """# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=C0wb0ys1!
NEO4J_DATABASE=neo4j

# Logging Configuration
LOG_LEVEL=INFO
DEBUG=false

# MCP Server Configuration
MCP_SERVER_NAME=neo4j-mcp-server
"""
    
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"⚠️  {env_file} already exists. Skipping creation.")
        return
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file} with default Neo4j configuration")
        print("📝 Please update the password and other settings as needed")
    except Exception as e:
        print(f"❌ Failed to create {env_file}: {e}")

def test_env_loading():
    """Test if environment variables can be loaded properly."""
    
    print("\n🧪 Testing environment variable loading...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if environment variables are loaded
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        neo4j_database = os.getenv("NEO4J_DATABASE")
        
        print(f"✅ NEO4J_URI: {neo4j_uri}")
        print(f"✅ NEO4J_USER: {neo4j_user}")
        print(f"✅ NEO4J_DATABASE: {neo4j_database}")
        print(f"✅ NEO4J_PASSWORD: {'*' * len(neo4j_password) if neo4j_password else 'Not set'}")
        
        if all([neo4j_uri, neo4j_user, neo4j_password, neo4j_database]):
            print("✅ All required environment variables are loaded")
        else:
            print("⚠️  Some environment variables are missing")
            
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    except Exception as e:
        print(f"❌ Error testing environment loading: {e}")

def main():
    """Main setup function."""
    
    print("🚀 Neo4j MCP Server Environment Setup")
    print("=" * 50)
    
    create_env_file()
    test_env_loading()
    
    print("\n📋 Next steps:")
    print("1. Update the .env file with your actual Neo4j credentials")
    print("2. Run the server: python server.py")
    print("3. Test the connection with: python test_neo4j_connection.py")

if __name__ == "__main__":
    main()
