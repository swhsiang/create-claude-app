"""User interaction prompts for project configuration."""
from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


@dataclass
class ProjectConfiguration:
    """Configuration for a new project."""
    project_name: str
    frontend: Optional[str] = None
    ui_framework: Optional[str] = None
    backend: Optional[str] = None
    database: Optional[str] = None
    package_manager: Optional[str] = None
    use_atlas: bool = False
    build_tool: Optional[str] = None
    use_github_actions: bool = False
    use_mcp: bool = False


def get_frontend_choice() -> Optional[str]:
    """Get user's frontend framework choice.
    
    Returns:
        Selected frontend framework or None if skipped
    """
    console.print("\n[bold cyan]Frontend Framework Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Framework", style="white")
    
    table.add_row("1", "React")
    table.add_row("2", "Vue")
    table.add_row("3", "Angular")
    table.add_row("4", "Skip")
    
    console.print(table)
    
    choice = Prompt.ask(
        "Select frontend framework",
        choices=["1", "2", "3", "4"],
        default="4"
    )
    
    choices_map = {
        "1": "react",
        "2": "vue",
        "3": "angular",
        "4": None
    }
    
    return choices_map[choice]


def get_ui_framework_choice(frontend: Optional[str]) -> Optional[str]:
    """Get user's UI framework choice.
    
    Args:
        frontend: Selected frontend framework
        
    Returns:
        Selected UI framework or None if skipped or incompatible
    """
    if frontend is None:
        return None
    
    console.print("\n[bold cyan]UI Framework Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Framework", style="white")
    
    table.add_row("1", "Tailwind CSS")
    table.add_row("2", "shadcn/ui")
    table.add_row("3", "None/Skip")
    
    console.print(table)
    
    # Check for incompatible combinations
    if frontend == "angular":
        console.print("[yellow]⚠️  Warning: shadcn/ui is not recommended with Angular (React-specific)[/yellow]")
    
    choice = Prompt.ask(
        "Select UI framework",
        choices=["1", "2", "3"],
        default="3"
    )
    
    choices_map = {
        "1": "tailwind",
        "2": "shadcn",
        "3": None
    }
    
    return choices_map[choice]


def get_backend_choice() -> Optional[str]:
    """Get user's backend framework choice.
    
    Returns:
        Selected backend framework or None if skipped
    """
    console.print("\n[bold cyan]Backend Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Framework", style="white")
    
    table.add_row("1", "Python")
    table.add_row("2", "Node.js")
    table.add_row("3", "Golang")
    table.add_row("4", "Skip")
    
    console.print(table)
    
    choice = Prompt.ask(
        "Select backend framework",
        choices=["1", "2", "3", "4"],
        default="4"
    )
    
    choices_map = {
        "1": "python",
        "2": "nodejs",
        "3": "golang",
        "4": None
    }
    
    return choices_map[choice]


def get_database_choice() -> Optional[str]:
    """Get user's database choice.
    
    Returns:
        Selected database or None if skipped
    """
    console.print("\n[bold cyan]Database Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Database", style="white")
    
    table.add_row("1", "MySQL")
    table.add_row("2", "PostgreSQL")
    table.add_row("3", "SQLite")
    table.add_row("4", "Skip")
    
    console.print(table)
    
    choice = Prompt.ask(
        "Select database",
        choices=["1", "2", "3", "4"],
        default="4"
    )
    
    choices_map = {
        "1": "mysql",
        "2": "postgresql",
        "3": "sqlite",
        "4": None
    }
    
    return choices_map[choice]


def get_package_manager_choice(frontend: Optional[str]) -> Optional[str]:
    """Get user's package manager choice for frontend projects.
    
    Args:
        frontend: Selected frontend framework
        
    Returns:
        Selected package manager or None if no frontend
    """
    if not frontend:
        return None
    
    console.print("\n[bold cyan]Package Manager Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Package Manager", style="white")
    
    table.add_row("1", "npm")
    table.add_row("2", "yarn")
    
    console.print(table)
    
    choice = Prompt.ask(
        "Select package manager",
        choices=["1", "2"],
        default="1"
    )
    
    choices_map = {
        "1": "npm",
        "2": "yarn"
    }
    
    return choices_map[choice]


def get_atlas_choice() -> bool:
    """Get user's Atlas migration tool choice.
    
    Returns:
        True if user wants Atlas, False otherwise
    """
    console.print("\n[bold cyan]Database Migration Tool:[/bold cyan]")
    return Confirm.ask(
        "Would you like to include Atlas migration tool?",
        default=True
    )


def get_build_tool_choice(frontend: Optional[str]) -> Optional[str]:
    """Get user's build tool choice.
    
    Args:
        frontend: Selected frontend framework
        
    Returns:
        Selected build tool or None if no frontend selected
    """
    if not frontend:
        return None
        
    console.print("\n[bold cyan]Frontend Build Tool Options:[/bold cyan]")
    table = Table(show_header=False, show_lines=False)
    table.add_column("Option", style="cyan")
    table.add_column("Build Tool", style="white")
    table.add_column("Description", style="dim")
    
    table.add_row("1", "Vite", "(recommended - fast HMR, optimized builds)")
    table.add_row("2", "Webpack", "(traditional bundling with extensive configuration)")
    table.add_row("3", "Babel + Webpack", "(custom transpilation with webpack bundling)")
    
    console.print(table)
    
    choice = Prompt.ask(
        "Select build tool",
        choices=["1", "2", "3"],
        default="1"
    )
    
    choices_map = {
        "1": "vite",
        "2": "webpack", 
        "3": "babel"
    }
    
    return choices_map[choice]


def get_github_actions_choice() -> bool:
    """Get user's GitHub Actions CI/CD choice.
    
    Returns:
        True if user wants GitHub Actions, False otherwise
    """
    console.print("\n[bold cyan]GitHub Actions CI/CD:[/bold cyan]")
    return Confirm.ask(
        "Would you like to include GitHub Actions workflows?",
        default=True
    )


def get_mcp_choice() -> bool:
    """Get user's MCP (Model Context Protocol) configuration choice.
    
    Returns:
        True if user wants MCP integration, False otherwise
    """
    console.print("\n[bold cyan]Model Context Protocol (MCP) Integration:[/bold cyan]")
    console.print("[dim]MCP enhances AI-assisted development with project-aware context using Context7[/dim]")
    console.print("[dim]• Intelligent project understanding and navigation[/dim]")
    console.print("[dim]• Enhanced Claude Desktop integration[/dim]")
    console.print("[dim]• Context-aware AI assistance[/dim]")
    
    return Confirm.ask(
        "Would you like to include MCP configuration? (recommended)",
        default=True
    )