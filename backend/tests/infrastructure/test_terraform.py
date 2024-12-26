"""Tests for Terraform configuration."""

from infrastructure import TERRAFORM_DIR


def test_terraform_dir_exists():
    """Test that Terraform directory exists."""
    assert TERRAFORM_DIR.exists()
    assert TERRAFORM_DIR.is_dir()


def test_terraform_files_exist():
    """Test that required Terraform files exist."""
    required_files = ["main.tf", "variables.tf", "outputs.tf"]
    for file in required_files:
        assert (TERRAFORM_DIR / file).exists()
        assert (TERRAFORM_DIR / file).is_file()
