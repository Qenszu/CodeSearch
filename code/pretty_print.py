def pretty_print(result):
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0] if "distances" in result else None

    print("\n= RESULTS =\n")

    for i, doc in enumerate(documents):
        meta = metadatas[i]

        print(f" Result #{i+1}")
        print(f" File: {meta.get('file')}")
        print(f" Index: {meta.get('index')}")

        if distances:
            print(f" Score (distance): {distances[i]:.4f}")

        print("\n Code:")
        print(doc)
        print("\n---------------------------------------------\n")