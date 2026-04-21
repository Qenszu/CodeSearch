import chromadb
from model import MyEmbeddingFunc
from typing import Any

class DB:
    def __init__(self, name: str):
        func = MyEmbeddingFunc()
        chroma_client = chromadb.PersistentClient(
            path="./chroma_db"
        )
        self.collection = chroma_client.get_or_create_collection(
            name=name,
            embedding_function=func
        )
    def update(self, doc: list[str], id_list: list[str], metadatas=None) -> None:
        self.collection.add(
            documents=doc,
            ids=id_list,
            metadatas=metadatas
        )
    def query(self, text, num_of_result) -> dict[str, Any]:
        return self.collection.query(
            query_texts=text,
            n_results=num_of_result
        )