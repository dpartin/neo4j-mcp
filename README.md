# Neo4j MCP Server

A production-ready Model Context Protocol (MCP) server for Neo4j graph database operations. This server provides comprehensive tools for creating, reading, updating, and deleting nodes and relationships in Neo4j, as well as executing custom Cypher queries with full data formatting.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete nodes and relationships
- **Custom Queries**: Execute any Cypher query with parameters and formatted results
- **Real Database Connection**: Proven connection logic with robust error handling
- **FastMCP Implementation**: Built with FastMCP 2.0 for optimal performance
- **Data Formatting**: Properly formatted results with actual data display
- **Environment Management**: Secure configuration via .env files
- **Comprehensive Testing**: Full test suite with automated validation
- **Advanced Analytics**: Graph analytics including centrality, community detection, and path analysis
- **RAG Support**: Retrieval-Augmented Generation with vector search and semantic similarity

## 📋 Prerequisites

- Python 3.8+
- Neo4j database running locally or remotely
- `uv` package manager (**required for MCP configuration**) or `pip` (requires manual mcp.json modification)
- **Optional**: Neo4j Graph Data Science (GDS) library for advanced algorithms (see [GDS Installation Guide](GDS_INSTALLATION_GUIDE.md))

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```
   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**:
     ```bash
   cd tests
   uv run python setup_env.py
   ```

## ⚙️ Configuration

### Environment Variables

The server uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j

# Logging Configuration
LOG_LEVEL=INFO
DEBUG=false

# MCP Server Configuration
MCP_SERVER_NAME=neo4j-mcp-server
```

### MCP Configuration

The `mcp.json` file is configured for Cursor integration using **UV** for environment and package management:

