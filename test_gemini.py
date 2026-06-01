from utils.gemini_utils import (
    generate_point_summary
)

text = """
Machine learning is a branch of AI.

It allows systems to learn from data.

There are supervised and unsupervised
learning methods.
"""

result = generate_point_summary(
    text
)

print(result)