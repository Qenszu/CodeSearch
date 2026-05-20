import subprocess
from pathlib import Path
from parser_ast import parser
from db import DB

class CodeIndexer:
    def __init__(self, db_name="codebase"):
        self.db = DB(db_name)
        self.root = self._find_repo_root()

    def _find_repo_root(self) -> Path:
        cwd = Path.cwd()
        try:
            root = Path(subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=cwd
            ).decode("utf-8").strip())
            return root
        except Exception:
            return cwd

    def normalize_path(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.is_absolute():
            path = (self.root / path).resolve()

        try:
            path = path.relative_to(self.root)
        except ValueError:
            pass

        return str(path.as_posix())

    def index_file(self, file_path: str):
        source_path = Path(file_path)
        if not source_path.is_absolute():
            source_path = (self.root / source_path).resolve()

        normalized_path = self.normalize_path(str(source_path))
        elements = parser(str(source_path))

        docs = []
        ids = []
        metadatas = []

        for i, code in enumerate(elements):
            doc_id = f"{normalized_path}:{i}"

            docs.append(code)
            ids.append(doc_id)
            metadatas.append({
                "file": normalized_path,
                "index": i,
                "type": "code_block"
            })

        if docs:
            print(f"INDEXING: {normalized_path} -> {len(docs)} chunks")
            self.db.upsert(docs, ids, metadatas)

        print(f"[OK] Zindeksowano: {normalized_path}")

    def index_project(self, path="code/"):
        path = Path(path)
        if not path.is_absolute():
            path = (self.root / path).resolve()

        print("LOOKING IN:", path)

        files = list(path.rglob("*.py"))
        print("FOUND FILES:", len(files))

        for file in files:
            print("FILE:", file)
            self.index_file(str(file))

    def delete_file(self, path):
        normalized_path = self.normalize_path(path)
        self.db.collection.delete(where={"file": normalized_path})

        alt_path = Path(path)
        if not alt_path.is_absolute():
            alt_path = (self.root / alt_path).resolve()
        try:
            alt_relative = alt_path.relative_to(self.root).as_posix()
        except ValueError:
            alt_relative = None

        if alt_relative and alt_relative != normalized_path:
            self.db.collection.delete(where={"file": alt_relative})
        if normalized_path != str(alt_path.as_posix()):
            self.db.collection.delete(where={"file": str(alt_path.as_posix())})

        print(f"[OK] Usunięto z indeksu: {normalized_path}")


if __name__ == "__main__":
    indexer = CodeIndexer()
    indexer.index_project("")
