import subprocess
from indexer import CodeIndexer
import os

repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
os.chdir(repo_root)

def smart_update(commit_a, commit_b):
    try:
        indexer = CodeIndexer()

        cmd = ['git', 'diff', '--name-status', commit_a, commit_b]
        result = subprocess.check_output(cmd).decode('utf-8')

        files = []
        for line in result.strip().split('\n'):
            if not line:
                continue

            parts = line.split('\t')
            status = parts[0]

            if status.startswith('R'):
                old_path = parts[1]
                path = parts[2]
            else:
                old_path = None
                path = parts[1]

            match status[0]:
                case 'A':
                    print(f"Dodaję do indeksu: {path}")
                    indexer.index_file(path)

                case 'M':
                    print(f"Aktualizuję w indeksie: {path}")
                    indexer.delete_file(path)
                    indexer.index_file(path)

                case 'D':
                    print(f"Usuwam z indeksu: {path}")
                    indexer.delete_file(path)

                case 'R':
                    print(f"Zmieniam nazwę w indeksie: {old_path} -> {path}")
                    indexer.delete_file(old_path)
                    indexer.index_file(path)

                case 'T':
                    indexer.delete_file(path)
                    indexer.index_file(path)

            files.append({'status': status, 'path': path})

        return files
    except subprocess.CalledProcessError as e:
        print(f"Błąd Gita: {e}")
        return []
    except Exception as e:
        print(f"Błąd indeksowania: {e}")
        return []




if __name__ == "__main__":
    changes = smart_update('HEAD~1', 'HEAD')
    print("-" * 30)
    for c in changes:
        print(f"[{c['status']}] {c['path']}")