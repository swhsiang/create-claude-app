"""Tests for validators module."""
import pytest
import tempfile
import os
from pathlib import Path
from create_claude_app.validators import (
    validate_project_name,
    validate_directory_not_exists,
    validate_compatibility,
    validate_mcp_configuration,
    sanitize_input,
    ValidationError,
)


class TestValidators:
    """Test input validation functions."""

    def test_validate_project_name_valid_names(self):
        """Test valid project names."""
        valid_names = [
            'my-project',
            'my_project',
            'myproject',
            'my-project-123',
            'project2',
            'a',
            'z' * 100,  # Long but valid
        ]
        
        for name in valid_names:
            validate_project_name(name)  # Should not raise

    def test_validate_project_name_invalid_names(self):
        """Test invalid project names."""
        invalid_names = [
            '',
            ' ',
            '   ',
            'my/project',
            'my\\project',
            'my:project',
            'my*project',
            'my?project',
            'my"project',
            'my<project',
            'my>project',
            'my|project',
            'my project',  # Space in middle
            ' myproject',  # Leading space
            'myproject ',  # Trailing space
        ]
        
        for name in invalid_names:
            with pytest.raises(ValidationError) as exc_info:
                validate_project_name(name)
            assert 'Invalid project name' in str(exc_info.value)

    def test_validate_directory_not_exists_success(self):
        """Test validation when directory does not exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existent_path = Path(temp_dir) / 'non-existent-project'
            validate_directory_not_exists(str(non_existent_path))  # Should not raise

    def test_validate_directory_not_exists_failure(self):
        """Test validation when directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_path = Path(temp_dir) / 'existing-project'
            existing_path.mkdir()
            
            with pytest.raises(ValidationError) as exc_info:
                validate_directory_not_exists(str(existing_path))
            assert 'Directory already exists' in str(exc_info.value)

    def test_validate_directory_not_exists_file_exists(self):
        """Test validation when a file with the same name exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_file = Path(temp_dir) / 'existing-file'
            existing_file.touch()
            
            with pytest.raises(ValidationError) as exc_info:
                validate_directory_not_exists(str(existing_file))
            assert 'already exists' in str(exc_info.value)

    def test_validate_compatibility_valid_combinations(self):
        """Test valid frontend/UI framework combinations."""
        valid_combinations = [
            ('react', 'tailwind'),
            ('react', 'shadcn'),
            ('react', None),
            ('vue', 'tailwind'),
            ('vue', None),
            ('angular', 'tailwind'),
            ('angular', None),
            (None, None),
        ]
        
        for frontend, ui_framework in valid_combinations:
            validate_compatibility(frontend, ui_framework)  # Should not raise

    def test_validate_compatibility_invalid_combinations(self):
        """Test invalid frontend/UI framework combinations."""
        invalid_combinations = [
            ('angular', 'shadcn'),
            ('vue', 'shadcn'),
        ]
        
        for frontend, ui_framework in invalid_combinations:
            with pytest.raises(ValidationError) as exc_info:
                validate_compatibility(frontend, ui_framework)
            assert 'incompatible' in str(exc_info.value).lower()

    def test_validate_compatibility_none_frontend_with_ui_framework(self):
        """Test that UI framework with no frontend raises error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_compatibility(None, 'tailwind')
        assert 'UI framework requires a frontend framework' in str(exc_info.value)

    def test_sanitize_input_basic(self):
        """Test basic input sanitization."""
        test_cases = [
            ('  hello  ', 'hello'),
            ('HELLO', 'hello'),
            ('Hello World', 'hello world'),
            ('', ''),
            ('   ', ''),
            ('React', 'react'),
            ('Node.js', 'node.js'),
        ]
        
        for input_val, expected in test_cases:
            result = sanitize_input(input_val)
            assert result == expected

    def test_sanitize_input_none(self):
        """Test sanitizing None input."""
        result = sanitize_input(None)
        assert result is None

    def test_sanitize_input_special_characters(self):
        """Test sanitizing input with special characters."""
        test_cases = [
            ('hello\nworld', 'hello world'),
            ('hello\tworld', 'hello world'),
            ('hello\r\nworld', 'hello world'),
            ('hello   world', 'hello world'),
        ]
        
        for input_val, expected in test_cases:
            result = sanitize_input(input_val)
            assert result == expected

    def test_validation_error_is_exception(self):
        """Test that ValidationError is a proper exception."""
        error = ValidationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_validation_error_with_details(self):
        """Test ValidationError with additional details."""
        error = ValidationError("Test error", details="Additional info")
        assert str(error) == "Test error"
        assert error.details == "Additional info"

    def test_validate_mcp_configuration_valid(self):
        """Test valid MCP configuration validation."""
        # Valid boolean values
        validate_mcp_configuration(True)  # Should not raise
        validate_mcp_configuration(False)  # Should not raise

    def test_validate_mcp_configuration_invalid(self):
        """Test invalid MCP configuration validation."""
        invalid_values = [
            "true",  # String instead of bool
            "false", # String instead of bool
            1,       # Integer instead of bool
            0,       # Integer instead of bool
            None,    # None instead of bool
            "yes",   # String
            "no",    # String
        ]
        
        for value in invalid_values:
            with pytest.raises(ValidationError) as exc_info:
                validate_mcp_configuration(value)
            assert 'MCP configuration must be a boolean value' in str(exc_info.value)

    def test_validate_mcp_configuration_with_project_name(self):
        """Test MCP configuration validation with project context."""
        # Should work with any valid boolean regardless of project name
        validate_mcp_configuration(True, project_name="test-project")
        validate_mcp_configuration(False, project_name="another-project")

    def test_validate_compatibility_with_mcp_combinations(self):
        """Test that MCP works with all frontend/backend combinations."""
        # MCP should be compatible with any technology stack
        combinations = [
            ('react', 'tailwind', 'python', True),
            ('vue', 'tailwind', 'nodejs', True),
            ('angular', None, 'golang', True),
            (None, None, None, True),
            ('react', 'shadcn', 'python', False),
            (None, None, None, False),
        ]
        
        for frontend, ui_framework, backend, use_mcp in combinations:
            # Validate base compatibility first
            if frontend is not None or ui_framework is not None:
                validate_compatibility(frontend, ui_framework)
            
            # MCP should not affect compatibility
            validate_mcp_configuration(use_mcp)