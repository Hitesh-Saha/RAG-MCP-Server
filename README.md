# RAG MCP Server

A Retrieval Augmented Generation (RAG) server implementing the Model Context Protocol (MCP). This server allows you to embed, search, and manage documents using vector database technology.

## Features

- 📚 Document Embedding: Support for multiple document formats (PDF, DOCX, TXT, MD)
- 🔍 Semantic Search: Search through documents using natural language queries
- 💾 Vector Database: Efficient storage and retrieval of document embeddings
- 🤖 MCP Protocol: Implements the Model Context Protocol for standardized AI/ML service interactions
- 🔧 Easy-to-use API: Simple interface for document management and search


## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/Hitesh-Saha/RAG-MCP-Server.git
cd RAG-MCP-Server
```

### 2. Install dependencies
```bash
uv sync
```


### 3. Run with Docker (Recommended)
```bash
# Build from source
docker build -t rag-mcp-server .
docker run -p 8000:8000 rag-mcp-server

# Or pull from DockerHub (after you push your image):
docker pull <your-dockerhub-username>/rag-mcp-server:latest
docker run -p 8000:8000 <your-dockerhub-username>/rag-mcp-server:latest
```

---

## 🧩 VS Code Integration

You can use this MCP server as a backend for VS Code extensions or AI tools that support the Model Context Protocol.

**To use in VS Code:**
1. Start the server (locally or via Docker as above).
2. In your VS Code extension or tool, set the MCP server endpoint to:
	```
	http://localhost:8000/mcp
	```
3. Use the available tools (embed, search, list, ask, etc.) from your extension or scripts.

**Tip:** You can also deploy this server to the cloud and connect from VS Code anywhere!

### 4. Run locally (source or installed)

You can run the server directly from source (useful during development) or install the package and run the provided console script.

From source (no install):

```bash
# Run using the src package layout (from repository root)
PYTHONPATH=src python -m rag_mcp_server.server --mode http --port 8000

# For stdio mode:
PYTHONPATH=src python -m rag_mcp_server.server --mode stdio
```

Install in editable mode (recommended for development):

```bash
pip install -e .
# then run the console script
rag-mcp-server --mode http --port 8000
```

After publishing to PyPI (or installing from wheel), run via the console script or with `uv`:

```bash
# Console script (installed):
rag-mcp-server --mode http --port 8000

