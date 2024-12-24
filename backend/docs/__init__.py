"""Documentation package for RunOn backend."""

from pathlib import Path

DOCS_DIR = Path(__file__).parent
OPENAPI_PATH = DOCS_DIR / "openapi.yaml"

__all__ = ["DOCS_DIR", "OPENAPI_PATH"]
