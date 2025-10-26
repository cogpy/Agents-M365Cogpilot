# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
OpenCog integration for Microsoft 365 Copilot APIs.

This package provides tools to integrate OpenCog's knowledge graph and reasoning
capabilities with Microsoft 365 Copilot APIs.
"""

__version__ = "1.0.0-preview.1"

# Lazy imports to avoid requiring all dependencies at import time
def __getattr__(name):
    """Lazy import of package components."""
    if name == "OpenCogCopilotClient":
        from .client import OpenCogCopilotClient
        return OpenCogCopilotClient
    elif name == "AtomSpaceAdapter":
        from .atomspace_adapter import AtomSpaceAdapter
        return AtomSpaceAdapter
    elif name == "KnowledgeGraphBuilder":
        from .knowledge_graph_builder import KnowledgeGraphBuilder
        return KnowledgeGraphBuilder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "OpenCogCopilotClient",
    "AtomSpaceAdapter",
    "KnowledgeGraphBuilder",
]
