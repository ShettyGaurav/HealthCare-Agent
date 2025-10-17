import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class MedicalVectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.index = None
        self.documents = []
        self.embeddings = []
        
    def build_index(self, medical_knowledge_path: str):
        print("Building medical knowledge vector index...")
        
        with open(medical_knowledge_path, 'r') as f:
            content = f.read()
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        self.documents = lines
        
        embeddings = self.model.encode(lines)
        self.embeddings = embeddings
        
        self.index = faiss.IndexFlatIP(self.dimension)
        
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Vector index built with {len(lines)} medical entries")
        
    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        if self.index is None:
            return []
        

        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        

        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        

        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append((doc, float(score)))
        
        return results
    
    def save_index(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        

        faiss.write_index(self.index, f"{path}.faiss")
        

        with open(f"{path}.pkl", 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'embeddings': self.embeddings
            }, f)
        
        print(f"Vector index saved to {path}")
    
    def load_index(self, path: str):
        try:

            self.index = faiss.read_index(f"{path}.faiss")
            

            with open(f"{path}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.embeddings = data['embeddings']
            
            print(f"Vector index loaded from {path}")
            return True
        except FileNotFoundError:
            print(f"Vector index not found at {path}")
            return False


medical_vector_store = MedicalVectorStore()