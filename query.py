import chromadb
from sentence_transformers import SentenceTransformer

from pipeline import build_chunks

COLLECTION_NAME = "acnh_guide"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def build_vector_store():
    chunks = build_chunks()
    model = SentenceTransformer(MODEL_NAME)
    collection = get_collection()

    existing = collection.count()
    if existing > 0:
        print(f"Vector store already has {existing} chunks.")
        return collection

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(documents).tolist()
    metadatas = [
        {
            "source": chunk["source"],
            "url": chunk["url"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Added {len(chunks)} chunks to ChromaDB.")
    return collection


def retrieve(query, top_k=4):
    model = SentenceTransformer(MODEL_NAME)
    collection = build_vector_store()
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved = []
    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        retrieved.append(
            {
                "text": document,
                "source": metadata["source"],
                "url": metadata["url"],
                "distance": distance,
            }
        )

    return retrieved


if __name__ == "__main__":
    test_questions = [
        "Which ordinance should I use if I play late at night?",
        "How do I catch a coelacanth?",
        "How do I create hybrid flowers?",
    ]

    for question in test_questions:
        print("=" * 80)
        print(f"QUESTION: {question}")
        results = retrieve(question)

        for result in results:
            print("-" * 80)
            print(f"Source: {result['source']}")
            print(f"Distance: {result['distance']:.4f}")
            print(result["text"])