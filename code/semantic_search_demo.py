"""Lesson 1.1.2 - Real embeddings, on your own computer: meaning search and the SKU trap.

Free, no API key. Uses a small open embedding model (BAAI/bge-small-en-v1.5, 384 numbers per
text) that runs locally. The first run downloads it once (about 70 MB, saved outside this folder).
Paid embedding APIs work the same way with longer vectors (1,024 to 3,072 numbers).

  .\\run.ps1 semantic_search_demo.py
  .\\run.ps1 semantic_search_demo.py --query "your own question"
"""
import argparse
import re
import sys

sys.dont_write_bytecode = True
from course_env import cache_path  # noqa: E402

MODEL = "BAAI/bge-small-en-v1.5"

TICKETS = [
    "Please issue a refund for my invoice",
    "How do I reset my password?",
    "Our webhook returns a 500 error",
]

CATALOG = [
    "SKU-8842-A | Hydraulic pump seal kit, large | $57.90",
    "SKU-8841-B | Hydraulic pump seal kit, small | $42.10",
    "SKU-8814-B | Hydraulic hose clamp | $6.25",
    "SKU-1203-C | Office chair armrest | $18.00",
    "SKU-8841-D | Hydraulic pump seal kit, medium | $49.50",
]


def load_model():
    print(f"Loading {MODEL} (first run: downloads ~70 MB, then it's offline)...")
    from fastembed import TextEmbedding
    return TextEmbedding(MODEL, cache_dir=str(cache_path("fastembed")))


def cosine(a, b):
    import numpy as np
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def bar(score, lo=0.4, width=30):
    """Scores here sit between ~0.4 and 1.0, so the bar starts at 0.4 to make gaps visible."""
    return "#" * max(0, round((score - lo) / (1 - lo) * width))


def rank(model, query, docs):
    vectors = list(model.embed([query] + docs))
    scores = [cosine(vectors[0], v) for v in vectors[1:]]
    return sorted(zip(scores, docs), reverse=True)


def sku_search(model, query):
    wanted = re.search(r"SKU-\d{4}-[A-Z]", query)
    print(f'\nQUERY: "{query}"')
    print("  Vector search (meaning):")
    for i, (score, doc) in enumerate(rank(model, query, CATALOG)):
        mark = ""
        if i == 0 and wanted:
            mark = "  <- right part" if doc.startswith(wanted.group()) else "  <- WRONG part, wrong price"
        print(f"    {score:.3f} {bar(score):<30} {doc}{mark}")
    if wanted:
        hits = [doc for doc in CATALOG if wanted.group() in doc]
        print(f"  Keyword search (exact text '{wanted.group()}'):")
        for doc in hits:
            print(f"    exact match                          {doc}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--query", help="search the part catalog with your own question")
    args = p.parse_args()
    model = load_model()

    if args.query:
        sku_search(model, args.query)
        return

    first = next(iter(model.embed(["I want my money back"])))
    print(f'\nAn embedding is just a list of numbers. "I want my money back" =')
    print("  [" + ", ".join(f"{x:+.3f}" for x in first[:6]) + f", ... ]   ({len(first)} numbers)")

    print('\n1) MEANING WITHOUT SHARED WORDS   query: "I want my money back"')
    for score, doc in rank(model, "I want my money back", TICKETS):
        print(f"    {score:.3f} {bar(score):<30} {doc}")
    print("    The refund ticket wins, and it shares no word with the query.")

    print("\n2) THE SKU TRAP: same part number, two ways of asking")
    sku_search(model, "What is the price of part SKU-8841-B?")
    sku_search(model, "price of SKU-8841-B")
    print("\nAll the scores sit close together: to an embedding, every part number looks alike."
          "\nFix: hybrid search = vector search for meaning + keyword search for exact IDs (Module 6).")


if __name__ == "__main__":
    main()