```json
{
  "mcpServers": {
    "neo4j-mcp-server": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "env": {
        "PYTHONPATH": "E:\\Projects\\neo4j_mcp",
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "your-password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

> **⚠️ Important Note**: This MCP configuration requires **UV** for environment and package management. If you're using a different package manager (conda, pip, etc.), you'll need to modify the `command` and `args` in the `mcp.json` file to work with your specific package manager.
>
> **Examples for other package managers:**
> - **pip**: `"command": "python", "args": ["server.py"]`
> - **conda**: `"command": "conda", "args": ["run", "-n", "your-env", "python", "server.py"]`
> - **poetry**: `"command": "poetry", "args": ["run", "python", "server.py"]`

## 🏃‍♂️ Running the Server

### Start the MCP Server

```bash
uv run python server.py
```

The server will:
- ✅ Load environment variables from .env file
- ✅ Test Neo4j connection on startup
- ✅ Start the MCP server with stdio transport
- ✅ Display formatted results with actual data

### Expected Output

```
Loaded environment variables from .env file
INFO:__main__:DEBUG: Connecting to Neo4j at bolt://localhost:7687 as neo4j to database neo4j
```

## 🛠️ Available Tools

### Core Operations

- **`echo(message: str)`** - Echo back a message (for testing)
- **`create_node(labels: List[str], properties: Optional[Dict])`** - Create a new node
- **`list_nodes(label: Optional[str])`** - List nodes with formatted results
- **`create_relationship(from_node_id: str, to_node_id: str, relationship_type: str, properties: Optional[Dict])`** - Create a relationship
- **`execute_query(query: str, parameters: Optional[Dict])`** - Execute custom Cypher queries with formatted results

### Advanced Operations

- **`get_node(node_id: Optional[int], labels: Optional[List[str]], properties: Optional[Dict])`** - Get nodes by criteria
- **`update_node(node_id: int, properties: Optional[Dict], labels: Optional[List[str]])`** - Update a node
- **`delete_node(node_id: int, cascade: bool)`** - Delete a node

### Advanced Analytics

- **`graph_analytics(analysis_type: str, node_label: Optional[str], relationship_type: Optional[str])`** - Perform graph analytics
  - `degree_centrality` - Find nodes with highest connections
  - `betweenness_centrality` - Find nodes that act as bridges (GDS or APOC)
  - `community_detection` - Detect communities in the graph (GDS Louvain or native)
  - `pagerank` - Measure node importance and influence (GDS or APOC)
  - `node_similarity` - Find similar nodes based on relationships (GDS or native)
  - `clustering_coefficient` - Measure local clustering (GDS or APOC)
  - `path_analysis` - Analyze shortest paths between nodes
- **`graph_statistics()`** - Get comprehensive graph statistics

### Graph Data Science (GDS) Support

- **`create_graph_projection(graph_name: str, node_labels: Optional[List[str]], relationship_types: Optional[List[str]])`** - Create graph projections for GDS algorithms
- **`list_graph_projections()`** - List all available graph projections
- **`drop_graph_projection(graph_name: str)`** - Drop a graph projection

**GDS Algorithms Available** (when Neo4j GDS library is installed):
- **Louvain Community Detection**: Advanced modularity-based clustering
- **GDS PageRank**: Optimized PageRank implementation
- **GDS Betweenness Centrality**: Fast betweenness computation
- **GDS Node Similarity**: Efficient similarity algorithms
- **GDS Local Clustering Coefficient**: Advanced clustering metrics

**Fallback Algorithms** (when GDS not available):
- **APOC PageRank**: Uses APOC library algorithms
- **Native Cypher**: Uses built-in Cypher queries
- **APOC Triangle Count**: Basic clustering coefficient

### RAG (Retrieval-Augmented Generation)

- **`create_vector_index(index_name: str, node_label: str, property_name: str, dimensions: int)`** - Create vector index for semantic search
- **`semantic_search(query_vector: List[float], index_name: str, limit: int)`** - Perform semantic search using vector similarity
- **`hybrid_search(text_query: str, node_label: str, vector_property: str, text_properties: List[str], limit: int)`** - Combine text and vector search
- **`create_embedding_node(node_label: str, name: str, description: str, embedding: List[float])`** - Create nodes with embeddings
- **`rag_context_retrieval(query: str, node_label: str, context_properties: List[str], limit: int)`** - Retrieve relevant context for RAG

## 🧪 Testing

### Run Complete Test Suite

```bash
cd tests
uv run python test_suite.py
```

### Run Individual Tests

```bash
# Verify MCP server functionality
uv run python verify_mcp.py

# Setup environment
uv run python setup_env.py
```

## 📊 Test Results

The test suite will output:
- ✅ PASS for successful tests
- ❌ FAIL for failed tests
- Detailed error messages for debugging

## 🔧 Recent Improvements

### ✅ Implemented Features

1. **Data Formatting**: Added proper result formatting with actual data display
2. **Environment Management**: Secure configuration via .env files with python-dotenv
3. **Comprehensive Testing**: Full test suite with automated validation
4. **Tool Consolidation**: All tests organized in `/tests` directory
5. **Error Handling**: Robust error handling with real error messages
6. **Connection Logic**: Proven connection logic with proper driver lifecycle management
7. **GDS Integration**: Full Graph Data Science library support with verified functionality
8. **Advanced Analytics**: Comprehensive graph analytics with GDS algorithms and fallbacks
9. **MLB Database**: Complete 2025 MLB season database with teams, games, players, and box scores
10. **Community Detection**: Working Louvain community detection with realistic team clustering

### 🔄 Key Improvements

- **Data Display**: Tools now show actual formatted data instead of just success messages
- **Environment Setup**: Automated .env file creation and validation
- **Test Organization**: Consolidated all tests into a structured test suite
- **Documentation**: Updated installation and configuration instructions

## 📁 Project Structure

```
neo4j_mcp/
├── server.py                 # Main MCP server implementation
├── mcp.json                  # MCP configuration for Cursor
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── LICENSE                  # MIT License
├── TRD_Neo4j_MCP_Server.md  # Technical Requirements Document
├── tests/                   # Test suite directory
│   ├── test_suite.py        # Comprehensive test suite
│   ├── verify_mcp.py        # MCP server verification
│   ├── setup_env.py         # Environment setup helper
│   └── README.md           # Test documentation
└── .env                     # Environment variables (created by setup)
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**: Ensure Neo4j is running and credentials are correct
2. **MCP Tools Not Responding**: Restart the MCP server and Cursor
3. **Environment Variables**: Check that `.env` file exists and is configured
4. **Test Failures**: Run the test suite to identify specific issues

