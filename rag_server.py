#!/usr/bin/env python3
import json
from typing import Optional
from db import RAGDatabase
from fastmcp import FastMCP

# Initialize the RAG database
rag_db = RAGDatabase()

# Create FastMCP server
mcp = FastMCP(
    name="RAG Server", 
    instructions="""
    You are a Retrieval-Augmented Generation (RAG) server that manages a vector database of documents.
    You can embed documents, search for similar documents, and manage the database.
    Use the tools provided to interact with the database.
    """,
    description="""
    This server provides tools to embed documents into a vector database, search for similar documents,
    retrieve database statistics, delete documents, and list all documents currently stored.
    It supports various document formats including PDF, DOCX, TXT, and Markdown.
    The database is designed for efficient retrieval of relevant information based on natural language queries.
    You can use the following tools:
    - `embed_document(file_path: str, metadata: Optional[dict] = None) -> str`: Embed a document file into the vector database.
    - `search_documents(query: str, top_k: int = 5, min_similarity = 0.1) -> str`: Search for similar documents using natural language query.
    - `get_database_stats() -> str`: Get comprehensive statistics about the RAG database.
    - `delete_document(filename: str) -> str`: Delete all chunks of a specific document from the database.
    - `list_documents() -> str`: List all documents currently in the database.
    """,
    version="1.0.0",
    author="Hitesh Saha",
)

@mcp.tool()
def embed_document(file_path: str, metadata: Optional[dict] = None) -> str:
    """
    Embed a document file into the vector database.
    
    Args:
        file_path: Path to the document file to embed (PDF, DOCX, TXT, MD)
        metadata: Optional metadata dictionary to store with the document
    
    Returns:
        Status message about the embedding operation
    """
    result = rag_db.embed_document(file_path, metadata)
    
    if result["success"]:
        return f"✅ Successfully embedded '{result['filename']}' - {result['chunks_added']} chunks created from {result['total_characters']} characters"
    else:
        return f"❌ Failed to embed document: {result['error']}"

@mcp.tool()
def search_documents(query: str, top_k: int = 5, min_similarity: float = 0.1) -> str:
    """
    Search for similar documents using natural language query.
    
    Args:
        query: Natural language search query
        top_k: Number of results to return (default: 5)
        min_similarity: Minimum similarity threshold (default: 0.1)
    
    Returns:
        Formatted search results with similarity scores
    """
    results = rag_db.search_similar(query, top_k, min_similarity)
    
    if not results:
        return "🔍 No similar documents found for your query."
    
    response = f"🔍 Found {len(results)} similar documents:\n\n"
    
    for i, result in enumerate(results, 1):
        response += f"{i}. 📄 **{result['filename']}** (chunk {result['chunk_id']})\n"
        response += f"   📊 Similarity: {result['similarity']:.3f}\n"
        response += f"   📝 Content: {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}\n"
        
        if result['metadata']:
            response += f"   🏷️ Metadata: {json.dumps(result['metadata'])}\n"
        
        response += "\n" + "-" * 80 + "\n\n"
    
    return response

@mcp.tool()
def get_database_stats() -> str:
    """
    Get comprehensive statistics about the RAG database.
    
    Returns:
        Formatted database statistics including file counts and embedding info
    """
    stats = rag_db.get_stats()
    
    response = "📊 **RAG Database Statistics**\n\n"
    response += f"📚 Total Documents: {stats['unique_files']}\n"
    response += f"🧩 Total Chunks: {stats['total_chunks']}\n"
    response += f"🤖 Embedding Model: {stats['embedding_model']}\n"
    response += f"💾 Database Path: {stats['database_path']}\n\n"
    
    if stats['files']:
        response += "📋 **Files in Database:**\n"
        for file_info in stats['files']:
            response += f"  • {file_info['filename']}: {file_info['chunks']} chunks\n"
    else:
        response += "📭 No documents in database yet.\n"
    
    return response

@mcp.tool()
def delete_document(filename: str) -> str:
    """
    Delete all chunks of a specific document from the database.
    
    Args:
        filename: Name of the file to delete from the database
    
    Returns:
        Status message about the deletion operation
    """
    result = rag_db.delete_document(filename)
    
    if result["success"]:
        return f"🗑️ Successfully deleted '{result['filename']}' - {result['chunks_deleted']} chunks removed"
    else:
        return f"❌ Failed to delete document: {result['error']}"

@mcp.tool()
def list_documents() -> str:
    """
    List all documents currently in the database.
    
    Returns:
        Formatted list of all documents with their chunk counts
    """
    stats = rag_db.get_stats()
    
    if not stats['files']:
        return "📭 No documents in database."
    
    response = f"📚 **Documents in Database** ({stats['unique_files']} total):\n\n"
    
    for i, file_info in enumerate(stats['files'], 1):
        response += f"{i}. 📄 {file_info['filename']} ({file_info['chunks']} chunks)\n"
    
    return response

if __name__ == "__main__":
    mcp.run(transport='http', host='127.0.0.1', port=8000)
