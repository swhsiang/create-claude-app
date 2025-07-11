"""Tests for CLI module."""
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from create_claude_app.cli import main


class TestCLI:
    """Test CLI functionality."""

    def test_cli_requires_project_name(self):
        """Test that CLI requires a project name argument."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output

    def test_cli_accepts_project_name(self):
        """Test that CLI accepts a valid project name."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['my-test-project'])
            
            assert result.exit_code == 0
            mock_create.assert_called_once_with('my-test-project')

    def test_cli_shows_help(self):
        """Test that CLI shows help information."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "create-claude-app" in result.output
        assert "Interactive Python CLI tool" in result.output

    def test_cli_shows_version(self):
        """Test that CLI shows version information."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_handles_invalid_project_name(self):
        """Test that CLI handles invalid project names."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.side_effect = ValueError("Invalid project name")
            result = runner.invoke(main, ['invalid/project/name'])
            
            assert result.exit_code != 0
            assert "Invalid project name" in result.output

    def test_cli_handles_existing_directory(self):
        """Test that CLI handles existing directory gracefully."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.side_effect = FileExistsError("Directory already exists")
            result = runner.invoke(main, ['existing-project'])
            
            assert result.exit_code != 0
            assert "Directory already exists" in result.output