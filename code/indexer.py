from pathlib import Path
from parser_ast import parser
from db import DB

class CodeIndexer:
    def __init__(self, db_name="codebase"):
        self.db = DB(db_name)

    def index_file(self, file_path: str):
        elements = parser(file_path)

        docs = []
        ids = []
        metadatas = []

        for i, code in enumerate(elements):
            doc_id = f"{file_path}:{i}"

            docs.append(code)
            ids.append(doc_id)
            metadatas.append({
                "file": file_path,
                "index": i,
                "type": "code_block"
            })

        if docs:
            print(f"INDEXING: {file_path} -> {len(docs)} chunks")
            self.db.update(docs, ids, metadatas)

        print(f"[OK] Zindeksowano: {file_path}")

    def index_project(self, path="code/"):
        path = Path(path)

        print("LOOKING IN:", path.resolve())

        files = list(path.rglob("*.py"))
        print("FOUND FILES:", len(files))

        for file in files:
            print("FILE:", file)
            self.index_file(str(file))


if __name__ == "__main__":
    indexer = CodeIndexer()
    indexer.index_project("")
