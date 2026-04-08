from chromadb import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer

class MyEmbeddingFunc(EmbeddingFunction):
    def __init__(self, model=SentenceTransformer("jinaai/jina-embeddings-v2-base-code", trust_remote_code=True)):
        self.model = model

    def __call__(self, input: Documents) -> Embeddings:
        return self.model.encode(input).tolist()

    def embed_documents(self, input: Documents) -> Embeddings:
        return self.__call__(input)

    def embed_query(self, input: Documents) -> Embeddings:
        return self.__call__(input)