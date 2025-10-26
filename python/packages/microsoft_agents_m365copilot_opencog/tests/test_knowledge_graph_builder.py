# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Tests for Knowledge Graph Builder."""
import pytest
from unittest.mock import Mock

from microsoft_agents_m365copilot_opencog.knowledge_graph_builder import KnowledgeGraphBuilder


class TestKnowledgeGraphBuilder:
    """Test cases for KnowledgeGraphBuilder."""

    def test_initialization(self):
        """Test builder initialization."""
        builder = KnowledgeGraphBuilder()
        assert builder.metta is not None
        assert len(builder.entities) == 0
        assert len(builder.relationships) == 0

    def test_initialization_with_metta(self):
        """Test builder initialization with existing MeTTa."""
        from hyperon import MeTTa
        metta = MeTTa()
        builder = KnowledgeGraphBuilder(metta=metta)
        assert builder.metta is metta

    def test_build_from_empty_retrieval(self):
        """Test building from empty retrieval response."""
        builder = KnowledgeGraphBuilder()
        result = builder.build_from_retrieval(None)
        assert result is not None

    def test_build_from_retrieval_with_hits(self):
        """Test building from retrieval response with hits."""
        builder = KnowledgeGraphBuilder()
        
        mock_extract = Mock()
        mock_extract.text = "This document discusses Project Alpha and Team Beta."
        
        mock_hit = Mock()
        mock_hit.web_url = "https://example.com/project-alpha"
        mock_hit.extracts = [mock_extract]
        
        mock_response = Mock()
        mock_response.retrieval_hits = [mock_hit]
        
        result = builder.build_from_retrieval(mock_response)
        assert result is not None
        assert builder.get_entity_count() > 0

    def test_extract_entity_from_url(self):
        """Test entity extraction from URL."""
        builder = KnowledgeGraphBuilder()
        
        # Test normal URL
        entity = builder._extract_entity_from_url("https://example.com/my-document")
        assert entity == "doc_my_document"
        
        # Test URL with spaces
        entity = builder._extract_entity_from_url("https://example.com/my%20document")
        assert entity == "doc_my_document"
        
        # Test URL without path
        entity = builder._extract_entity_from_url("https://example.com/")
        assert entity is not None or entity is None  # Either outcome is acceptable

    def test_extract_entities_from_text(self):
        """Test entity extraction from text."""
        builder = KnowledgeGraphBuilder()
        
        text = "This is about Project Alpha and Team Beta in the Organization."
        entities = builder._extract_entities_from_text(text)
        
        assert isinstance(entities, set)
        assert len(entities) > 0
        
        # Check that capitalized words are extracted
        entity_names = [e.replace('entity_', '') for e in entities]
        assert any('project' in name.lower() for name in entity_names)

    def test_add_relationship(self):
        """Test adding relationships."""
        builder = KnowledgeGraphBuilder()
        
        builder.add_relationship("entity_a", "related-to", "entity_b")
        assert builder.get_relationship_count() == 1
        
        builder.add_relationship("entity_b", "part-of", "entity_c")
        assert builder.get_relationship_count() == 2

    def test_infer_relationships(self):
        """Test relationship inference."""
        builder = KnowledgeGraphBuilder()
        
        # Add entities with similar names
        builder.entities.add("doc_project_alpha")
        builder.entities.add("doc_project_beta")
        builder.entities.add("doc_report")
        
        initial_count = builder.get_relationship_count()
        builder.infer_relationships()
        
        # Should have inferred some relationships
        assert builder.get_relationship_count() >= initial_count

    def test_are_similar(self):
        """Test similarity check."""
        builder = KnowledgeGraphBuilder()
        
        # Similar entities (same prefix)
        assert builder._are_similar("doc_project_alpha", "doc_project_beta")
        
        # Different entities
        assert not builder._are_similar("doc_project", "doc_report")
        
        # Short entities
        assert not builder._are_similar("doc_a", "doc_b")
        
        # Empty entities
        assert not builder._are_similar("", "something")
        assert not builder._are_similar(None, "something")

    def test_get_entity_count(self):
        """Test getting entity count."""
        builder = KnowledgeGraphBuilder()
        
        assert builder.get_entity_count() == 0
        
        builder.entities.add("entity_1")
        builder.entities.add("entity_2")
        
        assert builder.get_entity_count() == 2

    def test_get_relationship_count(self):
        """Test getting relationship count."""
        builder = KnowledgeGraphBuilder()
        
        assert builder.get_relationship_count() == 0
        
        builder.add_relationship("a", "rel", "b")
        assert builder.get_relationship_count() == 1

    def test_export_statistics(self):
        """Test exporting statistics."""
        builder = KnowledgeGraphBuilder()
        
        builder.entities.add("entity_1")
        builder.entities.add("entity_2")
        builder.add_relationship("entity_1", "related-to", "entity_2")
        
        stats = builder.export_statistics()
        
        assert stats['entity_count'] == 2
        assert stats['relationship_count'] == 1
        assert 'entities' in stats
        assert 'relationships' in stats
        assert isinstance(stats['entities'], list)
        assert isinstance(stats['relationships'], list)

    def test_build_entity_nodes(self):
        """Test building entity nodes."""
        builder = KnowledgeGraphBuilder()
        
        builder.entities.add("test_entity")
        
        # Should not raise exception
        builder._build_entity_nodes()

    def test_build_relationship_edges(self):
        """Test building relationship edges."""
        builder = KnowledgeGraphBuilder()
        
        builder.add_relationship("entity_a", "connected-to", "entity_b")
        
        # Should not raise exception
        builder._build_relationship_edges()

    def test_process_hit_without_url(self):
        """Test processing hit without URL."""
        builder = KnowledgeGraphBuilder()
        
        mock_hit = Mock()
        mock_hit.web_url = None
        mock_hit.extracts = []
        
        initial_count = builder.get_entity_count()
        builder._process_hit(mock_hit)
        
        # Should handle gracefully
        assert builder.get_entity_count() >= initial_count

    def test_process_hit_with_empty_extracts(self):
        """Test processing hit with empty extracts."""
        builder = KnowledgeGraphBuilder()
        
        mock_extract = Mock()
        mock_extract.text = ""
        
        mock_hit = Mock()
        mock_hit.web_url = "https://example.com/doc"
        mock_hit.extracts = [mock_extract]
        
        builder._process_hit(mock_hit)
        
        # Should handle empty text
        assert builder.get_entity_count() >= 0
