import subprocess
import os
import pathspec
from indexer import CodeIndexer

def glupia_funkcja():
    drumba = 0
    print(drumba)

def get_gitignore_spec():
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            lines = f.readlines()
        return pathspec.PathSpec.from_lines('gitwildmatch', lines)
    return None


def smart_update(commit_a, commit_b):
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
        os.chdir(repo_root)

        indexer = CodeIndexer()
        spec = get_gitignore_spec()

        cmd = ['git', 'diff', '--name-status', commit_a, commit_b]
        result = subprocess.check_output(cmd).decode('utf-8')

        files = []
        for line in result.strip().split('\n'):
            if not line: continue

            parts = line.split('\t')
            status = parts[0]
            path = parts[2] if status.startswith('R') else parts[1]
            old_path = parts[1] if status.startswith('R') else None

            if spec and spec.match_file(path):
                print(f"Ignoruję (gitignore): {path}")
                continue

            match status[0]:
                case 'A':
                    print(f"Dodaję do indeksu: {path}")
                    indexer.index_file(path)
                case 'M':
                    print(f"Aktualizuję w indeksie: {path}")
                    indexer.db.collection.delete(where={"path": path})

                    indexer.index_file(path)
                case 'D':
                    print(f"Usuwam z indeksu: {path}")
                    indexer.delete_file(path)
                case 'R':
                    print(f"Zmiana nazwy: {old_path} -> {path}")
                    indexer.delete_file(old_path)
                    indexer.index_file(path)

            files.append({'status': status, 'path': path})

        return files
    except Exception as e:
        print(f"Błąd: {e}")
        return []