import chromadb
from model import MyEmbeddingFunc
from typing import Any

class DB:
    def __init__(self, name: str):
        func = MyEmbeddingFunc()
        chroma_client = chromadb.Client()
        self.collection = (chroma_client.create_collection(
            name=name,
            embedding_function=func
        ))
    def update(self, doc: list[str], id_list: list[str]) -> None:
        self.collection.add(
            documents=doc,
            ids=id_list
        )
    def query(self, text, num_of_result) -> dict[str, Any]:
        return self.collection.query(
            query_texts=text,
            n_results=num_of_result
        )