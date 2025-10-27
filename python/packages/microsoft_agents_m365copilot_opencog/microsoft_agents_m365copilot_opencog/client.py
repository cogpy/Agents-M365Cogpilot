# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
OpenCog-enabled Microsoft 365 Copilot API client.
"""
from typing import Any, List, Optional, Union

from azure.core.credentials import TokenCredential
from azure.core.credentials_async import AsyncTokenCredential
from hyperon import GroundingSpace

try:
    from microsoft_agents_m365copilot_beta import (
        AgentsM365CopilotBetaServiceClient,
    )
    from microsoft_agents_m365copilot_beta.generated.copilot.retrieval import (
        retrieval_post_request_body,
    )
    from microsoft_agents_m365copilot_beta.generated.models import (
        retrieval_data_source,
    )
    RetrievalPostRequestBody = (
        retrieval_post_request_body.RetrievalPostRequestBody
    )
    RetrievalDataSource = retrieval_data_source.RetrievalDataSource
except ImportError as e:
    raise ImportError(
        "microsoft-agents-m365copilot-beta is required. "
        "Install it with: pip install microsoft-agents-m365copilot-beta"
    ) from e

from .atomspace_adapter import AtomSpaceAdapter
from .knowledge_graph_builder import KnowledgeGraphBuilder


class OpenCogCopilotClient:
    """
    Microsoft 365 Copilot API client with OpenCog integration.

    This client wraps the standard M365 Copilot client and provides additional
    methods to work with OpenCog knowledge graphs and reasoning.
    """

    def __init__(
        self,
        credentials: Optional[Union[TokenCredential, AsyncTokenCredential]] = None,
        scopes: Optional[List[str]] = None,
        client: Optional[AgentsM365CopilotBetaServiceClient] = None,
    ) -> None:
        """
        Initialize the OpenCog Copilot client.

        Args:
            credentials: Azure credentials for authentication
            scopes: OAuth scopes, defaults to ['https://graph.microsoft.com/.default']
            client: Optional existing M365 Copilot client to wrap
        """
        if client:
            self.client = client
        elif credentials:
            self.client = AgentsM365CopilotBetaServiceClient(
                credentials=credentials,
                scopes=scopes or ['https://graph.microsoft.com/.default']
            )
        else:
            raise ValueError("Either credentials or client must be provided")

        # Initialize OpenCog components
        self.adapter = AtomSpaceAdapter()
        self.graph_builder = KnowledgeGraphBuilder(metta=self.adapter.metta)

    async def retrieve_to_atomspace(
        self,
        query: str,
        data_source: Union[str, RetrievalDataSource] = RetrievalDataSource.SharePoint,
        maximum_results: Optional[int] = None
    ) -> GroundingSpace:
        """
        Retrieve data from M365 Copilot and convert to OpenCog AtomSpace.

        Args:
            query: Search query string
            data_source: Data source to search (SharePoint, OneDrive, etc.)
            maximum_results: Maximum number of results to retrieve

        Returns:
            GroundingSpace: Knowledge graph of retrieval results
        """
        # Create retrieval request
        retrieval_body = RetrievalPostRequestBody()

        # Handle data source
        if isinstance(data_source, str):
            # Convert string to enum
            data_source = getattr(RetrievalDataSource, data_source, RetrievalDataSource.SharePoint)
        retrieval_body.data_source = data_source
        retrieval_body.query_string = query

        if maximum_results:
            retrieval_body.maximum_number_of_results = maximum_results

        # Make API call
        retrieval_response = await self.client.copilot.retrieval.post(retrieval_body)

        # Convert to AtomSpace
        return self.adapter.convert_retrieval_response(retrieval_response)

    async def build_knowledge_graph(
        self,
        query: str,
        data_source: Union[str, RetrievalDataSource] = RetrievalDataSource.SharePoint,
        infer_relationships: bool = True
    ) -> GroundingSpace:
        """
        Build a rich knowledge graph from M365 Copilot retrieval.

        Args:
            query: Search query string
            data_source: Data source to search
            infer_relationships: Whether to infer implicit relationships

        Returns:
            GroundingSpace: Constructed knowledge graph
        """
        # Create retrieval request
        retrieval_body = RetrievalPostRequestBody()

        if isinstance(data_source, str):
            data_source = getattr(RetrievalDataSource, data_source, RetrievalDataSource.SharePoint)
        retrieval_body.data_source = data_source
        retrieval_body.query_string = query

        # Make API call
        retrieval_response = await self.client.copilot.retrieval.post(retrieval_body)

        # Build knowledge graph
        space = self.graph_builder.build_from_retrieval(retrieval_response)

        # Infer relationships if requested
        if infer_relationships:
            self.graph_builder.infer_relationships()

        return space

    def query_knowledge_graph(self, pattern: str) -> List[str]:
        """
        Query the knowledge graph using MeTTa pattern matching.

        Args:
            pattern: MeTTa query pattern

        Returns:
            List[str]: Matching results
        """
        return self.adapter.query_atoms(pattern)

    def get_graph_statistics(self) -> dict:
        """
        Get statistics about the current knowledge graph.

        Returns:
            dict: Statistics including entity and relationship counts
        """
        return self.graph_builder.export_statistics()

    def get_all_atoms(self) -> List[str]:
        """
        Get all atoms in the current knowledge graph.

        Returns:
            List[str]: All atoms
        """
        return self.adapter.get_all_atoms()

    async def retrieve(
        self,
        query: str,
        data_source: Union[str, RetrievalDataSource] = RetrievalDataSource.SharePoint
    ) -> Any:
        """
        Standard retrieval without OpenCog conversion (for compatibility).

        Args:
            query: Search query string
            data_source: Data source to search

        Returns:
            Retrieval response from M365 Copilot API
        """
        retrieval_body = RetrievalPostRequestBody()

        if isinstance(data_source, str):
            data_source = getattr(RetrievalDataSource, data_source, RetrievalDataSource.SharePoint)
        retrieval_body.data_source = data_source
        retrieval_body.query_string = query

        return await self.client.copilot.retrieval.post(retrieval_body)
