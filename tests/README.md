# Neo4j MCP Server Tests

This directory contains comprehensive tests for the Neo4j MCP Server.

## Test Structure

### Primary Test Files

- **`test_basic.py`** - Basic functionality tests (recommended - tests server logic directly)
- **`test_suite.py`** - Comprehensive test suite with MCP client (may have connection issues)
- **`verify_mcp.py`** - Manual verification script for MCP server functionality
- **`setup_env.py`** - Environment setup and configuration helper

### Legacy Test Files (Kept for Reference)

- **`test_minimal_server.py`** - Tests for minimal server implementation
- **`test_final_mcp.py`** - Final MCP integration tests
- **`test_dotenv_server.py`** - Environment variable loading tests
- **`test_simple_server.py`** - Simple server functionality tests
- **`debug_server.py`** - Debug server implementation
- **`minimal_server.py`** - Minimal server for testing
- **`simple_test.py`** - Simple connection tests
- **`quick_test.py`** - Quick functionality tests

## Running Tests

### Run the Basic Tests (Recommended)

```bash
cd tests
uv run python test_basic.py
```

### Run the Complete Test Suite

```bash
cd tests
uv run python test_suite.py
```

### Run Individual Tests

```bash
# Verify MCP server
uv run python verify_mcp.py

# Setup environment
uv run python setup_env.py
```

## Test Coverage

The test suite covers:

1. **Environment Setup**
   - .env file existence
   - Environment variable loading
   - Configuration validation

2. **MCP Connection**
   - Server startup
   - Client connection
   - Tool discovery

3. **Core Tools**
   - Echo tool functionality
   - List nodes tool
   - Create node tool
   - Execute query tool

4. **Error Handling**
   - Connection failures
   - Invalid queries
   - Missing parameters

## Test Results

Tests will output:
- ✅ PASS for successful tests
- ❌ FAIL for failed tests
- Detailed error messages for debugging

## Prerequisites

- Neo4j database running
- .env file configured
- All dependencies installed via `uv sync`

## Troubleshooting

If tests fail:

1. Check Neo4j database is running
2. Verify .env file exists and is configured
3. Run `uv sync` to ensure dependencies are installed
4. Check server logs for detailed error messages
