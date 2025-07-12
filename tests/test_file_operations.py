"""Tests for file operations module."""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from create_claude_app.file_operations import (
    create_directory_structure,
    write_file_safe,
    copy_template_file,
    cleanup_on_error,
    write_mcp_config_file,
    FileOperationError,
    ProjectStructure,
)


class TestFileOperations:
    """Test file operations functionality."""

    def test_create_directory_structure_success(self):
        """Test successful directory structure creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'test-project'
            
            structure = ProjectStructure(
                project_name='test-project',
                has_frontend=True,
                has_backend=True,
                has_database=True
            )
            
            created_dirs = create_directory_structure(str(project_path), structure)
            
            # Check that directories were created
            assert project_path.exists()
            assert (project_path / 'frontend').exists()
            assert (project_path / 'backend').exists()
            assert (project_path / 'migrations').exists()
            
            # Check return value
            assert str(project_path) in created_dirs
            assert str(project_path / 'frontend') in created_dirs
            assert str(project_path / 'backend') in created_dirs

    def test_create_directory_structure_minimal(self):
        """Test directory structure creation with minimal options."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'minimal-project'
            
            structure = ProjectStructure(
                project_name='minimal-project',
                has_frontend=False,
                has_backend=False,
                has_database=False
            )
            
            created_dirs = create_directory_structure(str(project_path), structure)
            
            # Check that only root directory was created
            assert project_path.exists()
            assert not (project_path / 'frontend').exists()
            assert not (project_path / 'backend').exists()
            assert not (project_path / 'migrations').exists()
            
            # Check return value
            assert str(project_path) in created_dirs
            assert len(created_dirs) == 1

    def test_create_directory_structure_already_exists(self):
        """Test error when directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'existing-project'
            project_path.mkdir()
            
            structure = ProjectStructure(
                project_name='existing-project',
                has_frontend=True,
                has_backend=False,
                has_database=False
            )
            
            with pytest.raises(FileOperationError) as exc_info:
                create_directory_structure(str(project_path), structure)
            
            assert 'already exists' in str(exc_info.value)

    def test_write_file_safe_success(self):
        """Test successful file writing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'test.txt'
            content = 'Hello, World!'
            
            write_file_safe(str(file_path), content)
            
            # Check that file was created with correct content
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_write_file_safe_create_parent_dirs(self):
        """Test file writing with parent directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'subdir' / 'test.txt'
            content = 'Test content'
            
            write_file_safe(str(file_path), content)
            
            # Check that parent directory was created
            assert file_path.parent.exists()
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_write_file_safe_overwrite_protection(self):
        """Test that existing files are not overwritten by default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'existing.txt'
            original_content = 'Original content'
            new_content = 'New content'
            
            # Create existing file
            file_path.write_text(original_content)
            
            # Try to write new content (should fail)
            with pytest.raises(FileOperationError) as exc_info:
                write_file_safe(str(file_path), new_content)
            
            assert 'already exists' in str(exc_info.value)
            assert file_path.read_text() == original_content

    def test_write_file_safe_with_overwrite(self):
        """Test file writing with overwrite flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'overwrite.txt'
            original_content = 'Original content'
            new_content = 'New content'
            
            # Create existing file
            file_path.write_text(original_content)
            
            # Write new content with overwrite=True
            write_file_safe(str(file_path), new_content, overwrite=True)
            
            assert file_path.read_text() == new_content

    def test_copy_template_file_success(self):
        """Test successful template file copying."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source template file
            template_path = Path(temp_dir) / 'template.txt'
            template_content = 'Template content'
            template_path.write_text(template_content)
            
            # Copy to destination
            dest_path = Path(temp_dir) / 'dest.txt'
            copy_template_file(str(template_path), str(dest_path))
            
            # Check that file was copied
            assert dest_path.exists()
            assert dest_path.read_text() == template_content

    def test_copy_template_file_source_not_found(self):
        """Test error when source template file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / 'nonexistent.txt'
            dest_path = Path(temp_dir) / 'dest.txt'
            
            with pytest.raises(FileOperationError) as exc_info:
                copy_template_file(str(template_path), str(dest_path))
            
            assert 'Template file not found' in str(exc_info.value)

    def test_cleanup_on_error_success(self):
        """Test successful cleanup of created files and directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some files and directories
            created_paths = []
            
            dir1 = Path(temp_dir) / 'dir1'
            dir1.mkdir()
            created_paths.append(str(dir1))
            
            file1 = dir1 / 'file1.txt'
            file1.write_text('content')
            created_paths.append(str(file1))
            
            dir2 = Path(temp_dir) / 'dir2'
            dir2.mkdir()
            created_paths.append(str(dir2))
            
            # Verify they exist
            assert dir1.exists()
            assert file1.exists()
            assert dir2.exists()
            
            # Cleanup
            cleanup_on_error(created_paths)
            
            # Verify they were deleted
            assert not dir1.exists()
            assert not file1.exists()
            assert not dir2.exists()

    def test_cleanup_on_error_handles_missing_files(self):
        """Test cleanup handles missing files gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some paths, some existing, some not
            existing_dir = Path(temp_dir) / 'existing'
            existing_dir.mkdir()
            
            nonexistent_file = Path(temp_dir) / 'nonexistent.txt'
            
            created_paths = [str(existing_dir), str(nonexistent_file)]
            
            # Should not raise exception
            cleanup_on_error(created_paths)
            
            # Existing directory should be cleaned up
            assert not existing_dir.exists()

    def test_project_structure_dataclass(self):
        """Test ProjectStructure dataclass."""
        structure = ProjectStructure(
            project_name='test-project',
            has_frontend=True,
            has_backend=True,
            has_database=True
        )
        
        assert structure.project_name == 'test-project'
        assert structure.has_frontend is True
        assert structure.has_backend is True
        assert structure.has_database is True

    def test_project_structure_defaults(self):
        """Test ProjectStructure with default values."""
        structure = ProjectStructure(project_name='test-project')
        
        assert structure.project_name == 'test-project'
        assert structure.has_frontend is False
        assert structure.has_backend is False
        assert structure.has_database is False

    def test_file_operation_error_is_exception(self):
        """Test that FileOperationError is a proper exception."""
        error = FileOperationError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_file_operation_error_with_path(self):
        """Test FileOperationError with file path."""
        error = FileOperationError("Test error", path="/test/path")
        assert str(error) == "Test error"
        assert error.path == "/test/path"

    def test_write_mcp_config_file_success(self):
        """Test successful MCP configuration file writing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'mcp-project'
            project_path.mkdir()
            
            mcp_config = {
                "mcpServers": {
                    "context7": {
                        "command": "npx",
                        "args": ["-y", "@upstash/context7-mcp"],
                        "env": {}
                    }
                }
            }
            
            file_path = write_mcp_config_file(str(project_path), mcp_config)
            
            # Check that file was created
            mcp_file = project_path / '.mcp.json'
            assert mcp_file.exists()
            assert file_path == str(mcp_file)
            
            # Check content
            import json
            content = json.loads(mcp_file.read_text())
            assert content == mcp_config

    def test_write_mcp_config_file_with_none_config(self):
        """Test MCP config file writing with None config (should not create file)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'no-mcp-project'
            project_path.mkdir()
            
            file_path = write_mcp_config_file(str(project_path), None)
            
            # Check that no file was created
            mcp_file = project_path / '.mcp.json'
            assert not mcp_file.exists()
            assert file_path is None

    def test_write_mcp_config_file_invalid_path(self):
        """Test MCP config file writing with invalid project path."""
        nonexistent_path = "/nonexistent/path"
        mcp_config = {"mcpServers": {}}
        
        with pytest.raises(FileOperationError) as exc_info:
            write_mcp_config_file(nonexistent_path, mcp_config)
        
        assert 'Project directory does not exist' in str(exc_info.value)

    def test_write_mcp_config_file_invalid_json(self):
        """Test MCP config file writing with invalid JSON data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / 'invalid-json-project'
            project_path.mkdir()
            
            # Create invalid JSON data (circular reference)
            invalid_config = {}
            invalid_config['self'] = invalid_config
            
            with pytest.raises(FileOperationError) as exc_info:
                write_mcp_config_file(str(project_path), invalid_config)
            
            assert 'Failed to write MCP configuration' in str(exc_info.value)