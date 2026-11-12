from os import path
from pathlib import Path
from unittest import result

# Directorio raíz del repositorio

PROJECT_ROOT = Path(__file__).resolve().parents[4]

# Directorio autorizado para consultar documentos
KNOWLEDGE_DIR = (
    PROJECT_ROOT / "projects" / "academic" / "knowledge"
).resolve()

def resolve_file(relative_path: str) -> Path:
    """
    Resuelve una ruta relativa dentro del repositorio
    de conocimiento y evita accesos fuere del directorio.
    """
    candidate = (KNOWLEDGE_DIR / relative_path).resolve()

    if not candidate.is_relative_to(KNOWLEDGE_DIR):
        raise ValueError("Access outside knowledge directory is forbidden")
    if candidate.suffix.lower() not in {".md", ".txt"}:
        raise ValueError("Only Markdown and TXT files are allowed")
    return candidate

def list_files() -> list[str]:
    """
    Returns the available Markdown and TXT files.
    """
    if not KNOWLEDGE_DIR.exists():
        return []
    return sorted(
        str(path.relative_to(KNOWLEDGE_DIR))
        for path in KNOWLEDGE_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".txt"}
    )

def read_file(relative_path: str) -> str:
    """
    Reads a document from the knowledge repository.
    """

    file_path= resolve_file(relative_path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Document not found: {relative_path}"
        )
    return file_path.read_text(encoding="utf-8")

def search_files(query: str) -> list[dict[str, str]]:
    """
    Searches documents using individual query terms.
    """

    if not query.strip():
        raise ValueError("Searh query cannot be empty")

    terms = query.casefold().split()
    results = []

    for relative_path in list_files():

        content = read_file(relative_path)
        normalized_content = content.casefold()
        matches = [
            term for term in terms
            if term in normalized_content
        ]

        if matches:
            results.append({
                "file": relative_path,
                "matched_terms": matches,
                "content": content
            })
            
    return results