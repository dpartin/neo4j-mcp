#!/usr/bin/env python3
"""
Verify that the MCP server is ready for Cursor
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def verify_cursor_mcp():
    """Verify the MCP server is ready for Cursor."""
    
    print("🔍 Verifying MCP server for Cursor...")
    print("=" * 50)
    
    # Use the exact same configuration as Cursor
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "server.py"],
        env={
            "PYTHONPATH": "E:\\Projects\\neo4j_mcp",
            "NEO4J_URI": "bolt://localhost:7687",
            "NEO4J_USER": "neo4j",
            "NEO4J_PASSWORD": "C0wb0ys1!",
            "NEO4J_DATABASE": "neo4j",
            "LOG_LEVEL": "INFO",
            "DEBUG": "false"
        },
        cwd="E:\\Projects\\neo4j_mcp"
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
                
                print("\n📋 Available tools for Cursor:")
                print("=" * 40)
                for tool in tools_result.tools:
                    cursor_tool_name = f"mcp_neo4j-mcp-server_{tool.name}"
                    print(f"  {cursor_tool_name}")
                    print(f"    Description: {tool.description}")
                    print()
                
                # Test the list_nodes tool specifically
                print("🧪 Testing mcp_neo4j-mcp-server_list_nodes...")
                list_result = await session.call_tool("list_nodes", arguments={})
                print(f"✅ Tool result: {list_result.content[0].text}")
                
                print("\n🎉 MCP server is ready for Cursor!")
                print("\n📋 Next steps:")
                print("1. Restart Cursor completely")
                print("2. Try typing: mcp_neo4j-mcp-server_list_nodes")
                print("3. The tool should now work and return node information")
                
                return True
                
    except Exception as e:
        print(f"❌ MCP verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    try:
        success = asyncio.run(verify_cursor_mcp())
        if success:
            print("\n✅ Verification completed successfully!")
        else:
            print("\n❌ Verification failed!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
