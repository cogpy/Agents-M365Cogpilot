# Microsoft 365 Copilot APIs OpenCog Integration

This package provides an integration layer between Microsoft 365 Copilot APIs and OpenCog, enabling knowledge graph-based AI reasoning with M365 data.

## Overview

The OpenCog integration allows you to:
- Convert Microsoft 365 Copilot retrieval results into OpenCog AtomSpace knowledge graphs
- Use OpenCog's reasoning capabilities with data from M365 services
- Build AGI applications that leverage both Microsoft 365 Copilot APIs and OpenCog's cognitive framework

## Installation

```bash
pip install microsoft-agents-m365copilot-opencog
```

This package requires:
- `microsoft-agents-m365copilot-beta` - For accessing Microsoft 365 Copilot APIs
- `hyperon` - OpenCog Hyperon for knowledge representation and reasoning

## Quick Start

```python
import asyncio
from azure.identity import DeviceCodeCredential
from microsoft_agents_m365copilot_opencog import OpenCogCopilotClient

# Set up credentials
credentials = DeviceCodeCredential(
    client_id="YOUR_CLIENT_ID",
    tenant_id="YOUR_TENANT_ID"
)

# Create OpenCog-enabled Copilot client
client = OpenCogCopilotClient(credentials=credentials)

async def main():
    # Retrieve data and convert to AtomSpace
    atom_space = await client.retrieve_to_atomspace(
        query="What are the latest updates?",
        data_source="SharePoint"
    )
    
    # Access atoms in the knowledge graph
    for atom in atom_space.get_atoms_by_type("ConceptNode"):
        print(atom)

asyncio.run(main())
```

## Features

### AtomSpace Adapter
Converts M365 Copilot retrieval results into OpenCog AtomSpace format:
- Documents become `ConceptNode` atoms
- Relationships become `Link` atoms
- Metadata is preserved as atom properties

### Knowledge Graph Builder
Build rich knowledge graphs from M365 data:
- Automatic entity extraction
- Relationship inference
- Semantic linking

### Reasoning Integration
Apply OpenCog reasoning to M365 data:
- Pattern matching over organizational knowledge
- Inference and deduction
- Knowledge synthesis

## Architecture

The integration consists of:

1. **OpenCogCopilotClient**: Main client that wraps the M365 Copilot API client with OpenCog capabilities
2. **AtomSpaceAdapter**: Converts between M365 Copilot data models and OpenCog AtomSpace
3. **KnowledgeGraphBuilder**: Builds rich knowledge graphs from retrieval results
4. **ReasoningEngine**: Applies OpenCog reasoning over M365 data

## Examples

See the `examples/` directory for complete examples:
- `basic_retrieval.py` - Basic retrieval and AtomSpace conversion
- `knowledge_graph.py` - Building knowledge graphs from M365 data
- `reasoning.py` - Applying reasoning to organizational knowledge

## Contributing

This project welcomes contributions and suggestions. See the main repository [CONTRIBUTING.md](https://github.com/microsoft/Agents-M365Copilot) for details.

## License

MIT License - see LICENSE file for details.
