# Changelog

All notable changes to the Microsoft Agents M365 Copilot OpenCog integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-preview.1] - 2025-10-26

### Added
- Initial release of OpenCog integration for Microsoft 365 Copilot APIs
- `OpenCogCopilotClient` - Main client for OpenCog-enabled M365 Copilot interactions
- `AtomSpaceAdapter` - Converts M365 Copilot data to OpenCog AtomSpace format
- `KnowledgeGraphBuilder` - Builds rich knowledge graphs from M365 data
- Support for converting retrieval responses to OpenCog knowledge graphs
- Entity extraction from M365 documents and text
- Relationship inference between entities
- Pattern matching and querying capabilities using MeTTa
- Example scripts demonstrating basic usage and knowledge graph building
- Comprehensive test suite for all components
- Documentation and README

### Features
- Seamless integration with existing Microsoft 365 Copilot API clients
- Knowledge graph representation using OpenCog Hyperon
- Automatic conversion of M365 retrieval results to AtomSpace
- Entity and relationship extraction from documents
- Support for SharePoint, OneDrive, and other M365 data sources
- MeTTa pattern matching for querying knowledge graphs
- Statistics and analytics for knowledge graph structure

[1.0.0-preview.1]: https://github.com/microsoft/Agents-M365Copilot/releases/tag/python-opencog-v1.0.0-preview.1
