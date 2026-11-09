"""Lesson 1.1.2 - The 2D "map of meaning" from the slides, with real cosine-similarity math.

Free, offline, no packages needed. The coordinates are made up for teaching: real embedding
models use hundreds or thousands of numbers per text, but the math is exactly the same.

  .\\run.ps1 vector_map_2d.py
"""
import math
import sys

sys.dont_write_bytecode = True
import course_env  # noqa: E402,F401  (sets UTF-8 output)

# Same points as the slide "A map of meaning": money words on the right, tech words on the left.
WORDS = {
    "Invoice": (0.85, 0.31),
    "Receipt": (0.82, 0.38),
    "Refund": (0.69, 0.58),
    "Webhook": (-0.31, 0.85),
    "FastAPI": (-0.69, 0.58),
    "Python": (-0.78, 0.45),
}


def cosine(a, b):
    """Compares directions: 1.0 = same meaning, 0 = unrelated, below 0 = pointing away."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))


def bar(score, width=20):
    return "#" * round(max(score, 0) * width)


def main():
    for word, (x, y) in WORDS.items():
        print(f"{word:<8} = [{x:+.2f}, {y:+.2f}]")

    for target in ("Invoice", "Python"):
        print(f"\nCosine similarity to '{target}':")
        others = sorted((w for w in WORDS if w != target),
                        key=lambda w: cosine(WORDS[target], WORDS[w]), reverse=True)
        for word in others:
            score = cosine(WORDS[target], WORDS[word])
            print(f"  {word:<8} {score:+.2f}  {bar(score)}")
    print("\nClose in space = close in meaning. No letters were compared, only numbers.")


if __name__ == "__main__":
    main()
