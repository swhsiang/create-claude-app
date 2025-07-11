"""Input validation and compatibility checking functions."""
import re
from pathlib import Path
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message)
        self.details = details


def validate_project_name(name: str) -> None:
    """Validate project name for filesystem compatibility.
    
    Args:
        name: Project name to validate
        
    Raises:
        ValidationError: If project name is invalid
    """
    if not name or not name.strip():
        raise ValidationError("Invalid project name: cannot be empty")
    
    # Check for leading/trailing spaces
    if name != name.strip():
        raise ValidationError("Invalid project name: cannot have leading or trailing spaces")
    
    # Check for invalid characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
    for char in invalid_chars:
        if char in name:
            raise ValidationError(f"Invalid project name: contains invalid character '{char}'")


def validate_directory_not_exists(path: str) -> None:
    """Validate that directory or file doesn't already exist.
    
    Args:
        path: Path to check
        
    Raises:
        ValidationError: If directory or file already exists
    """
    path_obj = Path(path)
    
    if path_obj.exists():
        if path_obj.is_dir():
            raise ValidationError(f"Directory already exists: {path}")
        else:
            raise ValidationError(f"File already exists: {path}")


def validate_compatibility(frontend: Optional[str], ui_framework: Optional[str]) -> None:
    """Validate frontend and UI framework compatibility.
    
    Args:
        frontend: Selected frontend framework
        ui_framework: Selected UI framework
        
    Raises:
        ValidationError: If combination is incompatible
    """
    # UI framework requires a frontend framework
    if ui_framework is not None and frontend is None:
        raise ValidationError("UI framework requires a frontend framework")
    
    # shadcn/ui is only compatible with React
    if ui_framework == 'shadcn' and frontend not in ['react']:
        raise ValidationError(f"shadcn/ui is incompatible with {frontend} (React-only)")


def validate_mcp_configuration(use_mcp, project_name: Optional[str] = None) -> None:
    """Validate MCP configuration value.
    
    Args:
        use_mcp: MCP configuration value to validate
        project_name: Optional project name for context
        
    Raises:
        ValidationError: If MCP configuration is invalid
    """
    if not isinstance(use_mcp, bool):
        raise ValidationError("MCP configuration must be a boolean value (True or False)")


def sanitize_input(input_val: Optional[str]) -> Optional[str]:
    """Sanitize user input by trimming whitespace and normalizing.
    
    Args:
        input_val: Input value to sanitize
        
    Returns:
        Sanitized input or None if input was None
    """
    if input_val is None:
        return None
    
    # Convert to string and strip whitespace
    sanitized = str(input_val).strip()
    
    # Convert to lowercase
    sanitized = sanitized.lower()
    
    # Replace multiple whitespace with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return sanitized