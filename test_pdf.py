from utils.pdf_export import (
    create_notes_pdf
)

sample_text = """
Machine Learning Notes

Definition:
Machine learning enables
systems to learn from data.

Types:

1. Supervised Learning
2. Unsupervised Learning
3. Reinforcement Learning
"""

path = create_notes_pdf(
    "ML Lecture",
    sample_text
)

print(path)