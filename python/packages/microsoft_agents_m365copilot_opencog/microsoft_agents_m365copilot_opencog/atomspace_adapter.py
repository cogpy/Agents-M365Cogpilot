# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
AtomSpace adapter for converting M365 Copilot data to OpenCog knowledge graphs.
"""
import re
from typing import Any, List
from hyperon import MeTTa, GroundingSpace


class AtomSpaceAdapter:
    """
    Adapter to convert Microsoft 365 Copilot API responses into OpenCog AtomSpace format.

    This adapter creates a knowledge graph representation using OpenCog Hyperon's MeTTa
    and GroundingSpace, enabling reasoning and pattern matching over M365 data.
    """

    def __init__(self):
        """Initialize the AtomSpace adapter with a new MeTTa space."""
        self.metta = MeTTa()
        self.space = GroundingSpace()

    def convert_retrieval_response(self, retrieval_response: Any) -> GroundingSpace:
        """
        Convert a retrieval response from M365 Copilot API to AtomSpace.

        Args:
            retrieval_response: The retrieval response from Copilot API containing hits

        Returns:
            GroundingSpace: A knowledge graph representation of the retrieval results
        """
        if not retrieval_response:
            return self.space

        # Process retrieval hits if available
        if hasattr(retrieval_response, "retrieval_hits") and retrieval_response.retrieval_hits:
            for hit in retrieval_response.retrieval_hits:
                self._add_retrieval_hit(hit)

        return self.space

    def _add_retrieval_hit(self, hit: Any) -> None:
        """
        Add a retrieval hit to the AtomSpace as a document node with relationships.

        Args:
            hit: A single retrieval hit containing document information
        """
        # Create document concept node
        doc_id = self._sanitize_identifier(hit.web_url if hasattr(hit, 'web_url') else 'unknown')

        # Add document node
        doc_atom = f'(: Document_{doc_id} Document)'
        self._add_atom(doc_atom)

        # Add URL property if available
        if hasattr(hit, 'web_url') and hit.web_url:
            url_atom = f'(has-url Document_{doc_id} "{hit.web_url}")'
            self._add_atom(url_atom)

        # Add extracts as content nodes
        if hasattr(hit, 'extracts') and hit.extracts:
            for idx, extract in enumerate(hit.extracts):
                if hasattr(extract, 'text') and extract.text:
                    content_id = f"{doc_id}_extract_{idx}"
                    content_atom = f'(: Content_{content_id} Content)'
                    self._add_atom(content_atom)

                    # Link content to document
                    link_atom = f'(has-extract Document_{doc_id} Content_{content_id})'
                    self._add_atom(link_atom)

                    # Store text content (truncated for atom representation)
                    text_preview = (
                        extract.text[:100] if len(extract.text) > 100 else extract.text
                    )
                    escaped_text = self._escape_string(text_preview)
                    text_atom = f'(has-text Content_{content_id} "{escaped_text}")'
                    self._add_atom(text_atom)

    def convert_interaction_history(self, interactions: List[Any]) -> GroundingSpace:
        """
        Convert interaction history from M365 Copilot API to AtomSpace.

        Args:
            interactions: List of AI interactions

        Returns:
            GroundingSpace: A knowledge graph of interaction history
        """
        for interaction in interactions:
            self._add_interaction(interaction)
        return self.space

    def _add_interaction(self, interaction: Any) -> None:
        """
        Add an interaction to the AtomSpace.

        Args:
            interaction: An AI interaction event
        """
        interaction_id = self._sanitize_identifier(
            str(getattr(interaction, 'id', 'unknown'))
        )

        # Create interaction node
        interaction_atom = f'(: Interaction_{interaction_id} Interaction)'
        self._add_atom(interaction_atom)

        # Add interaction type if available
        if hasattr(interaction, 'interaction_type'):
            type_atom = f'(has-type Interaction_{interaction_id} {interaction.interaction_type})'
            self._add_atom(type_atom)

    def _add_atom(self, atom_str: str) -> None:
        """
        Add an atom to the MeTTa space.

        Args:
            atom_str: String representation of the atom in MeTTa format
        """
        try:
            # Parse and add the atom to the space
            self.metta.run(atom_str)
        except Exception as e:
            # Log error but continue processing
            print(f"Warning: Failed to add atom '{atom_str}': {e}")

    def _sanitize_identifier(self, identifier: str) -> str:
        """
        Sanitize a string to be used as an identifier in atoms.

        Args:
            identifier: Raw identifier string

        Returns:
            str: Sanitized identifier safe for use in atoms
        """
        # Replace non-alphanumeric characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', str(identifier))
        # Ensure it doesn't start with a number
        if sanitized and sanitized[0].isdigit():
            sanitized = 'id_' + sanitized
        return sanitized[:50]  # Limit length

    def _escape_string(self, text: str) -> str:
        """
        Escape a string for use in atom values.

        Args:
            text: Raw text string

        Returns:
            str: Escaped string safe for atom values
        """
        if not text:
            return ""
        # Escape quotes and backslashes
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

    def query_atoms(self, pattern: str) -> List[str]:
        """
        Query atoms in the space using a MeTTa pattern.

        Args:
            pattern: MeTTa query pattern

        Returns:
            List[str]: Matching atoms
        """
        try:
            results = self.metta.run(pattern)
            return [str(result) for result in results]
        except Exception as e:
            print(f"Query error: {e}")
            return []

    def get_all_atoms(self) -> List[str]:
        """
        Get all atoms in the space.

        Returns:
            List[str]: All atoms in the knowledge graph
        """
        try:
            # Use MeTTa to get all atoms
            result = self.metta.run("!(get-atoms &self)")
            return [str(atom) for atom in result]
        except Exception:
            return []
