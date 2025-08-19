# RAG MCP Server

A Retrieval Augmented Generation (RAG) server implementing the Model Context Protocol (MCP). This server allows you to embed, search, and manage documents using vector database technology.

## Features

- 📚 Document Embedding: Support for multiple document formats (PDF, DOCX, TXT, MD)
- 🔍 Semantic Search: Search through documents using natural language queries
- 💾 Vector Database: Efficient storage and retrieval of document embeddings
- 🤖 MCP Protocol: Implements the Model Context Protocol for standardized AI/ML service interactions
- 🔧 Easy-to-use API: Simple interface for document management and search

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hitesh-Saha/RAG-MCP-Server.git
cd RAG-MCP-Server
```

2. Install dependencies:
```bash
uv sync
```

## Usage

1. Start the server:
```bash
python rag_server.py
```

2. Available Operations:

### Embed a Document
Embed a document into the vector database:
```python
@mcp.tool()
def embed_document(file_path: str, metadata: Optional[dict] = None) -> str
```

### Search Documents
Search through embedded documents using natural language:
```python
@mcp.tool()
def search_documents(query: str, top_k: int = 5, min_similarity: float = 0.1) -> str
```

### List Documents
View all documents in the database:
```python
@mcp.tool()
def list_documents() -> str
```

### Get Database Stats
View statistics about the database:
```python
@mcp.tool()
def get_database_stats() -> str
```

### Delete Document
Remove a document from the database:
```python
@mcp.tool()
def delete_document(filename: str) -> str
```

## Technical Details

- Embedding Model: all-MiniLM-L6-v2
- Database: SQLite-based vector database
- Protocol: Model Context Protocol (MCP) via FastMCP

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
