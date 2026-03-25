from sentence_transformers import SentenceTransformer, util
import torch

#Jina demo - Jina wins on our test

model = SentenceTransformer("jinaai/jina-embeddings-v2-base-code", trust_remote_code=True)

code_snippets = [
    "def save_user_profile(user_id, data): return db.users.update(user_id, data)",
    "def validate_token(token): return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])",
    "def sunny(city): return requests.get(f'https://api.weather.com/{city1}')",
    "def rainy(city): return requests.get(f'https://api.weather.com/{city2}')",
    "class connect: def connect(self): self.conn = psycopg2.connect(DB_URL)",
    "def warta(graph): stack=[] while len(stack)!=0: p = stack.pop() for nei in p",
    "def quick_sort(graph): if len(arr) <= 1: return arr pivot = arr[len(arr) // 2] left = [x for x in arr if x < pivot] middle = [x for x in arr if x == pivot] right = [x for x in arr if x > pivot] return quicksort(left) + middle + quicksort(right)"
    "def buble_sort(a): for i in range(len(a)): for j in range(len(a)-i-1): if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]"
]

code_embeddings = model.encode(code_snippets, convert_to_tensor=True)


def intelligent_search(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, code_embeddings)[0]
    best_match_idx = torch.argmax(cosine_scores).item()

    return code_snippets[best_match_idx], cosine_scores[best_match_idx].item()

questions = [
    "Validate user",
    "Connected to database",
    "Load weather",
    "DatabaseConnector",
    "Nice weather",
    "Bad weather",
    "Bfs",
    "sorting",
    "2 fors loops"
]

print("==========================\n")
for q in questions:
    result, score = intelligent_search(q)
    print(f"Pytanie: '{q}'")
    print(f"Znaleziony kod: {result}")
    print(f"Pewność (Score): {score:.4f}\n")