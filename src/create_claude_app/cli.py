"""Command-line interface for create-claude-app."""
import click
from pathlib import Path
from rich.console import Console
from rich.traceback import install
from typing import Optional

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
    get_mcp_choice,
)
from .validators import validate_project_name, validate_directory_not_exists, validate_compatibility
from .generators import generate_project

# Install rich traceback handler
install(show_locals=True)

console = Console()

# Valid options for CLI arguments
VALID_FRONTEND_OPTIONS = ['react', 'vue', 'angular', 'none']
VALID_BACKEND_OPTIONS = ['python', 'nodejs', 'golang', 'none']
VALID_DATABASE_OPTIONS = ['mysql', 'postgresql', 'sqlite', 'none']
VALID_UI_OPTIONS = ['tailwind', 'shadcn', 'none']
VALID_BUILD_TOOL_OPTIONS = ['vite', 'webpack', 'babel']
VALID_PACKAGE_MANAGER_OPTIONS = ['npm', 'yarn']


def validate_cli_option(option: str, valid_options: list, option_name: str) -> str:
    """Validate CLI option value.
    
    Args:
        option: The option value to validate
        valid_options: List of valid option values
        option_name: Name of the option for error messages
        
    Returns:
        Validated option value or None for 'none'
        
    Raises:
        click.BadParameter: If option is invalid
    """
    if option not in valid_options:
        valid_str = ', '.join(valid_options)
        raise click.BadParameter(
            f"Invalid {option_name} option '{option}'.\n"
            f"Valid options: {valid_str}"
        )
    return option if option != 'none' else None


