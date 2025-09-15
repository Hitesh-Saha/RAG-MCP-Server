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
	http://localhost:8000
	```
3. Use the available tools (embed, search, list, ask, etc.) from your extension or scripts.

**Tip:** You can also deploy this server to the cloud and connect from VS Code anywhere!

### 4. Or run locally
```bash
python server.py
```

---

## 🛠️ API & Tool Usage


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
