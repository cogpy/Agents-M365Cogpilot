# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
Knowledge graph builder for M365 Copilot data using OpenCog.
"""
import re
from typing import Any, Dict, List, Optional, Set
from hyperon import MeTTa, GroundingSpace


class KnowledgeGraphBuilder:
    """
    Builds rich knowledge graphs from M365 Copilot API data.

    This builder extracts entities, relationships, and semantic connections
    from M365 data to create a comprehensive knowledge graph using OpenCog.
    """

    def __init__(self, metta: Optional[MeTTa] = None):
        """
        Initialize the knowledge graph builder.

        Args:
            metta: Optional MeTTa instance to use, creates new one if not provided
        """
        self.metta = metta or MeTTa()
        self.entities: Set[str] = set()
        self.relationships: List[tuple] = []

    def build_from_retrieval(self, retrieval_response: Any) -> GroundingSpace:
        """
        Build a knowledge graph from retrieval response.

        Args:
            retrieval_response: The retrieval response from Copilot API

        Returns:
            GroundingSpace: The constructed knowledge graph
        """
        space = GroundingSpace()

        if not retrieval_response:
            return space

        if hasattr(retrieval_response, "retrieval_hits") and retrieval_response.retrieval_hits:
            for hit in retrieval_response.retrieval_hits:
                self._process_hit(hit)

        # Build the graph structure
        self._build_entity_nodes()
        self._build_relationship_edges()

        return space

    def _process_hit(self, hit: Any) -> None:
        """
        Process a retrieval hit to extract entities and relationships.

        Args:
            hit: A single retrieval hit
        """
        # Extract document as entity
        if hasattr(hit, 'web_url') and hit.web_url:
            doc_entity = self._extract_entity_from_url(hit.web_url)
            if doc_entity:
                self.entities.add(doc_entity)

        # Process extracts for entity extraction
        if hasattr(hit, 'extracts') and hit.extracts:
            for extract in hit.extracts:
                if hasattr(extract, 'text') and extract.text:
                    extracted_entities = self._extract_entities_from_text(extract.text)
                    self.entities.update(extracted_entities)

    def _extract_entity_from_url(self, url: str) -> Optional[str]:
        """
        Extract entity name from URL.

        Args:
            url: Web URL

        Returns:
            Optional[str]: Extracted entity name or None
        """

        # Extract the last meaningful part of the URL
        match = re.search(r'/([^/]+)/?$', url)
        if match:
            entity = match.group(1).replace('-', '_').replace('%20', '_')
            return f"doc_{entity}"
        return None

    def _extract_entities_from_text(self, text: str) -> Set[str]:
        """
        Extract entities from text using simple heuristics.

        Args:
            text: Text content

        Returns:
            Set[str]: Extracted entities
        """
        entities = set()

        # Simple capitalized word extraction as entities

        # Find capitalized words (simple entity extraction)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

        for word in words:
            entity_name = word.replace(' ', '_').lower()
            entities.add(f"entity_{entity_name}")

        return entities

    def _build_entity_nodes(self) -> None:
        """Build entity nodes in the MeTTa space."""
        for entity in self.entities:
            entity_atom = f'(: {entity} Entity)'
            try:
                self.metta.run(entity_atom)
            except Exception as e:
                print(f"Warning: Failed to add entity '{entity}': {e}")

    def _build_relationship_edges(self) -> None:
        """Build relationship edges in the MeTTa space."""
        for rel in self.relationships:
            source, relation, target = rel
            rel_atom = f'({relation} {source} {target})'
            try:
                self.metta.run(rel_atom)
            except Exception as e:
                print(f"Warning: Failed to add relationship '{rel}': {e}")

    def add_relationship(self, source: str, relation: str, target: str) -> None:
        """
        Add a relationship to the knowledge graph.

        Args:
            source: Source entity
            relation: Relationship type
            target: Target entity
        """
        self.relationships.append((source, relation, target))

    def infer_relationships(self) -> None:
        """
        Infer implicit relationships based on existing entities and relationships.

        This method uses simple heuristics to infer potential connections.
        """
        # Example: Documents with similar names might be related
        entity_list = list(self.entities)
        for i, entity1 in enumerate(entity_list):
            for entity2 in entity_list[i+1:]:
                if self._are_similar(entity1, entity2):
                    self.add_relationship(entity1, "related-to", entity2)

    def _are_similar(self, entity1: str, entity2: str) -> bool:
        """
        Check if two entities are similar based on their names.

        Args:
            entity1: First entity name
            entity2: Second entity name

        Returns:
            bool: True if entities are similar
        """
        # Simple similarity check based on common prefixes
        if not entity1 or not entity2:
            return False

        # Extract base names
        base1 = entity1.replace('doc_', '').replace('entity_', '')
        base2 = entity2.replace('doc_', '').replace('entity_', '')

        # Check for common prefix (at least 4 characters)
        if len(base1) >= 4 and len(base2) >= 4:
            return base1[:4] == base2[:4]

        return False

    def get_entity_count(self) -> int:
        """
        Get the number of entities in the knowledge graph.

        Returns:
            int: Number of entities
        """
        return len(self.entities)

    def get_relationship_count(self) -> int:
        """
        Get the number of relationships in the knowledge graph.

        Returns:
            int: Number of relationships
        """
        return len(self.relationships)

    def export_statistics(self) -> Dict[str, Any]:
        """
        Export knowledge graph statistics.

        Returns:
            Dict[str, Any]: Statistics about the knowledge graph
        """
        return {
            'entity_count': self.get_entity_count(),
            'relationship_count': self.get_relationship_count(),
            'entities': list(self.entities),
            'relationships': self.relationships
        }