def create_project_with_config(project_name: str, config: ProjectConfiguration) -> None:
    """Create a new project with pre-configured settings.
    
    Args:
        project_name: Name of the project to create
        config: Pre-configured project settings
        
    Raises:
        ValueError: If project name is invalid
        FileExistsError: If directory already exists
    """
    console.print(f"[bold cyan]🚀 Welcome to create-claude-app![/bold cyan]")
    console.print(f"Creating a new project: [bold]{project_name}[/bold]\\n")
    
    # Validate project name
    validate_project_name(project_name)
    
    # Check if directory already exists
    project_path = Path.cwd() / project_name
    validate_directory_not_exists(str(project_path))
    
    # Validate compatibility
    validate_compatibility(config.frontend, config.ui_framework)
    
    # Generate the project
    console.print(f"\\n[bold yellow]📁 Generating project structure...[/bold yellow]")
    
    result = generate_project(str(project_path), config)
    
    if result['success']:
        console.print(f"\\n[bold green]✅ Project '{project_name}' created successfully![/bold green]")
        console.print(f"\\n[bold]📋 Summary:[/bold]")
        console.print(f"• Project path: {result['project_path']}")
        console.print(f"• Directories created: {len(result['directories_created'])}")
        console.print(f"• Files generated: {len(result['files_created'])}")
        
        console.print(f"\\n[bold]🎯 Next steps:[/bold]")
        console.print(f"1. [cyan]cd {project_name}[/cyan]")
        console.print(f"2. [cyan]cp .env.example .env[/cyan]")
        console.print(f"3. Edit .env file with your API keys")
        console.print(f"4. Read CLAUDE.md for detailed setup instructions")
        
        if config.frontend and config.package_manager:
            console.print(f"5. [cyan]cd frontend && {config.package_manager} install[/cyan]")
        if config.backend == "python":
            console.print(f"6. [cyan]cd backend && pip install -r requirements.txt[/cyan]")
    else:
        raise Exception("Project generation failed")


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
    use_mcp = get_mcp_choice()
    
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
        use_github_actions=use_github_actions,
        use_mcp=use_mcp
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
@click.option(
    '--frontend', '-f',
    type=click.Choice(VALID_FRONTEND_OPTIONS),
    help='Frontend framework (react, vue, angular, none)'
)
@click.option(
    '--backend', '-B',
    type=click.Choice(VALID_BACKEND_OPTIONS),
    help='Backend language (python, nodejs, golang, none)'
)
@click.option(
    '--database', '-d',
    type=click.Choice(VALID_DATABASE_OPTIONS),
    help='Database system (mysql, postgresql, sqlite, none)'
)
@click.option(
    '--ui', '-u',
    type=click.Choice(VALID_UI_OPTIONS),
    help='UI framework (tailwind, shadcn, none)'
)
@click.option(
    '--build-tool', '-b',
    type=click.Choice(VALID_BUILD_TOOL_OPTIONS),
    help='Frontend build tool (vite, webpack, babel)'
)
@click.option(
    '--package-manager', '-p',
    type=click.Choice(VALID_PACKAGE_MANAGER_OPTIONS),
    help='Package manager (npm, yarn)'
)
@click.option(
    '--atlas', '-a',
    is_flag=True,
    help='Enable Atlas database migrations'
)
@click.option(
    '--github-actions', '-g',
    is_flag=True,
    help='Enable GitHub Actions CI/CD workflows'
)
@click.option(
    '--mcp/--no-mcp', '-m',
    default=True,
    help='Enable/disable MCP (Model Context Protocol) integration (default: enabled)'
)
@click.version_option(version=__version__, prog_name='create-claude-app')
def main(
    project_name: str,
    frontend: Optional[str] = None,
    backend: Optional[str] = None,
    database: Optional[str] = None,
    ui: Optional[str] = None,
    build_tool: Optional[str] = None,
    package_manager: Optional[str] = None,
    atlas: bool = False,
    github_actions: bool = False,
    mcp: bool = True
) -> None:
    """Interactive Python CLI tool that scaffolds new projects optimized for Claude Code development.
    
    Create projects using CLI arguments (non-interactive) or interactive prompts.
    
    Examples:
    
        # Interactive mode (default)
        create-claude-app my-project
        
        # Non-interactive with CLI arguments
        create-claude-app my-project --frontend react --backend python --database mysql
        
        # Mixed mode (some args provided, others use defaults)
        create-claude-app my-project --frontend vue --ui tailwind
    
    Args:
        project_name: Name of the project to create
    """
    try:
        # Check if any CLI arguments were provided
        # Simple approach: if any non-default values are provided, it's CLI mode
        any_args_provided = any([
            frontend is not None,
            backend is not None,
            database is not None,
            ui is not None,
            build_tool is not None,
            package_manager is not None,
            atlas is True,
            github_actions is True,
            mcp is False  # Default is True, so False means --no-mcp was used
        ])
        
        if any_args_provided:
            # Non-interactive mode: use CLI arguments with defaults
            
            # Apply defaults for missing arguments
            final_frontend = validate_cli_option(
                frontend or 'none', VALID_FRONTEND_OPTIONS, 'frontend'
            )
            final_backend = validate_cli_option(
                backend or 'none', VALID_BACKEND_OPTIONS, 'backend'
            )
            final_database = validate_cli_option(
                database or 'none', VALID_DATABASE_OPTIONS, 'database'
            )
            final_ui = validate_cli_option(
                ui or 'none', VALID_UI_OPTIONS, 'UI framework'
            )
            final_build_tool = build_tool or 'vite'
            final_package_manager = package_manager or 'npm'
            
            # Validate build tool and package manager
            validate_cli_option(final_build_tool, VALID_BUILD_TOOL_OPTIONS, 'build tool')
            validate_cli_option(final_package_manager, VALID_PACKAGE_MANAGER_OPTIONS, 'package manager')
            
            # Create configuration
            config = ProjectConfiguration(
                project_name=project_name,
                frontend=final_frontend,
                ui_framework=final_ui,
                backend=final_backend,
                database=final_database,
                package_manager=final_package_manager,
                use_atlas=atlas,
                build_tool=final_build_tool,
                use_github_actions=github_actions,
                use_mcp=mcp
            )
            
            # Validate compatibility early
            try:
                validate_compatibility(config.frontend, config.ui_framework)
            except ValueError as e:
                # Convert to click.BadParameter for better CLI error formatting
                raise click.BadParameter(str(e))
            
            create_project_with_config(project_name, config)
        else:
            # Interactive mode: use existing interactive prompts
            create_project(project_name)
            
        console.print(f"[green]✅ Project '{project_name}' created successfully![/green]")
    except click.BadParameter as e:
        console.print(f"[red]❌ {e}[/red]")
        raise click.ClickException(str(e))
    except (ValueError, FileExistsError) as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise click.ClickException(str(e))
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        console.print(f"[yellow]Please report this issue at: https://github.com/swhsiang/create-claude-app/issues[/yellow]")
        raise click.ClickException(str(e))


if __name__ == '__main__':
    main()