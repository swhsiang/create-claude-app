"""File operations and project structure management."""
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any


class FileOperationError(Exception):
    """Custom exception for file operation errors."""
    
    def __init__(self, message: str, path: Optional[str] = None):
        super().__init__(message)
        self.path = path


@dataclass
class ProjectStructure:
    """Configuration for project directory structure."""
    project_name: str
    has_frontend: bool = False
    has_backend: bool = False
    has_database: bool = False


def create_directory_structure(project_path: str, structure: ProjectStructure) -> List[str]:
    """Create directory structure for the project.
    
    Args:
        project_path: Path to the project root directory
        structure: ProjectStructure configuration
        
    Returns:
        List of created directory paths
        
    Raises:
        FileOperationError: If directory creation fails
    """
    project_path_obj = Path(project_path)
    
    # Check if project directory already exists
    if project_path_obj.exists():
        raise FileOperationError(f"Project directory already exists: {project_path}")
    
    created_dirs = []
    
    try:
        # Create root project directory
        project_path_obj.mkdir(parents=True, exist_ok=False)
        created_dirs.append(str(project_path_obj))
        
        # Create frontend directory if needed
        if structure.has_frontend:
            frontend_dir = project_path_obj / 'frontend'
            frontend_dir.mkdir()
            created_dirs.append(str(frontend_dir))
            
            # Create frontend subdirectories
            (frontend_dir / 'src').mkdir()
            (frontend_dir / 'public').mkdir()
            created_dirs.extend([str(frontend_dir / 'src'), str(frontend_dir / 'public')])
        
        # Create backend directory if needed
        if structure.has_backend:
            backend_dir = project_path_obj / 'backend'
            backend_dir.mkdir()
            created_dirs.append(str(backend_dir))
            
            # Create backend subdirectories
            (backend_dir / 'app').mkdir()
            (backend_dir / 'tests').mkdir()
            created_dirs.extend([str(backend_dir / 'app'), str(backend_dir / 'tests')])
        
        # Create database/migrations directory if needed
        if structure.has_database:
            migrations_dir = project_path_obj / 'migrations'
            migrations_dir.mkdir()
            created_dirs.append(str(migrations_dir))
        
        return created_dirs
        
    except OSError as e:
        # Clean up any created directories on error
        cleanup_on_error(created_dirs)
        raise FileOperationError(f"Failed to create directory structure: {e}")


def write_file_safe(file_path: str, content: str, overwrite: bool = False) -> None:
    """Write content to a file safely.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        overwrite: Whether to overwrite existing files
        
    Raises:
        FileOperationError: If file operation fails
    """
    file_path_obj = Path(file_path)
    
    # Check if file already exists
    if file_path_obj.exists() and not overwrite:
        raise FileOperationError(f"File already exists: {file_path}")
    
    try:
        # Create parent directories if they don't exist
        file_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        file_path_obj.write_text(content, encoding='utf-8')
        
    except OSError as e:
        raise FileOperationError(f"Failed to write file {file_path}: {e}")


def copy_template_file(template_path: str, dest_path: str) -> None:
    """Copy a template file to destination.
    
    Args:
        template_path: Path to the template file
        dest_path: Destination path for the copied file
        
    Raises:
        FileOperationError: If file operation fails
    """
    template_path_obj = Path(template_path)
    dest_path_obj = Path(dest_path)
    
    # Check if template file exists
    if not template_path_obj.exists():
        raise FileOperationError(f"Template file not found: {template_path}")
    
    try:
        # Create parent directories if they don't exist
        dest_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(template_path_obj, dest_path_obj)
        
    except OSError as e:
        raise FileOperationError(f"Failed to copy template file: {e}")


def write_mcp_config_file(project_path: str, mcp_config: Optional[Dict[str, Any]]) -> Optional[str]:
    """Write MCP configuration file to project directory.
    
    Args:
        project_path: Path to the project root directory
        mcp_config: MCP configuration dictionary or None to skip creation
        
    Returns:
        Path to created .mcp.json file or None if config was None
        
    Raises:
        FileOperationError: If file operation fails
    """
    if mcp_config is None:
        return None
    
    project_path_obj = Path(project_path)
    mcp_file_path = project_path_obj / '.mcp.json'
    
    try:
        # Ensure project directory exists
        if not project_path_obj.exists():
            raise FileOperationError(f"Project directory does not exist: {project_path}")
        
        # Write MCP configuration as JSON
        mcp_content = json.dumps(mcp_config, indent=2)
        write_file_safe(str(mcp_file_path), mcp_content)
        
        return str(mcp_file_path)
        
    except (OSError, ValueError, TypeError) as e:
        raise FileOperationError(f"Failed to write MCP configuration: {e}")


def cleanup_on_error(created_paths: List[str]) -> None:
    """Clean up created files and directories on error.
    
    Args:
        created_paths: List of file/directory paths to clean up
    """
    # Sort paths by depth (deepest first) to avoid deletion order issues
    paths_to_clean = sorted(created_paths, key=lambda p: len(Path(p).parts), reverse=True)
    
    for path in paths_to_clean:
        try:
            path_obj = Path(path)
            if path_obj.exists():
                if path_obj.is_dir():
                    # Remove directory and all its contents
                    shutil.rmtree(path_obj)
                else:
                    # Remove file
                    path_obj.unlink()
        except OSError:
            # Ignore errors during cleanup
            pass