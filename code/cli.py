import argparse

from smart_update import smart_update
from db import DB

from pretty_print import pretty_print
from indexer import CodeIndexer


def main():
    parser = argparse.ArgumentParser(description="Proste CLI z opcjami i oraz f")

    parser.add_argument('-i', '--info', action='store_true', help='Wyświetla informacje')
    parser.add_argument('-f', '--file', action='store_true', help='Przyjmuje nazwę pliku')
    parser.add_argument('-u', '--update', action='store_true', help='Uaktualnie bazy danych')

    args = parser.parse_args()

    if args.info:
        print("Creating database, could take some time...")
        indexer = CodeIndexer()
        indexer.index_project("")

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

    if not (args.info or args.file):
        parser.print_help()


if __name__ == "__main__":
    main()