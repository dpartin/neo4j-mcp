#!/usr/bin/env python3
"""
Manual verification script for the MCP server
Run this script to test if the server is working correctly
"""

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def verify_mcp_server():
    """Verify that the MCP server is working correctly."""
    
    print("🔍 Verifying Neo4j MCP Server...")
    print("=" * 50)
    
    # Test 1: Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("❌ .env file missing - run setup_env.py first")
        return False
    
    # Test 2: Check if environment variables are loaded
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        neo4j_database = os.getenv("NEO4J_DATABASE")
        
        if all([neo4j_uri, neo4j_user, neo4j_password, neo4j_database]):
            print("✅ Environment variables loaded correctly")
        else:
            print("❌ Some environment variables are missing")
            return False
    except Exception as e:
        print(f"❌ Error loading environment variables: {e}")
        return False
    
    # Test 3: Test MCP server connection
    print("\n🧪 Testing MCP server connection...")
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "server.py"],
        env={"PYTHONPATH": "."},
        cwd="."
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ MCP client connected successfully!")
                
                # List available tools
                tools_result = await session.list_tools()
                print(f"✅ Found {len(tools_result.tools)} tools:")
                
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test the list_nodes tool specifically
                print(f"\n🧪 Testing mcp_neo4j-mcp-server_list_nodes...")
                list_result = await session.call_tool("list_nodes", arguments={})
                print(f"✅ Tool result: {list_result.content[0].text}")
                
                print("\n🎉 MCP server is working correctly!")
                print("📋 Tool names for Cursor:")
                print("   - mcp_neo4j-mcp-server_list_nodes")
                print("   - mcp_neo4j-mcp-server_echo")
                print("   - mcp_neo4j-mcp-server_create_node")
                print("   - etc.")
                
                return True
                
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    try:
        success = asyncio.run(verify_mcp_server())
        if success:
            print("\n✅ All tests passed! The server is ready for Cursor.")
            print("💡 Try restarting Cursor and using mcp_neo4j-mcp-server_list_nodes")
        else:
            print("\n❌ Tests failed. Check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