### Debug Steps

1. **Run Test Suite**: `cd tests && uv run python test_suite.py`
2. **Check Environment**: `cd tests && uv run python setup_env.py`
3. **Verify MCP Server**: `cd tests && uv run python verify_mcp.py`
4. **Check Server Logs**: Look for connection messages in server output

## 🚀 Usage Examples

### Using with Cursor

Once configured, you can use the MCP tools in Cursor:

```
mcp_neo4j-mcp-server_list_nodes
mcp_neo4j-mcp-server_create_node
mcp_neo4j-mcp-server_execute_query
```

### Example Queries

```cypher
# Create a movie node
CREATE (m:Movie {title: 'Dune', director: 'Denis Villeneuve', year: 2021})

# List all movies
MATCH (m:Movie) RETURN m.title, m.director, m.year

# Find relationships
MATCH (m1:Movie)-[r:SIMILAR_GENRE]->(m2:Movie) RETURN m1.title, m2.title
```

### Advanced Analytics Examples

```python
# Degree centrality analysis
mcp_neo4j-mcp-server_graph_analytics(analysis_type="degree_centrality", node_label="Movie")

# Community detection (GDS Louvain or native fallback)
mcp_neo4j-mcp-server_graph_analytics(analysis_type="community_detection")

# PageRank analysis (GDS or APOC fallback)
mcp_neo4j-mcp-server_graph_analytics(analysis_type="pagerank")

# Node similarity (GDS or native fallback)
mcp_neo4j-mcp-server_graph_analytics(analysis_type="node_similarity")

# Clustering coefficient (GDS or APOC fallback)
mcp_neo4j-mcp-server_graph_analytics(analysis_type="clustering_coefficient")

# Path analysis
mcp_neo4j-mcp-server_graph_analytics(analysis_type="path_analysis", relationship_type="STARRED_IN")

# Get graph statistics
mcp_neo4j-mcp-server_graph_statistics()
```

### Graph Data Science (GDS) Examples

```python
# Create a graph projection for GDS algorithms
mcp_neo4j-mcp-server_create_graph_projection(graph_name="movie_actor_graph", node_labels=["Movie", "Actor"], relationship_types=["STARRED_IN"])

# List available graph projections
mcp_neo4j-mcp-server_list_graph_projections()

# Run GDS algorithms on the projection
mcp_neo4j-mcp-server_graph_analytics(analysis_type="community_detection")  # Uses GDS Louvain
mcp_neo4j-mcp-server_graph_analytics(analysis_type="pagerank")  # Uses GDS PageRank

# Drop a graph projection when done
mcp_neo4j-mcp-server_drop_graph_projection(graph_name="movie_actor_graph")
```

### RAG Examples

```python
# Create vector index
mcp_neo4j-mcp-server_create_vector_index(index_name="movie_embeddings", node_label="Movie", property_name="embedding")

# Semantic search
mcp_neo4j-mcp-server_semantic_search(query_vector=[0.1, 0.2, ...], index_name="movie_embeddings")

# Hybrid search
mcp_neo4j-mcp-server_hybrid_search(text_query="sci-fi", node_label="Movie", vector_property="embedding", text_properties=["title", "description"])

# RAG context retrieval
mcp_neo4j-mcp-server_rag_context_retrieval(query="space exploration", node_label="Movie", context_properties=["title", "description"])
```

## 🤝 Contributing

This is a production-ready implementation with comprehensive testing and documentation. The project follows best practices for MCP development and Neo4j integration.

## 📄 License

This project is open source and available under the MIT License.
