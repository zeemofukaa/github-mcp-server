import ast
from pathlib import Path


def build_dependency_graph(repo):

    graph = {}

    for file in Path(repo).rglob("*.py"):

        try:
            tree = ast.parse(file.read_text(errors="ignore"))
        except Exception:
            continue

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append(node.module)

        graph[str(file.relative_to(repo))] = imports

    return graph