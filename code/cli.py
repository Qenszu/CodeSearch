import argparse

from smart_update import smart_update
from db import DB

from pretty_print import pretty_print
from indexer import CodeIndexer
import shutil
import os


def main():
    parser = argparse.ArgumentParser(description="Proste CLI z opcjami i oraz f")

    parser.add_argument('-i', '--index', action='store_true', help='Builds local database')
    parser.add_argument('-f', '--file', action='store_true', help='Finds in your code')
    parser.add_argument('-u', '--update', action='store_true', help='Updates smart database')
    parser.add_argument('-d', '--delete', action='store_true', help='Deletes local database')

    args = parser.parse_args()

    if args.index:
        print("Creating database, could take some time...")
        indexer = CodeIndexer()
        indexer.index_project("./code")

    if args.file:
        db = DB("codebase")
        print("Write your question or 'exit' to close \n")

        while True:
            query = input("Question (type exit to close): ")

            if query.lower() == "exit":
                break

            result = db.query([query], 3)
            pretty_print(result)

    if args.update:
        changes = smart_update('HEAD~1', 'HEAD')

        print("-" * 30)
        for c in changes:
            print(f"[{c['status']}] {c['path']}")

    if args.delete:
        path = "./chroma_db"

        if os.path.exists(path):
            shutil.rmtree(path)

    if not (args.index or args.file):
        parser.print_help()


if __name__ == "__main__":
    main()