# OpenCog Integration Guide

This guide provides detailed information on how to use the OpenCog integration with Microsoft 365 Copilot APIs.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Core Concepts](#core-concepts)
5. [Getting Started](#getting-started)
6. [Advanced Usage](#advanced-usage)
7. [API Reference](#api-reference)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

## Introduction

The OpenCog integration for Microsoft 365 Copilot APIs brings together two powerful technologies:

- **Microsoft 365 Copilot APIs**: Access to organizational knowledge and data
- **OpenCog Hyperon**: Advanced AGI framework with knowledge graphs and reasoning

This integration enables you to:
- Build knowledge graphs from M365 data
- Apply AI reasoning to organizational knowledge
- Extract entities and relationships
- Perform pattern matching and inference
- Create intelligent AI applications

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.9 or higher** installed
2. **Microsoft 365 Copilot license** for your tenant
3. **Azure AD app registration** with appropriate permissions
4. **Basic understanding** of async Python programming

## Installation

### Using pip

```bash
pip install microsoft-agents-m365copilot-opencog
```

This will install:
- `microsoft-agents-m365copilot-beta` (dependency)
- `microsoft-agents-m365copilot-core` (dependency)
- `hyperon` (OpenCog Hyperon, dependency)

### From source

```bash
git clone https://github.com/microsoft/Agents-M365Copilot.git
cd Agents-M365Copilot/python/packages/microsoft_agents_m365copilot_opencog
pip install -e .
```

## Core Concepts

### AtomSpace

AtomSpace is OpenCog's knowledge representation system. It stores knowledge as a hypergraph of "atoms":

- **Nodes**: Represent entities (e.g., documents, people, concepts)
- **Links**: Represent relationships between nodes

### MeTTa

MeTTa is OpenCog Hyperon's programming language for working with AtomSpace. It supports:
- Pattern matching
- Queries
- Reasoning
- Knowledge manipulation

### Knowledge Graph Builder

Automatically constructs knowledge graphs from M365 data:
- Extracts entities from text
- Creates relationships
- Infers implicit connections

## Getting Started

### Basic Setup

```python
import asyncio
from azure.identity import DeviceCodeCredential
from microsoft_agents_m365copilot_opencog import OpenCogCopilotClient

# Set up authentication
credentials = DeviceCodeCredential(
    client_id="YOUR_CLIENT_ID",
    tenant_id="YOUR_TENANT_ID"
)

# Create the client
client = OpenCogCopilotClient(credentials=credentials)
```

### Simple Retrieval to AtomSpace

```python
async def simple_example():
    # Retrieve and convert to AtomSpace
    atom_space = await client.retrieve_to_atomspace(
        query="recent documents",
        data_source="SharePoint"
    )
    
    # Get all atoms
    atoms = client.get_all_atoms()
    print(f"Created {len(atoms)} atoms")

asyncio.run(simple_example())
```

### Building Knowledge Graphs

```python
async def knowledge_graph_example():
    # Build a knowledge graph with inference
    graph = await client.build_knowledge_graph(
        query="project documents and reports",
        data_source="SharePoint",
        infer_relationships=True
    )
    
    # Get statistics
    stats = client.get_graph_statistics()
    print(f"Entities: {stats['entity_count']}")
    print(f"Relationships: {stats['relationship_count']}")

asyncio.run(knowledge_graph_example())
```

## Advanced Usage

### Custom Pattern Matching

Use MeTTa queries to find specific patterns:

```python
# Find all document nodes
documents = client.query_knowledge_graph(
    "!(match &self (: $x Document) $x)"
)

# Find all relationships
relationships = client.query_knowledge_graph(
    "!(match &self ($rel $source $target) ($rel $source $target))"
)
```

### Working with Multiple Data Sources

```python
async def multi_source_example():
    # Retrieve from SharePoint
    sp_graph = await client.build_knowledge_graph(
        query="projects",
        data_source="SharePoint"
    )
    
    # Retrieve from OneDrive
    od_graph = await client.build_knowledge_graph(
        query="projects",
        data_source="OneDrive"
    )
    
    # The graphs are merged in the same AtomSpace
    stats = client.get_graph_statistics()
    print(f"Combined entities: {stats['entity_count']}")
```

### Custom Entity Extraction

Extend the knowledge graph builder with custom logic:

```python
from microsoft_agents_m365copilot_opencog import KnowledgeGraphBuilder

# Create custom builder
builder = KnowledgeGraphBuilder()

# Add custom relationships
builder.add_relationship(
    "entity_project_alpha",
    "managed-by",
    "entity_john_doe"
)

# Build entity nodes
builder._build_entity_nodes()
builder._build_relationship_edges()
```

### Accessing Low-Level Components

Work directly with the AtomSpace adapter:

```python
from microsoft_agents_m365copilot_opencog import AtomSpaceAdapter

adapter = AtomSpaceAdapter()

# Convert retrieval response
retrieval_response = await client.retrieve(query="test")
atom_space = adapter.convert_retrieval_response(retrieval_response)

# Query atoms directly
results = adapter.query_atoms("!(match &self (: $x Entity) $x)")
```

## API Reference

### OpenCogCopilotClient

Main client for OpenCog-enabled M365 Copilot interactions.

#### Methods

**`__init__(credentials, scopes=None, client=None)`**
- Initialize the client
- Parameters:
  - `credentials`: Azure credentials
  - `scopes`: OAuth scopes (optional)
  - `client`: Existing M365 Copilot client (optional)

**`async retrieve_to_atomspace(query, data_source, maximum_results=None)`**
- Retrieve and convert to AtomSpace
- Returns: `GroundingSpace` object

**`async build_knowledge_graph(query, data_source, infer_relationships=True)`**
- Build rich knowledge graph
- Returns: `GroundingSpace` object

**`query_knowledge_graph(pattern)`**
- Query using MeTTa pattern
- Returns: List of matching results

**`get_graph_statistics()`**
- Get graph statistics
- Returns: Dictionary with counts and lists

**`get_all_atoms()`**
- Get all atoms in the graph
- Returns: List of atoms

### AtomSpaceAdapter

Converts M365 data to OpenCog AtomSpace.

#### Methods

**`convert_retrieval_response(retrieval_response)`**
- Convert retrieval response to atoms
- Returns: `GroundingSpace`

**`convert_interaction_history(interactions)`**
- Convert interaction history
- Returns: `GroundingSpace`

**`query_atoms(pattern)`**
- Query atoms with MeTTa pattern
- Returns: List of results

### KnowledgeGraphBuilder

Builds rich knowledge graphs from M365 data.

#### Methods

**`build_from_retrieval(retrieval_response)`**
- Build graph from retrieval
- Returns: `GroundingSpace`

**`add_relationship(source, relation, target)`**
- Manually add relationship

**`infer_relationships()`**
- Infer implicit relationships

**`export_statistics()`**
- Export graph statistics
- Returns: Dictionary

## Examples

See the `examples/` directory for complete examples:

1. **basic_retrieval.py**: Basic retrieval and AtomSpace conversion
2. **knowledge_graph.py**: Building knowledge graphs from M365 data

## Troubleshooting

### Common Issues

**ImportError: No module named 'hyperon'**
- Solution: `pip install hyperon`

**Authentication errors**
- Ensure your app registration has correct permissions
- Check that your tenant has M365 Copilot license
- Verify client ID and tenant ID are correct

**Empty knowledge graphs**
- Check that your query returns results
- Verify data source is accessible
- Ensure proper permissions are granted

**Pattern matching not working**
- Verify MeTTa syntax is correct
- Check that atoms exist in the space
- Use `get_all_atoms()` to debug

### Debug Tips

1. **Enable verbose output**:
   ```python
   # Print all atoms
   atoms = client.get_all_atoms()
   for atom in atoms:
       print(atom)
   ```

2. **Check statistics**:
   ```python
   stats = client.get_graph_statistics()
   print(f"Debug stats: {stats}")
   ```

3. **Test retrieval separately**:
   ```python
   # Test without OpenCog conversion
   response = await client.retrieve(query="test")
   print(f"Response: {response}")
   ```

## Support

For issues and questions:
- [GitHub Issues](https://github.com/microsoft/Agents-M365Copilot/issues)
- [Discussions](https://github.com/microsoft/Agents-M365Copilot/discussions)

## License

MIT License - see LICENSE file for details.
