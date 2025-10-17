#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rag.vector_store import medical_vector_store

def build_medical_index():
    

    knowledge_path = "data/medical_knowledge.txt"
    index_path = "rag/indexes/medical_index"
    
    print("Building Medical Knowledge Vector Index")
    print("=" * 50)
    

    if not os.path.exists(knowledge_path):
        print(f"Medical knowledge file not found: {knowledge_path}")
        return False
    
    try:

        medical_vector_store.build_index(knowledge_path)
        

        medical_vector_store.save_index(index_path)
        

        print("\nTesting vector search...")
        test_queries = [
            "chest pain",
            "headache and dizziness",
            "breathing problems"
        ]
        
        for query in test_queries:
            results = medical_vector_store.search(query, k=2)
            print(f"\nQuery: '{query}'")
            for i, (text, score) in enumerate(results, 1):
                print(f"  {i}. Score: {score:.3f} - {text[:60]}...")
        
        print(f"\nMedical vector index built successfully!")
        print(f"Index saved to: {index_path}")
        return True
        
    except Exception as e:
        print(f"Error building index: {e}")
        return False

if __name__ == "__main__":
    build_medical_index()