# Or use uv to run the installed entry point (uv finds the package script):
uv run rag-mcp-server
```

---

## 📦 Packaging & Publishing to PyPI (detailed)

Follow these steps to build, test, and publish the package to PyPI.

1) Prepare metadata

 - Open `pyproject.toml` and ensure the `[project]` table has correct fields: `name`, `version`, `description`, `readme`, `authors`, `license`, `keywords`, and `classifiers`.

Example additions to `[project]`:

```toml
authors = [ { name = "Your Name", email = "you@example.com" } ]
license = { text = "MIT" }
keywords = ["mcp", "rag", "vector", "embedding"]
classifiers = [
	"Development Status :: 4 - Beta",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
]
```

2) Ensure console script entry point is configured

We added a console script in `pyproject.toml`:

```toml
[project.scripts]
rag-mcp-server = "rag_mcp_server.cli:run"
```

This maps the `rag-mcp-server` command to `rag_mcp_server.cli.run()`.

3) Build distributions

Install build tools (if you don't have them):

```bash
pip install --upgrade build twine
```

Build source and wheel:

```bash
python -m build
# artifacts appear in dist/
```

4) Test upload to Test PyPI (recommended)

```bash
python -m twine upload --repository testpypi dist/*

# Verify install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps rag-mcp-server
```

5) Publish to PyPI

When ready, upload to the real PyPI:

```bash
python -m twine upload dist/*
```

6) Verify

```bash
pip install rag-mcp-server
rag-mcp-server --mode http --port 8000
```

Tips & best practices

- Use a dedicated PyPI account and enable 2FA.
- Increment the `version` for each release and tag releases in Git (e.g. `git tag v0.1.0`).
- Add automated publishing via GitHub Actions on tag push to streamline releases (I can add a template workflow if you want).
- Keep secrets out of the repo; store PyPI API tokens in CI secrets and use Twine in CI for publishing.

## 🧭 Install & run after publishing

Once published to PyPI, users can install and run the server easily.

Install via pip:

```bash
pip install rag-mcp-server
```

Run with `uv` (recommended) — `uv` will locate the package's entry point and run it. Example (after installing `uv`):

```bash
# Run the server (default HTTP on 127.0.0.1:8000)
uv run rag-mcp-server

# Or run via the console script directly (if project.scripts was configured):
rag-mcp-server --mode http --port 8000
```

If you'd rather run the module directly:

```bash
python -m rag_mcp_server.server --mode http
```

## 🧪 Smoke test / verification

After installing, try a quick health check (HTTP mode):

```bash
curl -v http://127.0.0.1:8000/health || true
```

For stdio mode, use a compliant MCP client that writes Content-Length framed JSON requests and reads framed responses.

## 🐳 Docker notes (packaged)

The included `Dockerfile` already uses `uv` to run the server. When packaging, you can either:

- Build the Docker image from the source (as-is), or
- Use the PyPI package inside a smaller runtime image (multi-stage build): install the published wheel with `pip install rag-mcp-server` and run the console script.

Example Docker command (after publishing to PyPI):

```Dockerfile
FROM python:3.12-slim
RUN pip install rag-mcp-server uv
CMD ["uv", "run", "rag-mcp-server"]
```


---

## �🛠️ API & Tool Usage


### 📥 Embed a Document
Embed a document into the vector database:
```python
embed_document(file_path: str, metadata: Optional[dict] = None) -> EmbedDocumentResponse
```
**Response Model:** `EmbedDocumentResponse`
**Example Response:**
```
✅ Document 'example.pdf' embedded! 3 chunks created from 7539 characters. 🚀
```



### 🔍 Search Documents
Search through embedded documents using natural language:
```python
search_documents(query: str, top_k: int = 5, min_similarity: float = 0.4) -> SearchDocumentsResponse
```
**Response Model:** `SearchDocumentsResponse`
**Example Response:**
```
🔍 Found 2 similar documents! 📄✨
1. 📄 somatosensory.pdf (chunk 0) | 📊 Similarity: 0.53
   📝 This is a sample document to showcase page-based formatting...
```



### 📚 List Documents
View all documents in the database:
```python
list_documents() -> ListDocumentsResponse
```
**Response Model:** `ListDocumentsResponse`
**Example Response:**
```
📚 2 documents in the database! 🗃️
1. 📄 somatosensory.pdf (3 chunks)
2. 📄 TopCSSFrameworks.docx (2 chunks)
```



### 📊 Get Database Stats
View statistics about the database:
```python
get_database_stats() -> DatabaseStatsResponse
```
**Response Model:** `DatabaseStatsResponse`
**Example Response:**
```
📊 Database loaded! 2 documents and 5 chunks stored. 🗂️
```



### 🗑️ Delete Document
Remove a document from the database:
```python
delete_document(filename: str) -> DeleteDocumentResponse
```
**Response Model:** `DeleteDocumentResponse`
**Example Response:**
```
🗑️ Document 'example.pdf' deleted! 3 chunks removed. 👋
```

### ❓ Ask a Question
Ask a question and get an answer using the RAG system:
```python
ask_question(request: QuestionRequest) -> QuestionAnswer
```
**Request Model:** `QuestionRequest`
**Response Model:** `QuestionAnswer`
**Example Response:**
```
🤖 Answer: The somatosensory system consists of sensors in the skin, muscles, tendons, and joints...
Sources: somatosensory.pdf
Confidence: 0.92
```

### 📄 Get Document Details
Get detailed information about a specific document chunk by its ID:
```python
get_document(document_id: str) -> GetDocumentResponse
```
**Response Model:** `GetDocumentResponse`
**Example Response:**
```
{
	"document": {
		"id": 3,
		"filename": "somatosensory.pdf",
		"content": "This is a sample document...",
		"chunk_id": 0,
		"metadata": {},
		"created_at": "2025-08-20 09:38:11"
	}
}
```


---

## ⚙️ Technical Details

- Embedding Model: all-MiniLM-L6-v2
- Database: SQLite-based vector database
- Protocol: Model Context Protocol (MCP) via FastMCP


---

## 📄 License

This project is licensed under the terms included in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
