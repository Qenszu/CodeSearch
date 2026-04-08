import chromadb
from model import MyEmbeddingFunc

F = MyEmbeddingFunc()

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="code",
    embedding_function=F
)

collection.add(
    documents=["def hello_world(): print('hi')", "class Database: pass"],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["Print Hi"],
    n_results=1
)

print(results)