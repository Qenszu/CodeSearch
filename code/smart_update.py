import subprocess
import os

try:
    import pathspec
except ImportError:
    pathspec = None

from indexer import CodeIndexer


def integral():
    fx = lambda x: x**2

    v = 0
    for i in range(0, 1):
        v += fx(i)

    return v

def get_gitignore_spec():
    if pathspec is None:
        return None

    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            lines = f.readlines()
        return pathspec.PathSpec.from_lines('gitwildmatch', lines)
    return None


def debug_check(indexer, search_path):
    all_data = indexer.db.collection.get()
    unique_files = set(m['file'] for m in all_data['metadatas'] if 'file' in m)
    print(f"DEBUG: Szukany plik: '{search_path}'")
    print(f"DEBUG: Pliki w bazie: {unique_files}")

def smart_update(commit_a=None, commit_b=None):
    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
        os.chdir(repo_root)

        indexer = CodeIndexer()
        spec = get_gitignore_spec()

        if commit_a is not None and commit_b is not None:
            cmd = ['git', 'diff', '--name-status', commit_a, commit_b]
            result = subprocess.check_output(cmd).decode('utf-8')
        else:
            result = subprocess.check_output(['git', 'diff', '--name-status', 'HEAD']).decode('utf-8')
            untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard']).decode('utf-8')
            if untracked.strip():
                untracked_files = [line.strip() for line in untracked.splitlines() if line.strip()]
                result += '\n' + '\n'.join(f"A\t{path}" for path in untracked_files)

        files = []
        for line in result.strip().split('\n'):
            if not line: continue

            parts = line.split('\t')
            status = parts[0]
            path = parts[2] if status.startswith('R') else parts[1]
            old_path = parts[1] if status.startswith('R') else None

            if not path.endswith('.py'):
                print(f"Ignoruję nie-Pythonowy plik: {path}")
                continue

            if spec and spec.match_file(path):
                print(f"Ignoruję (gitignore): {path}")
                continue

            match status[0]:
                case 'A':
                    print(f"Dodaję do indeksu: {path}")
                    indexer.index_file(path)

                case 'M':
                    indexer.db.collection.delete(where={"file": path})
                    indexer.index_file(path)

                case 'D':
                    print(f"Usuwam z indeksu: {path}")
                    indexer.delete_file(path)
                case 'R':
                    print(f"Zmiana nazwy: {old_path} -> {path}")
                    indexer.db.collection.delete(where={"file": old_path})
                    indexer.index_file(path)

            files.append({'status': status, 'path': path})

        return files
    except Exception as e:
        print(f"Błąd: {e}")
        return []