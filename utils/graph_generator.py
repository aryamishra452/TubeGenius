import graphviz
from pathlib import Path


GRAPH_FOLDER = "exports"

Path(GRAPH_FOLDER).mkdir(
    exist_ok=True
)


def parse_hierarchy(text):
    """
    Convert indented hierarchy text
    into parent-child relationships.
    """

    lines = [
        line.rstrip()
        for line in text.split("\n")
        if line.strip()
    ]

    nodes = []

    for line in lines:

        indent = (
            len(line)
            - len(line.lstrip())
        )

        level = indent // 4

        label = line.strip()

        nodes.append(
            {
                "level": level,
                "label": label
            }
        )

    return nodes


def build_graph(nodes):
    """
    Create Graphviz graph.
    """

    dot = graphviz.Digraph()

    dot.attr(
        rankdir="TB"
    )

    stack = []

    for node in nodes:

        current_level = node["level"]

        label = node["label"]

        dot.node(
            label,
            label
        )

        while (
            stack
            and
            stack[-1]["level"]
            >= current_level
        ):
            stack.pop()

        if stack:

            parent = stack[-1]["label"]

            dot.edge(
                parent,
                label
            )

        stack.append(node)

    return dot


def create_mindmap(
    hierarchy_text
):
    """
    Generate Graphviz object.
    """

    nodes = parse_hierarchy(
        hierarchy_text
    )

    graph = build_graph(
        nodes
    )

    return graph


def save_graph(
    graph,
    filename="mindmap"
):
    """
    Save graph as PNG.
    """

    filepath = (
        f"{GRAPH_FOLDER}/{filename}"
    )

    graph.render(
        filepath,
        format="png",
        cleanup=True
    )

    return (
        filepath + ".png"
    )