import ast
import pathlib

CORE = pathlib.Path(__file__).resolve().parents[2] / "app" / "core"
FORBIDDEN = ("app.agents", "app.services", "app.api")


def _imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def test_core_does_not_import_upward():
    offenders = []
    for path in CORE.glob("*.py"):
        for module in _imported_modules(path):
            if module.startswith(FORBIDDEN):
                offenders.append(f"{path.name} -> {module}")
    assert offenders == [], f"core/ must not import from agents/services/api: {offenders}"
