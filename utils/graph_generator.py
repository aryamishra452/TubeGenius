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

        label = str(
        line.strip()
        .replace("-", "")
        .strip()
       )

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

    dot = graphviz.Digraph(
     comment="Mind Map"
    )

    dot.attr(
     rankdir="TB"
    )

    dot.attr(
     splines="true"
    )

    dot.attr(
     nodesep="0.8"
    )

    dot.attr(
     ranksep="1.2"
    )
    
    dot.attr(
     "node",
     shape="box",
     style="rounded,filled",
     fillcolor="#E0E7FF",
     color="#6366F1",
     fontname="Arial",
     fontsize="12"
    )

    dot.attr(
     size="14,12"
    )

    dot.attr(
        dpi=300
    )

    stack = []

    for node in nodes:

        current_level = node["level"]

        label = str(node["label"])

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