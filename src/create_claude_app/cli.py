"""Command-line interface for create-claude-app."""
import click
from pathlib import Path
from rich.console import Console
from rich.traceback import install

from . import __version__
from .prompts import (
    ProjectConfiguration,
    get_frontend_choice,
    get_ui_framework_choice,
    get_backend_choice,
    get_database_choice,
    get_package_manager_choice,
    get_atlas_choice,
    get_build_tool_choice,
    get_github_actions_choice,
)
from .validators import validate_project_name, validate_directory_not_exists, validate_compatibility
from .generators import generate_project

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
    console.print(f"[bold cyan]🚀 Welcome to create-claude-app![/bold cyan]")
    console.print(f"Creating a new project: [bold]{project_name}[/bold]\n")
    
    # Validate project name
    validate_project_name(project_name)
    
    # Check if directory already exists
    project_path = Path.cwd() / project_name
    validate_directory_not_exists(str(project_path))
    
    # Get user choices through interactive prompts
    console.print("[bold]Let's configure your project:[/bold]")
    
    frontend = get_frontend_choice()
    ui_framework = get_ui_framework_choice(frontend)
    build_tool = get_build_tool_choice(frontend)
    backend = get_backend_choice()
    database = get_database_choice()
    package_manager = get_package_manager_choice(frontend)
    use_atlas = get_atlas_choice() if database else False
    use_github_actions = get_github_actions_choice()
    
    # Validate compatibility
    validate_compatibility(frontend, ui_framework)
    
    # Create project configuration
    config = ProjectConfiguration(
        project_name=project_name,
        frontend=frontend,
        ui_framework=ui_framework,
        backend=backend,
        database=database,
        package_manager=package_manager,
        use_atlas=use_atlas,
        build_tool=build_tool,
        use_github_actions=use_github_actions
    )
    
    # Generate the project
    console.print(f"\n[bold yellow]📁 Generating project structure...[/bold yellow]")
    
    result = generate_project(str(project_path), config)
    
    if result['success']:
        console.print(f"\n[bold green]✅ Project '{project_name}' created successfully![/bold green]")
        console.print(f"\n[bold]📋 Summary:[/bold]")
        console.print(f"• Project path: {result['project_path']}")
        console.print(f"• Directories created: {len(result['directories_created'])}")
        console.print(f"• Files generated: {len(result['files_created'])}")
        
        console.print(f"\n[bold]🎯 Next steps:[/bold]")
        console.print(f"1. [cyan]cd {project_name}[/cyan]")
        console.print(f"2. [cyan]cp .env.example .env[/cyan]")
        console.print(f"3. Edit .env file with your API keys")
        console.print(f"4. Read CLAUDE.md for detailed setup instructions")
        
        if frontend and package_manager:
            console.print(f"5. [cyan]cd frontend && {package_manager} install[/cyan]")
        if backend == "python":
            console.print(f"6. [cyan]cd backend && pip install -r requirements.txt[/cyan]")
    else:
        raise Exception("Project generation failed")


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