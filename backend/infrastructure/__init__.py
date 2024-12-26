"""Infrastructure package for RunOn backend."""

from pathlib import Path

TERRAFORM_DIR = Path(__file__).parent / "terraform"

__all__ = ["TERRAFORM_DIR"]
