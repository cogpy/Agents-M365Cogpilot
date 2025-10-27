#!/usr/bin/env python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
Knowledge graph building example with OpenCog and M365 Copilot.

This example demonstrates:
1. Building a knowledge graph from M365 data
2. Extracting entities and relationships
3. Inferring implicit connections
4. Analyzing the graph structure
"""
import asyncio
import os
from datetime import datetime

from azure.identity import DeviceCodeCredential
from dotenv import load_dotenv

from microsoft_agents_m365copilot_opencog import OpenCogCopilotClient

# Load environment variables
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")


def auth_callback(verification_uri: str, user_code: str, expires_on: datetime):
    """Callback for device code authentication."""
    print(f"\nTo sign in, use a web browser to open the page {verification_uri}")
    print(f"Enter the code {user_code} to authenticate.")
    print(f"The code will expire at {expires_on}")


async def main():
    """Main example function."""
    print("=" * 80)
    print("Knowledge Graph Builder with OpenCog and M365 Copilot")
    print("=" * 80)
    
    # Create credentials
    credentials = DeviceCodeCredential(
        client_id=CLIENT_ID,
        tenant_id=TENANT_ID,
        prompt_callback=auth_callback
    )

    # Create OpenCog-enabled Copilot client
    print("\n1. Initializing OpenCog Copilot client...")
    client = OpenCogCopilotClient(
        credentials=credentials,
        scopes=['https://graph.microsoft.com/.default']
    )
    print("   ✓ Client initialized")

    # Build knowledge graph
    print("\n2. Building knowledge graph from M365 data...")
    query = "recent projects and documents"
    
    try:
        # Build graph with relationship inference
        knowledge_graph = await client.build_knowledge_graph(
            query=query,
            data_source="SharePoint",
            infer_relationships=True
        )
        print(f"   ✓ Knowledge graph built")

        # Get and display statistics
        print("\n3. Analyzing knowledge graph structure...")
        stats = client.get_graph_statistics()
        
        print(f"\n   Graph Statistics:")
        print(f"   ─────────────────")
        print(f"   Entities:      {stats['entity_count']}")
        print(f"   Relationships: {stats['relationship_count']}")

        # Display entities
        if stats['entities']:
            print(f"\n   Sample Entities:")
            for i, entity in enumerate(stats['entities'][:10], 1):
                print(f"   {i}. {entity}")
            if len(stats['entities']) > 10:
                print(f"   ... and {len(stats['entities']) - 10} more")

        # Display relationships
        if stats['relationships']:
            print(f"\n   Sample Relationships:")
            for i, (source, rel, target) in enumerate(stats['relationships'][:5], 1):
                print(f"   {i}. {source} --[{rel}]--> {target}")
            if len(stats['relationships']) > 5:
                print(f"   ... and {len(stats['relationships']) - 5} more")

        # Query specific patterns
        print("\n4. Querying for specific patterns...")
        
        # Example: Find all entities
        entities = client.query_knowledge_graph("!(match &self (: $x Entity) $x)")
        if entities:
            print(f"   Found {len(entities)} entity nodes")
        
        print("\n5. Knowledge graph ready for reasoning!")
        print("   You can now:")
        print("   - Apply pattern matching")
        print("   - Perform inference")
        print("   - Extract insights")
        print("   - Build on the knowledge base")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
