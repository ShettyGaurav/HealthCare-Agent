from typing import List, Tuple
from .vector_store import medical_vector_store
import os

class MedicalRetriever:
    def __init__(self):
        self.vector_store = medical_vector_store
        self.index_loaded = False
        self._load_index()
    
    def _load_index(self):
        index_path = "rag/indexes/medical_index"
        
        if os.path.exists(f"{index_path}.faiss"):
            self.index_loaded = self.vector_store.load_index(index_path)
        else:
            print("Vector index not found. Building new index...")
            self._build_index()
    
    def _build_index(self):
        knowledge_path = "data/medical_knowledge.txt"
        index_path = "rag/indexes/medical_index"
        
        if os.path.exists(knowledge_path):
            self.vector_store.build_index(knowledge_path)
            self.vector_store.save_index(index_path)
            self.index_loaded = True
        else:
            print("Medical knowledge file not found!")
            self.index_loaded = False
    
    def retrieve_context(self, query: str, k: int = 3) -> List[str]:
        if not self.index_loaded:
            return []
        
        results = self.vector_store.search(query, k=k)
        return [text for text, score in results if score > 0.3]
    
    def get_status(self) -> dict:
        return {
            "index_loaded": self.index_loaded,
            "total_documents": len(self.vector_store.documents) if self.index_loaded else 0
        }


medical_retriever = MedicalRetriever()