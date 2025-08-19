from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from pathlib import Path
import sqlite3
import numpy as np
import PyPDF2
from docx import Document
import json

class RAGDatabase:
    def __init__(self, db_path: str = "rag_database.db"):
        self.db_path = db_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing documents and embeddings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                chunk_id INTEGER NOT NULL,
                embedding BLOB NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_filename ON documents(filename);
        ''')
        
        conn.commit()
        conn.close()
    
    def chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
        
        return chunks
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        
        elif path.suffix.lower() == '.docx':
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        elif path.suffix.lower() in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def embed_document(self, file_path: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Process and embed documents into the vector database"""
        try:
            text = self.extract_text_from_file(file_path)
            chunks = self.chunk_text(text)
            
            if not chunks:
                raise ValueError("No content could be extracted from the file")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            filename = Path(file_path).name
            documents_added = 0
            
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.model.encode(chunk)
                embedding_blob = embedding.tobytes()
                
                # Store in database
                cursor.execute('''
                    INSERT INTO documents (filename, content, chunk_id, embedding, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (filename, chunk, i, embedding_blob, json.dumps(metadata or {})))
                
                documents_added += 1
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "filename": filename,
                "chunks_added": documents_added,
                "total_characters": len(text)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_similar(self, query: str, top_k: int = 5, min_similarity: float = 0.0) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        query_embedding = self.model.encode(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, content, chunk_id, embedding, metadata, created_at 
            FROM documents
        ''')
        results = []
        
        for row in cursor.fetchall():
            doc_id, filename, content, chunk_id, embedding_blob, metadata, created_at = row
            
            # Convert blob back to numpy array
            doc_embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            
            if similarity >= min_similarity:
                results.append({
                    'id': doc_id,
                    'filename': filename,
                    'content': content,
                    'chunk_id': chunk_id,
                    'similarity': float(similarity),
                    'metadata': json.loads(metadata) if metadata else {},
                    'created_at': created_at
                })
        
        conn.close()
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM documents')
        total_chunks = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT filename) FROM documents')
        unique_files = cursor.fetchone()[0]
        
        cursor.execute('SELECT filename, COUNT(*) as chunk_count FROM documents GROUP BY filename')
        files_info = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_chunks': total_chunks,
            'unique_files': unique_files,
            'files': [{'filename': f[0], 'chunks': f[1]} for f in files_info],
            'embedding_model': 'all-MiniLM-L6-v2',
            'database_path': self.db_path
        }
    
    def delete_document(self, filename: str) -> Dict[str, Any]:
        """Delete all chunks of a specific document"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM documents WHERE filename = ?', (filename,))
        chunks_to_delete = cursor.fetchone()[0]
        
        if chunks_to_delete == 0:
            conn.close()
            return {"success": False, "error": "Document not found"}
        
        cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "filename": filename,
            "chunks_deleted": chunks_to_delete
        }
