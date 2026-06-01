from utils.rag_chat import (
    build_vector_store,
    ask_video
)

sample_text = """
Machine learning is a branch
of artificial intelligence.

Supervised learning uses
labeled data.

Unsupervised learning uses
unlabeled data.

Regression predicts
continuous values.

Classification predicts
categories.
"""

build_vector_store(
    sample_text
)

answer = ask_video(
    "What is regression?"
)

print(answer)