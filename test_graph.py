from utils.graph_generator import (
    create_mindmap,
    save_graph
)

sample = """
Machine Learning
    Supervised Learning
        Regression
        Classification
    Unsupervised Learning
        Clustering
        Dimensionality Reduction
"""

graph = create_mindmap(
    sample
)

path = save_graph(
    graph,
    "ml_mindmap"
)

print(path)