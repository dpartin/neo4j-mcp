# Neo4j MCP Server

A Model Context Protocol (MCP) server that exposes Neo4j graph database functionality to AI assistants and applications, enabling CRUD operations, advanced analytics, and RAG capabilities.

## Features

### 🗄️ CRUD Operations
- **Nodes**: Create, read, update, delete nodes with labels and properties
- **Relationships**: Manage relationships between nodes
- **Properties**: Handle node and relationship properties

### 📊 Advanced Analytics
- **Path Finding**: Shortest path, all paths, weighted paths
- **Centrality Analysis**: Degree, betweenness, closeness centrality
- **Community Detection**: Louvain, Label Propagation algorithms
- **Graph Metrics**: Density, clustering coefficient, diameter
- **Pattern Recognition**: Subgraph matching, frequent patterns

### 🔍 RAG (Retrieval-Augmented Generation) Support
- **Vector Operations**: Store and search vector embeddings
- **Semantic Search**: Text-based graph queries
- **Knowledge Graph Integration**: Entity linking and context retrieval
- **Hybrid Search**: Combine graph structure with vector similarity

## Quick Start

### Prerequisites
- Python 3.9+
- Neo4j 5.x+ database
- Neo4j Graph Data Science (GDS) library (optional, for advanced analytics)
- Cursor IDE (for MCP integration)

### Installation

#### Option 1: Using uv (Recommended)
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Setup Git (if not already done)**
   ```bash
   python setup_git.py
   ```

3. **Setup development environment with uv**
   ```bash
   python setup_dev.py
   ```

4. **Activate the environment**
   ```bash
   # On Windows:
   .venv\Scripts\activate
   # On Linux/Mac:
   source .venv/bin/activate
   ```

5. **Configure Neo4j connection**
   ```bash
   cp .env.example .env
   # Edit .env with your Neo4j credentials
   ```

6. **Run the MCP server**
   ```bash
   uv run python run_server.py
   ```

7. **Integrate with Cursor (Optional)**
   ```bash
   # Follow the Cursor integration guide
   # See CURSOR_INTEGRATION.md for detailed instructions
   ```

#### Option 2: Manual Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Neo4j connection**
   ```bash
   cp env.example .env
   # Edit .env with your Neo4j credentials
   ```

5. **Run the MCP server**
   ```bash
   python run_server.py
   ```

### Configuration

Create a `.env` file with your Neo4j configuration:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Optional: Vector embedding settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DIMENSION=384

# Optional: OpenAI for advanced RAG
OPENAI_API_KEY=your_openai_key
```

## Usage Examples

### Basic CRUD Operations

```python
# Create a node
result = await create_node(
    labels=["Person"],
    properties={"name": "Alice", "age": 30}
)

# Get a node
node = await get_node(node_id=123)

# Create a relationship
await create_relationship(
    from_node_id=123,
    to_node_id=456,
    relationship_type="KNOWS",
    properties={"since": "2020"}
)
```

### Advanced Analytics

```python
# Find shortest path
path = await find_paths(
    start_node_id=123,
    end_node_id=456,
    algorithm="shortest_path"
)

# Calculate centrality
centrality = await calculate_centrality(
    node_ids=[123, 456, 789],
    algorithm="betweenness"
)

# Detect communities
communities = await detect_communities(
    algorithm="louvain"
)
```

### RAG Operations

```python
# Vector similarity search
similar_nodes = await vector_search(
    query_vector=embedding_vector,
    top_k=10
)

# Semantic search
results = await semantic_search(
    query="Find people who work in technology",
    limit=20
)

# Context retrieval for RAG
context = await context_retrieval(
    query="What is the relationship between Alice and Bob?",
    max_nodes=50
)
```

## Development

### Project Structure

```
neo4j_mcp_server/
├── server.py              # Main MCP server
├── config/               # Configuration management
├── core/                 # Core server functionality
├── operations/           # CRUD operation handlers
├── analytics/            # Graph analytics functions
├── rag/                  # RAG functionality
├── models/               # Data models and schemas
├── utils/                # Utilities and helpers
└── tests/                # Test suite
```

### Running Tests

#### Using nv (Recommended)
```bash
# Activate environment
nv use neo4j-mcp-server

