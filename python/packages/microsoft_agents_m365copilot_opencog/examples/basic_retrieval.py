#!/usr/bin/env python
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
Basic example of using OpenCog with Microsoft 365 Copilot APIs.

This example demonstrates:
1. Setting up the OpenCog Copilot client
2. Retrieving data from M365 Copilot
3. Converting results to OpenCog AtomSpace
4. Querying the knowledge graph
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
    print("OpenCog Integration with Microsoft 365 Copilot APIs")
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

    # Retrieve data and convert to AtomSpace
    print("\n2. Retrieving data from M365 Copilot...")
    query = "What are the latest updates in my organization?"
    
    try:
        atom_space = await client.retrieve_to_atomspace(
            query=query,
            data_source="SharePoint"
        )
        print(f"   ✓ Retrieved data and converted to AtomSpace")

        # Display atoms in the knowledge graph
        print("\n3. Exploring the AtomSpace knowledge graph...")
        all_atoms = client.get_all_atoms()
        
        if all_atoms:
            print(f"   Found {len(all_atoms)} atoms in the knowledge graph:")
            for i, atom in enumerate(all_atoms[:5], 1):  # Show first 5
                print(f"   {i}. {atom}")
            if len(all_atoms) > 5:
                print(f"   ... and {len(all_atoms) - 5} more")
        else:
            print("   No atoms found in the knowledge graph")

        # Query the knowledge graph
        print("\n4. Querying the knowledge graph...")
        # Example query for documents
        results = client.query_knowledge_graph("!(match &self (: $x Document) $x)")
        if results:
            print(f"   Found {len(results)} document nodes:")
            for i, result in enumerate(results[:3], 1):
                print(f"   {i}. {result}")
        else:
            print("   No documents found in query")

        # Get statistics
        print("\n5. Knowledge graph statistics...")
        stats = client.get_graph_statistics()
        print(f"   Entities: {stats.get('entity_count', 0)}")
        print(f"   Relationships: {stats.get('relationship_count', 0)}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
