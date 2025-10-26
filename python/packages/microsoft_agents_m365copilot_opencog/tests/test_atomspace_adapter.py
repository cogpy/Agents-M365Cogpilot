# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Tests for AtomSpace adapter."""
import pytest
from unittest.mock import Mock, MagicMock

from microsoft_agents_m365copilot_opencog.atomspace_adapter import AtomSpaceAdapter


class TestAtomSpaceAdapter:
    """Test cases for AtomSpaceAdapter."""

    def test_initialization(self):
        """Test adapter initialization."""
        adapter = AtomSpaceAdapter()
        assert adapter.metta is not None
        assert adapter.space is not None

    def test_convert_empty_retrieval_response(self):
        """Test converting empty retrieval response."""
        adapter = AtomSpaceAdapter()
        result = adapter.convert_retrieval_response(None)
        assert result is not None

    def test_convert_retrieval_response_with_hits(self):
        """Test converting retrieval response with hits."""
        adapter = AtomSpaceAdapter()
        
        # Create mock retrieval hit
        mock_extract = Mock()
        mock_extract.text = "This is a test document content."
        
        mock_hit = Mock()
        mock_hit.web_url = "https://example.com/document1"
        mock_hit.extracts = [mock_extract]
        
        mock_response = Mock()
        mock_response.retrieval_hits = [mock_hit]
        
        # Convert response
        result = adapter.convert_retrieval_response(mock_response)
        assert result is not None

    def test_sanitize_identifier(self):
        """Test identifier sanitization."""
        adapter = AtomSpaceAdapter()
        
        # Test various inputs
        assert adapter._sanitize_identifier("test-doc") == "test_doc"
        assert adapter._sanitize_identifier("123test") == "id_123test"
        assert adapter._sanitize_identifier("hello world!") == "hello_world_"
        
        # Test length limiting
        long_id = "a" * 100
        sanitized = adapter._sanitize_identifier(long_id)
        assert len(sanitized) <= 50

    def test_escape_string(self):
        """Test string escaping."""
        adapter = AtomSpaceAdapter()
        
        # Test quote escaping
        assert adapter._escape_string('test "quoted"') == 'test \\"quoted\\"'
        
        # Test backslash escaping
        assert adapter._escape_string('path\\to\\file') == 'path\\\\to\\\\file'
        
        # Test newline handling
        assert adapter._escape_string('line1\nline2') == 'line1 line2'
        
        # Test empty string
        assert adapter._escape_string('') == ''
        assert adapter._escape_string(None) == ''

    def test_add_retrieval_hit_without_url(self):
        """Test adding retrieval hit without URL."""
        adapter = AtomSpaceAdapter()
        
        mock_hit = Mock()
        mock_hit.web_url = None
        mock_hit.extracts = []
        
        # Should not raise exception
        adapter._add_retrieval_hit(mock_hit)

    def test_add_retrieval_hit_with_extracts(self):
        """Test adding retrieval hit with multiple extracts."""
        adapter = AtomSpaceAdapter()
        
        mock_extract1 = Mock()
        mock_extract1.text = "First extract content"
        
        mock_extract2 = Mock()
        mock_extract2.text = "Second extract content"
        
        mock_hit = Mock()
        mock_hit.web_url = "https://example.com/doc"
        mock_hit.extracts = [mock_extract1, mock_extract2]
        
        # Should process both extracts without error
        adapter._add_retrieval_hit(mock_hit)

    def test_convert_interaction_history_empty(self):
        """Test converting empty interaction history."""
        adapter = AtomSpaceAdapter()
        result = adapter.convert_interaction_history([])
        assert result is not None

    def test_convert_interaction_history_with_interactions(self):
        """Test converting interaction history with data."""
        adapter = AtomSpaceAdapter()
        
        mock_interaction = Mock()
        mock_interaction.id = "interaction-123"
        mock_interaction.interaction_type = "chat"
        
        result = adapter.convert_interaction_history([mock_interaction])
        assert result is not None

    def test_query_atoms(self):
        """Test querying atoms."""
        adapter = AtomSpaceAdapter()
        
        # Query should not raise error even with empty space
        results = adapter.query_atoms("!(match &self (: $x Document) $x)")
        assert isinstance(results, list)

    def test_get_all_atoms(self):
        """Test getting all atoms."""
        adapter = AtomSpaceAdapter()
        
        # Should return a list
        results = adapter.get_all_atoms()
        assert isinstance(results, list)

    def test_add_atom_with_invalid_syntax(self):
        """Test adding atom with invalid syntax."""
        adapter = AtomSpaceAdapter()
        
        # Should not raise exception, just warn
        adapter._add_atom("invalid atom syntax {}")

    def test_retrieval_hit_with_long_text(self):
        """Test processing retrieval hit with very long text."""
        adapter = AtomSpaceAdapter()
        
        mock_extract = Mock()
        mock_extract.text = "a" * 1000  # Very long text
        
        mock_hit = Mock()
        mock_hit.web_url = "https://example.com/doc"
        mock_hit.extracts = [mock_extract]
        
        # Should handle long text by truncating
        adapter._add_retrieval_hit(mock_hit)