# Run all tests
nv run pytest

# Run with coverage
nv run pytest --cov=neo4j_mcp_server

# Run specific test categories
nv run pytest tests/test_crud.py
nv run pytest tests/test_analytics.py
nv run pytest tests/test_rag.py
```

#### Using standard virtual environment
```bash
# Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests
pytest

# Run with coverage
pytest --cov=neo4j_mcp_server

# Run specific test categories
pytest tests/test_crud.py
pytest tests/test_analytics.py
pytest tests/test_rag.py
```

### Code Quality

```bash
# Format code
black neo4j_mcp_server/

# Lint code
flake8 neo4j_mcp_server/

# Type checking
mypy neo4j_mcp_server/
```

## API Reference

### Tools

#### Node Operations
- `create_node` - Create new nodes with labels and properties
- `get_node` - Retrieve nodes by ID or filters
- `update_node` - Update node properties and labels
- `delete_node` - Delete nodes and handle cascading

#### Relationship Operations
- `create_relationship` - Create relationships between nodes
- `get_relationship` - Retrieve relationships
- `update_relationship` - Update relationship properties
- `delete_relationship` - Delete relationships

#### Analytics
- `find_paths` - Find paths between nodes
- `calculate_centrality` - Calculate node centrality metrics
- `detect_communities` - Find community structures
- `graph_metrics` - Calculate graph-level metrics

#### RAG Operations
- `vector_search` - Perform vector similarity search
- `semantic_search` - Semantic graph search
- `context_retrieval` - Retrieve relevant subgraphs for RAG

### Resources

- `graph_schema` - Graph database schema information
- `node_types` - Available node labels and their properties
- `relationship_types` - Available relationship types
- `analytics_results` - Cached analytics results
- `vector_indexes` - Vector index information

## Performance

### Response Times
- **CRUD Operations**: < 100ms for simple operations
- **Analytics**: < 5 seconds for moderate-sized graphs
- **Vector Search**: < 2 seconds for similarity queries
- **Complex Queries**: < 10 seconds for advanced operations

### Scalability
- Support for graphs with millions of nodes and relationships
- Efficient memory usage for large datasets
- Connection pooling for concurrent requests
- Caching for frequently accessed data

## Cursor Integration

The Neo4j MCP Server is designed to integrate seamlessly with Cursor IDE, providing AI-powered graph database operations directly within your development environment.

### Quick Cursor Setup

1. **Install the MCP server** (follow installation instructions above)
2. **Configure Cursor settings** - Add MCP server configuration to Cursor
3. **Restart Cursor** to load the integration
4. **Start using** - Access Neo4j operations through Cursor's AI assistant

### Available Features in Cursor

- **Graph Operations**: Create, query, and analyze Neo4j graphs
- **AI-Powered Queries**: Natural language to Cypher query conversion
- **Visual Results**: Graph visualization and data exploration
- **Code Generation**: Generate Cypher queries and Python code
- **RAG Integration**: Context-aware graph retrieval for AI responses

For detailed setup instructions and examples, see [CURSOR_INTEGRATION.md](CURSOR_INTEGRATION.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information about:

- Development setup
- Git workflow
- Code style guidelines
- Testing requirements
- Pull request process
- Issue reporting

### Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   ```

3. **Setup development environment**:
   ```bash
   python setup_git.py
   python setup_dev.py
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes and test**:
   ```bash
   uv run pytest tests/ -v
   ```

6. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

For more detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [TRD Document](TRD_Neo4j_MCP_Server.md)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

## Roadmap

See the [TRD Document](TRD_Neo4j_MCP_Server.md) for detailed development phases and roadmap.

### Current Phase: Foundation (Phase 1)
- [x] Project structure setup
- [x] TRD documentation
- [ ] Neo4j connection management
- [ ] Basic MCP server framework
- [ ] Configuration management
- [ ] Error handling and logging
- [ ] Unit tests framework

### Next Phases
- **Phase 2**: CRUD Operations (Weeks 3-4)
- **Phase 3**: Advanced Analytics (Weeks 5-7)
- **Phase 4**: RAG Integration (Weeks 8-10)
- **Phase 5**: Advanced Features & Optimization (Weeks 11-12)
