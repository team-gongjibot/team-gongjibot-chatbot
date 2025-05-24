from services.indexing import build_faiss_index

if __name__ == "__main__":
    result = build_faiss_index("announcements.json", "announcements.index")
    print(result)
    
