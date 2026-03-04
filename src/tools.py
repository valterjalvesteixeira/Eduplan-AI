from pathlib import Path


def write_file(path: Path, content: str) -> None:
    """
    Create (if needed) the parent folders and write text content to a file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_file(path: Path) -> str:
    """
    Read text content from a file and return it as a string.
    """
    return path.read_text(encoding="utf-8")


def list_dir(path: Path) -> list[str]:
    """
    Return a list with the names of files/folders inside a directory.
    """
    return [p.name for p in path.iterdir()]