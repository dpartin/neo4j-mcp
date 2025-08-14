# Neo4j Graph Data Science (GDS) Library Installation Guide

## Overview
The Neo4j Graph Data Science library provides advanced graph algorithms for community detection, centrality analysis, similarity algorithms, and more.

## Prerequisites
- Neo4j 5.15.0 (Community or Enterprise Edition)
- Java 11 or higher
- Admin access to Neo4j installation

## Installation Steps

### Step 1: Download GDS Library
1. Go to [Neo4j GDS Downloads](https://neo4j.com/docs/graph-data-science/current/installation/)
2. Download the appropriate version for Neo4j 5.15.0:
   - **Community Edition**: `neo4j-graph-data-science-2.4.x.zip`
   - **Enterprise Edition**: `neo4j-graph-data-science-2.4.x-enterprise.zip`

### Step 2: Install GDS Library
1. Stop Neo4j server:
   ```bash
   neo4j stop
   ```

2. Extract the downloaded ZIP file to Neo4j plugins directory:
   ```bash
   # Windows (typical location)
   C:\Program Files\Neo4j\neo4j-community-5.15.0\plugins\
   
   # Linux/Mac (typical location)
   /usr/local/neo4j/neo4j-community-5.15.0/plugins/
   ```

3. Add GDS configuration to `neo4j.conf`:
   ```conf
   # Enable GDS procedures
   dbms.security.procedures.unrestricted=gds.*
   
   # Memory settings for GDS (adjust based on your system)
   dbms.memory.heap.initial_size=1G
   dbms.memory.heap.max_size=4G
   dbms.memory.pagecache.size=1G
   ```

### Step 3: Verify Installation
1. Start Neo4j server:
   ```bash
   neo4j start
   ```

2. Connect to Neo4j and verify GDS is installed:
   ```cypher
   CALL gds.list() YIELD name, signature, description
   RETURN name, signature, description
   LIMIT 5;
   ```

## Alternative: Using Neo4j Desktop
1. Open Neo4j Desktop
2. Select your database
3. Go to "Plugins" tab
4. Click "Install" next to "Graph Data Science Library"
5. Restart the database

## Available Algorithms

### Community Detection
- **Louvain**: Modularity-based community detection
- **Label Propagation**: Fast community detection
- **Triangle Count**: Count triangles in the graph
- **Local Clustering Coefficient**: Measure local clustering

### Centrality
- **PageRank**: Measure node importance
- **Betweenness Centrality**: Measure node influence
- **Closeness Centrality**: Measure node accessibility
- **Harmonic Centrality**: Alternative closeness measure

### Similarity
- **Node Similarity**: Find similar nodes
- **K-Nearest Neighbors**: Find similar nodes with k parameter

### Path Finding
- **Shortest Path**: Find shortest paths
- **All Pairs Shortest Path**: Find all shortest paths
- **Single Source Shortest Path**: Find paths from one node

### Link Prediction
- **Adamic Adar**: Predict missing relationships
- **Common Neighbors**: Count common neighbors

## Usage Examples

### Community Detection with Louvain
```cypher
// Create a graph projection
CALL gds.graph.project(
  'myGraph',
  ['Movie', 'Actor'],
  ['STARRED_IN']
);

// Run Louvain community detection
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS name, communityId
ORDER BY communityId, name;
```

### PageRank Centrality
```cypher
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10;
```

### Node Similarity
```cypher
CALL gds.nodeSimilarity.stream('myGraph')
YIELD node1, node2, similarity
RETURN 
  gds.util.asNode(node1).name AS actor1,
  gds.util.asNode(node2).name AS actor2,
  similarity
ORDER BY similarity DESC
LIMIT 10;
```

## Memory Requirements
- **Minimum**: 2GB RAM
- **Recommended**: 8GB+ RAM for large graphs
- **Heap**: At least 50% of available RAM
- **Page Cache**: At least 25% of available RAM

## Troubleshooting

### Common Issues
1. **Out of Memory**: Increase heap size in neo4j.conf
2. **Procedure Not Found**: Ensure GDS is properly installed and configured
3. **Permission Denied**: Check dbms.security.procedures.unrestricted setting

### Verification Commands
```cypher
-- Check GDS version
CALL gds.version() YIELD version;

-- List all GDS procedures
CALL gds.list() YIELD name;

-- Check available algorithms
CALL gds.list() YIELD name WHERE name CONTAINS 'louvain';
```

## Next Steps
After installation, you can:
1. Create graph projections for your movie-actor data
2. Run community detection algorithms
3. Analyze actor centrality and influence
4. Find similar actors based on collaboration patterns
5. Perform link prediction for potential future collaborations
