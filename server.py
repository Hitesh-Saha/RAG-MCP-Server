#!/usr/bin/env python3
import json
from typing import Optional, Dict, Any
from db import RAGDatabase
from fastmcp import FastMCP
from models import (
    QuestionRequest,
    EmbedDocumentResponse,
    SearchDocumentsResponse,
    DatabaseStatsResponse,
    DeleteDocumentResponse,
    ListDocumentsResponse,
    GetDocumentResponse,
    DocumentChunk,
    DocumentInfo,
    QuestionAnswer
)
from dotenv import load_dotenv
import logging
import os
# Load environment variables from .env file
load_dotenv()

# Initialize the RAG database
rag_db = RAGDatabase()

# Create FastMCP server
mcp = FastMCP(
    name="RAG Server", 
    instructions="""
    You are a Retrieval-Augmented Generation (RAG) server that manages a vector database of documents.
    You can embed documents, search for similar documents, and manage the database.
    Use the tools provided to interact with the database.
    """
)

@mcp.tool()
def embed_document(file_path: str, metadata: Optional[dict] = None) -> EmbedDocumentResponse:
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
        return EmbedDocumentResponse(
            success=True,
            filename=result.get("filename"),
            chunks_added=result.get("chunks_added"),
            total_characters=result.get("total_characters"),
            message=f"✅ Document '{result['filename']}' embedded! {result['chunks_added']} chunks created from {result['total_characters']} characters. 🚀"
        )
    else:
        return EmbedDocumentResponse(
            success=False,
            error=result.get("error"),
            message=f"❌ Oops! Failed to embed document: {result['error']} 😢"
        )

@mcp.tool()
def search_documents(query: str, top_k: int = 5, min_similarity: float = 0.4) -> SearchDocumentsResponse:
    """
    Search for similar documents using natural language query.
    
    Args:
        query: Natural language search query
        top_k: Number of results to return (default: 5)
        min_similarity: Minimum similarity threshold (default: 0.4)
    
    Returns:
        Formatted search results with similarity scores
    """
    results = rag_db.search_similar(query, top_k, min_similarity)
    if not results:
        return SearchDocumentsResponse(results=[], message="🔍 No similar documents found for your query. Try another search! 🕵️‍♂️")
    return SearchDocumentsResponse(
        results=results,
        message=f"🔍 Found {len(results)} similar document{'s' if len(results)!=1 else ''}! 📄✨"
    )

@mcp.tool()
def get_database_stats() -> DatabaseStatsResponse:
    """
    Get comprehensive statistics about the RAG database.
    
    Returns:
        Formatted database statistics including file counts and embedding info
    """
    stats = rag_db.get_stats()
    # If get_stats returns a DocumentInfo summary, wrap in list for files
    files = [stats] if isinstance(stats, DocumentInfo) else getattr(stats, 'files', [])
    return DatabaseStatsResponse(
        total_documents=len(files),
        total_chunks=getattr(stats, 'chunks', 0),
        embedding_model=getattr(stats, 'embedding_model', ''),
        database_path=getattr(stats, 'database_path', ''),
        files=files,
        message=f"📊 Database loaded! {len(files)} document{'s' if len(files)!=1 else ''} and {getattr(stats, 'chunks', 0)} chunk{'s' if getattr(stats, 'chunks', 0)!=1 else ''} stored. 🗂️"
    )

@mcp.tool()
def delete_document(filename: str) -> DeleteDocumentResponse:
    """
    Delete all chunks of a specific document from the database.
    
    Args:
        filename: Name of the file to delete from the database
    
    Returns:
        Status message about the deletion operation
    """
    result = rag_db.delete_document(filename)
    if result["success"]:
        return DeleteDocumentResponse(
            success=True,
            filename=result.get("filename"),
            chunks_deleted=result.get("chunks_deleted"),
            message=f"🗑️ Document '{result['filename']}' deleted! {result['chunks_deleted']} chunks removed. 👋"
        )
    else:
        return DeleteDocumentResponse(
            success=False,
            error=result.get("error"),
            message=f"❌ Could not delete document: {result['error']} 😬"
        )

@mcp.tool()
def list_documents() -> ListDocumentsResponse:
    """
    List all documents currently in the database.
    
    Returns:
        Formatted list of all documents with their chunk counts
    """
    stats = rag_db.get_stats()
    files = [stats] if isinstance(stats, DocumentInfo) else getattr(stats, 'files', [])
    return ListDocumentsResponse(
        total_documents=len(files),
        files=files,
        message=(
            f"📚 {len(files)} document{'s' if len(files)!=1 else ''} in the database! 🗃️" if files else "📭 No documents in database. Add some to get started! ✨"
        )
    )

@mcp.tool()
async def ask_question(request: QuestionRequest) -> QuestionAnswer:
    """Ask a question and get an answer using RAG
    
    Args:
        question: The question to answer
        context_limit: Maximum number of context chunks (default: 5)
        similarity_threshold: Minimum similarity for context (optional)
    
    Returns:
        Answer with context, sources, and confidence score
    """
    try:
        answer = await rag_db.ask_question(
            question=request.question,
            context_limit=request.context_limit,
            similarity_threshold=request.similarity_threshold
        )
        return answer
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return QuestionAnswer(
            question=request.question,
            answer="I'm sorry, I couldn't process your question due to an error.",
            context_chunks=[],
            sources=[],
            confidence=0.0
        )

@mcp.tool()
async def get_document(document_id: str) -> GetDocumentResponse:
    """Get detailed information about a specific document
    
    Args:
        document_id: ID of the document to retrieve
    
    Returns:
        Document information or error message
    """
    try:
        doc_info = await rag_db.get_document_info(document_id)
        if doc_info:
            return GetDocumentResponse(document=doc_info)
        else:
            return GetDocumentResponse(error=f"Document {document_id} not found", document_id=document_id)
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        return GetDocumentResponse(error=str(e), document_id=document_id)

if __name__ == "__main__":
    mcp.run(transport='http', host='127.0.0.1', port=8000)
