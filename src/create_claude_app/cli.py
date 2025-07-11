"""Command-line interface for create-claude-app."""
import click
from rich.console import Console
from rich.traceback import install

from . import __version__

# Install rich traceback handler
install(show_locals=True)

console = Console()


def create_project(project_name: str) -> None:
    """Create a new project with the given name.
    
    Args:
        project_name: Name of the project to create
        
    Raises:
        ValueError: If project name is invalid
        FileExistsError: If directory already exists
    """
    # Basic validation
    if not project_name or not project_name.strip():
        raise ValueError("Project name cannot be empty")
    
    # Check for invalid characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    if any(char in project_name for char in invalid_chars):
        raise ValueError("Invalid project name: contains invalid characters")
    
    # For now, just a placeholder - will be implemented later
    console.print(f"[green]Creating project: {project_name}[/green]")


@click.command(name='create-claude-app')
@click.argument('project_name', required=True)
@click.version_option(version=__version__, prog_name='create-claude-app')
def main(project_name: str) -> None:
    """Interactive Python CLI tool that scaffolds new projects optimized for Claude Code development.
    
    Args:
        project_name: Name of the project to create
    """
    try:
        create_project(project_name)
        console.print(f"[green]✅ Project '{project_name}' created successfully![/green]")
    except (ValueError, FileExistsError) as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise click.ClickException(str(e))
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        console.print(f"[yellow]Please report this issue at: https://github.com/swhsiang/create-claude-app/issues[/yellow]")
        raise click.ClickException(str(e))


if __name__ == '__main__':
    main()