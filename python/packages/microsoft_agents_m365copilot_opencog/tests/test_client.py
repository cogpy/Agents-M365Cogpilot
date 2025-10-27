# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Tests for OpenCog Copilot Client."""
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock, patch

from microsoft_agents_m365copilot_opencog.client import OpenCogCopilotClient


class TestOpenCogCopilotClient:
    """Test cases for OpenCogCopilotClient."""

    def test_initialization_with_credentials(self):
        """Test client initialization with credentials."""
        mock_credentials = Mock()
        
        with patch('microsoft_agents_m365copilot_opencog.client.AgentsM365CopilotBetaServiceClient') as mock_client_class:
            mock_client_class.return_value = Mock()
            
            client = OpenCogCopilotClient(credentials=mock_credentials)
            
            assert client.client is not None
            assert client.adapter is not None
            assert client.graph_builder is not None
            mock_client_class.assert_called_once()

    def test_initialization_with_existing_client(self):
        """Test client initialization with existing M365 client."""
        mock_m365_client = Mock()
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        assert client.client is mock_m365_client
        assert client.adapter is not None
        assert client.graph_builder is not None

    def test_initialization_without_credentials_or_client(self):
        """Test that initialization fails without credentials or client."""
        with pytest.raises(ValueError, match="Either credentials or client must be provided"):
            OpenCogCopilotClient()

    @pytest.mark.asyncio
    async def test_retrieve_to_atomspace(self):
        """Test retrieving data to AtomSpace."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_response.retrieval_hits = []
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.retrieve_to_atomspace(
            query="test query",
            data_source="SharePoint"
        )
        
        assert result is not None
        mock_retrieval.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieve_to_atomspace_with_string_data_source(self):
        """Test retrieve with string data source."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_response.retrieval_hits = []
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.retrieve_to_atomspace(
            query="test query",
            data_source="SharePoint"
        )
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_build_knowledge_graph(self):
        """Test building knowledge graph."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_response.retrieval_hits = []
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.build_knowledge_graph(
            query="test query",
            data_source="SharePoint",
            infer_relationships=True
        )
        
        assert result is not None
        mock_retrieval.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_build_knowledge_graph_without_inference(self):
        """Test building knowledge graph without relationship inference."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_response.retrieval_hits = []
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.build_knowledge_graph(
            query="test query",
            infer_relationships=False
        )
        
        assert result is not None

    def test_query_knowledge_graph(self):
        """Test querying knowledge graph."""
        mock_m365_client = Mock()
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        results = client.query_knowledge_graph("!(match &self (: $x Document) $x)")
        
        assert isinstance(results, list)

    def test_get_graph_statistics(self):
        """Test getting graph statistics."""
        mock_m365_client = Mock()
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        stats = client.get_graph_statistics()
        
        assert isinstance(stats, dict)
        assert 'entity_count' in stats
        assert 'relationship_count' in stats

    def test_get_all_atoms(self):
        """Test getting all atoms."""
        mock_m365_client = Mock()
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        atoms = client.get_all_atoms()
        
        assert isinstance(atoms, list)

    @pytest.mark.asyncio
    async def test_retrieve_standard(self):
        """Test standard retrieve method."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.retrieve(query="test query")
        
        assert result is not None
        mock_retrieval.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieve_with_maximum_results(self):
        """Test retrieve with maximum results parameter."""
        mock_m365_client = Mock()
        mock_retrieval = AsyncMock()
        mock_response = Mock()
        mock_response.retrieval_hits = []
        mock_retrieval.post.return_value = mock_response
        mock_m365_client.copilot.retrieval = mock_retrieval
        
        client = OpenCogCopilotClient(client=mock_m365_client)
        
        result = await client.retrieve_to_atomspace(
            query="test query",
            maximum_results=10
        )
        
        assert result is not None

    def test_scopes_default_value(self):
        """Test that default scopes are used when not provided."""
        mock_credentials = Mock()
        
        with patch('microsoft_agents_m365copilot_opencog.client.AgentsM365CopilotBetaServiceClient') as mock_client_class:
            mock_client_class.return_value = Mock()
            
            client = OpenCogCopilotClient(credentials=mock_credentials)
            
            # Verify default scopes were used
            call_args = mock_client_class.call_args
            assert call_args[1]['scopes'] == ['https://graph.microsoft.com/.default']
