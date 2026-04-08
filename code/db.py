import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("jinaai/jina-embeddings-v2-base-code", trust_remote_code=True)

from chromadb import EmbeddingFunction, Documents, Embeddings

class MyEmbeddingFunc(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Metoda __call__ jest używana przy dodawaniu dokumentów
        return model.encode(input).tolist()

    def embed_documents(self, input: Documents) -> Embeddings:
        # ChromaDB czasem wywołuje to jawnie dla dokumentów
        return self.__call__(input)

    def embed_query(self, input: Documents) -> Embeddings:
        # TO TEGO BRAKOWAŁO: metoda używana przy collection.query
        return self.__call__(input)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="code",
    embedding_function=MyEmbeddingFunc()
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