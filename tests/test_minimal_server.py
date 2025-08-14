#!/usr/bin/env python3
"""
Test the minimal server
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_minimal_server():
    """Test the minimal server."""
    
    print("🧪 Testing minimal server...")
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "minimal_server.py"],
        env={"PYTHONPATH": "."},
        cwd="."
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected to minimal server!")
                
                # List available tools
                tools_result = await session.list_tools()
                print(f"✅ Found {len(tools_result.tools)} tools:")
                
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test the echo tool
                print("\n🧪 Testing test_echo tool...")
                echo_result = await session.call_tool("test_echo", arguments={"message": "Hello from test!"})
                print(f"✅ Echo result: {echo_result.content[0].text}")
                
                # Test the add tool
                print("\n🧪 Testing test_add tool...")
                add_result = await session.call_tool("test_add", arguments={"a": 5, "b": 3})
                print(f"✅ Add result: {add_result.content[0].text}")
                
                print("\n🎉 Minimal server test passed!")
                return True
                
    except Exception as e:
        print(f"❌ Minimal server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_minimal_server())
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!")
