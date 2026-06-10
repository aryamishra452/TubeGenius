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

    text = str(text)

    lines = [
        str(line).rstrip()
        for line in text.split("\n")
        if str(line).strip()
    ]

    nodes = []

    for line in lines:

        indent = (
            len(line)
            - len(line.lstrip())
        )

        level = max(
            0,
            round(indent / 4)
        )

        label = (
            str(line)
            .strip()
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
        rankdir="LR"
    )

    dot.attr(
        splines="true"
    )

    dot.attr(
        nodesep="0.8"
    )

    dot.attr(
        ranksep="3"
    )

    dot.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="#E0E7FF",
        color="#6366F1",
        fontname="Arial",
        fontsize="22"
    )

    dot.attr(
        size="12,24"
    )
    stack = []

    for node in nodes:

        current_level = int(
            node["level"]
        )

        label = str(
            node["label"]
        )

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

            parent = str(
                stack[-1]["label"]
            )

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