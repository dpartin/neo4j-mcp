#!/usr/bin/env python3
"""
Final test to verify the MCP server is working correctly with dotenv
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_final_mcp():
    """Test the MCP server with the final configuration."""
    
    print("🧪 Final MCP Server Test")
    print("=" * 40)
    
    # Set up server parameters (same as mcp.json)
    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "python",
            "server.py"
        ],
        env={
            "PYTHONPATH": ".",
        },
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
                
                # Test calling the list_nodes tool
                print("\n🧪 Testing list_nodes tool...")
                list_result = await session.call_tool("list_nodes", arguments={})
                print(f"✅ List nodes result: {list_result.content[0].text}")
                
                # Test calling the echo tool
                print("\n🧪 Testing echo tool...")
                echo_result = await session.call_tool("echo", arguments={"message": "Hello from final test!"})
                print(f"✅ Echo result: {echo_result.content[0].text}")
                
                print("\n🎉 All tests passed! The server is working correctly with dotenv.")
                
    except Exception as e:
        print(f"❌ MCP client test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_final_mcp())
