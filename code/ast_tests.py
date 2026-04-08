def powitanie(imie):
    print(f"Hej {imie}!")
    return True

def suma(a, b):
    return a + b


class GemaniKuKu:
    def __init__(self):
        pass

def bfs(graf, start):
    from collections import deque
    odwiedzone = set()
    kolejka = deque([start])
    odwiedzone.add(start)

    while kolejka:
        węzeł = kolejka.popleft()
        print(węzeł)

        for sąsiad in graf[węzeł]:
            if sąsiad not in odwiedzone:
                odwiedzone.add(sąsiad)
                kolejka.append(sąsiad)


def dfs(graf, start):
    def _dfs(węzeł, odwiedzone, wynik):
        odwiedzone.add(węzeł)
        wynik.append(węzeł)

        for sąsiad in graf[węzeł]:
            if sąsiad not in odwiedzone:
                _dfs(sąsiad, odwiedzone, wynik)

    odwiedzone = set()
    wynik = []
    _dfs(start, odwiedzone, wynik)
    return wynik

class Graph:
    def __init__(self, directed=False):
        self.graf = {}
        self.directed = directed

    def add_node(self, węzeł):
        if węzeł not in self.graf:
            self.graf[węzeł] = []

    def add_edge(self, a, b):
        self.add_node(a)
        self.add_node(b)
        self.graf[a].append(b)
        if not self.directed:
            self.graf[b].append(a)

    def remove_edge(self, a, b):
        self.graf[a].remove(b)
        if not self.directed:
            self.graf[b].remove(a)

    def remove_node(self, węzeł):
        self.graf.pop(węzeł, None)
        for sąsiedzi in self.graf.values():
            if węzeł in sąsiedzi:
                sąsiedzi.remove(węzeł)

    def neighbors(self, węzeł):
        return self.graf.get(węzeł, [])

    def has_edge(self, a, b):
        return b in self.graf.get(a, [])

    def nodes(self):
        return list(self.graf.keys())

    def edges(self):
        wynik = []
        for a, sąsiedzi in self.graf.items():
            for b in sąsiedzi:
                if self.directed or (b, a) not in wynik:
                    wynik.append((a, b))
        return wynik

    def bfs(self, start):
        from collections import deque
        odwiedzone = set()
        kolejka = deque([start])
        odwiedzone.add(start)
        wynik = []

        while kolejka:
            węzeł = kolejka.popleft()
            wynik.append(węzeł)
            for sąsiad in self.graf[węzeł]:
                if sąsiad not in odwiedzone:
                    odwiedzone.add(sąsiad)
                    kolejka.append(sąsiad)
        return wynik

    def dfs(self, start):
        odwiedzone = set()
        wynik = []

        def _dfs(węzeł):
            odwiedzone.add(węzeł)
            wynik.append(węzeł)
            for sąsiad in self.graf[węzeł]:
                if sąsiad not in odwiedzone:
                    _dfs(sąsiad)

        _dfs(start)
        return wynik

    def has_cycle(self):
        odwiedzone = set()

        def _cycle(węzeł, rodzic):
            odwiedzone.add(węzeł)
            for sąsiad in self.graf[węzeł]:
                if sąsiad not in odwiedzone:
                    if _cycle(sąsiad, węzeł):
                        return True
                elif sąsiad != rodzic:
                    return True
            return False

        for węzeł in self.graf:
            if węzeł not in odwiedzone:
                if _cycle(węzeł, None):
                    return True
        return False

    def is_connected(self):
        if not self.graf:
            return True
        start = next(iter(self.graf))
        return len(self.bfs(start)) == len(self.graf)

    def shortest_path(self, start, cel):
        from collections import deque
        kolejka = deque([(start, [start])])
        odwiedzone = {start}

        while kolejka:
            węzeł, ścieżka = kolejka.popleft()
            if węzeł == cel:
                return ścieżka
            for sąsiad in self.graf[węzeł]:
                if sąsiad not in odwiedzone:
                    odwiedzone.add(sąsiad)
                    kolejka.append((sąsiad, ścieżka + [sąsiad]))
        return None

    def topological_sort(self):
        from collections import deque
        in_degree = {n: 0 for n in self.graf}
        for sąsiedzi in self.graf.values():
            for s in sąsiedzi:
                in_degree[s] += 1

        kolejka = deque([n for n, d in in_degree.items() if d == 0])
        wynik = []

        while kolejka:
            węzeł = kolejka.popleft()
            wynik.append(węzeł)
            for sąsiad in self.graf[węzeł]:
                in_degree[sąsiad] -= 1
                if in_degree[sąsiad] == 0:
                    kolejka.append(sąsiad)

        return wynik if len(wynik) == len(self.graf) else None

    def __repr__(self):
        return f"Graph(nodes={self.nodes()}, edges={self.edges()})"
    
def dijkstra(graph, start):
    import heapq

    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        current_distance, node = heapq.heappop(queue)

        if current_distance > distances[node]:
            continue

        for neighbor, weight in graph[node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = node
                heapq.heappush(queue, (distance, neighbor))

    return distances, previous

def reconstruct_path(previous, start, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path[0] == start else None


def bfs(graph, start):
    from collections import deque

    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result


def dfs(graph, start):
    visited = set()
    result = []

    def _dfs(node):
        visited.add(node)
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return result