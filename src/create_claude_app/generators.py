"""Template generation and project scaffolding."""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from .prompts import ProjectConfiguration
from .file_operations import create_directory_structure, write_file_safe, ProjectStructure
from .validators import validate_directory_not_exists


class TemplateError(Exception):
    """Custom exception for template generation errors."""
    
    def __init__(self, message: str, template: Optional[str] = None):
        super().__init__(message)
        self.template = template


class TemplateGenerator:
    """Template generator for project scaffolding."""
    
    def __init__(self, config: ProjectConfiguration):
        self.config = config


def generate_project(project_path: str, config: ProjectConfiguration) -> Dict[str, Any]:
    """Generate a complete project from configuration.
    
    Args:
        project_path: Path where the project should be created
        config: Project configuration
        
    Returns:
        Dictionary with generation results
        
    Raises:
        TemplateError: If project generation fails
    """
    try:
        # Validate that directory doesn't exist
        validate_directory_not_exists(project_path)
        
        # Create project structure
        structure = ProjectStructure(
            project_name=config.project_name,
            has_frontend=config.frontend is not None,
            has_backend=config.backend is not None,
            has_database=config.database is not None
        )
        
        created_dirs = create_directory_structure(project_path, structure)
        files_created = []
        
        # Generate core files
        project_path_obj = Path(project_path)
        
        # Generate CLAUDE.md
        claude_md_content = generate_claude_md(config)
        claude_md_path = project_path_obj / 'CLAUDE.md'
        write_file_safe(str(claude_md_path), claude_md_content)
        files_created.append(str(claude_md_path))
        
        # Generate .env.example
        env_content = generate_env_example(config)
        env_path = project_path_obj / '.env.example'
        write_file_safe(str(env_path), env_content)
        files_created.append(str(env_path))
        
        # Generate README.md
        readme_content = generate_readme(config)
        readme_path = project_path_obj / 'README.md'
        write_file_safe(str(readme_path), readme_content)
        files_created.append(str(readme_path))
        
        # Generate frontend files
        if config.frontend:
            frontend_files = generate_frontend_files(project_path_obj, config)
            files_created.extend(frontend_files)
        
        # Generate backend files
        if config.backend:
            backend_files = generate_backend_files(project_path_obj, config)
            files_created.extend(backend_files)
        
        # Generate database files
        if config.database:
            database_files = generate_database_files(project_path_obj, config)
            files_created.extend(database_files)
        
        return {
            'success': True,
            'project_path': project_path,
            'directories_created': created_dirs,
            'files_created': files_created
        }
        
    except Exception as e:
        raise TemplateError(f"Failed to generate project: {e}")


def generate_claude_md(config: ProjectConfiguration) -> str:
    """Generate CLAUDE.md content for the project.
    
    Args:
        config: Project configuration
        
    Returns:
        CLAUDE.md content as string
    """
    content = f"""# {config.project_name}

## Project Overview
{config.project_name} is a modern application built with best practices for AI-assisted development using Claude Code.

## Technology Stack
"""
    
    if config.frontend:
        content += f"- **Frontend**: {config.frontend.title()}\n"
        if config.ui_framework:
            ui_name = "Tailwind CSS" if config.ui_framework == "tailwind" else "shadcn/ui"
            content += f"- **UI Framework**: {ui_name}\n"
        if config.package_manager:
            content += f"- **Package Manager**: {config.package_manager}\n"
    
    if config.backend:
        backend_name = "Python (FastAPI)" if config.backend == "python" else config.backend.title()
        content += f"- **Backend**: {backend_name}\n"
    
    if config.database:
        db_name = "PostgreSQL" if config.database == "postgresql" else config.database.title()
        content += f"- **Database**: {db_name}\n"
        if config.use_atlas:
            content += f"- **Migrations**: Atlas\n"
    
    content += """
## Environment Setup

### Prerequisites
- AI API keys (choose one or more):
  - Anthropic Claude API key
  - OpenAI API key  
  - Google Gemini API key

### Installation
1. Copy `.env.example` to `.env`
2. Fill in your API keys in the `.env` file
3. Follow the setup instructions below

## Development Commands

### Setup
```bash
# Copy environment variables
cp .env.example .env

# Edit .env file with your API keys
"""
    
    if config.frontend and config.package_manager:
        content += f"""
# Install frontend dependencies
cd frontend
{config.package_manager} install
"""
    
    if config.backend == "python":
        content += """
# Install backend dependencies
cd backend
pip install -r requirements.txt
"""
    
    if config.database:
        content += """
# Start database (if using Docker)
docker-compose up -d
"""
    
    content += """
```

### Development
```bash
"""
    
    if config.frontend:
        if config.package_manager:
            content += f"""# Start frontend development server
cd frontend
{config.package_manager} run dev
"""
        else:
            content += """# Start frontend development server
cd frontend
npm run dev
"""
    
    if config.backend == "python":
        content += """# Start backend development server
cd backend
uvicorn app.main:app --reload
"""
    
    content += """```

## Project Structure
- **Root**: Configuration files and documentation
"""
    
    if config.frontend:
        content += "- **frontend/**: Frontend application code\n"
    if config.backend:
        content += "- **backend/**: Backend API code\n"
    if config.database:
        content += "- **migrations/**: Database migration files\n"
    
    content += """
## Contributing
1. Follow the existing code style and patterns
2. Write tests for new features
3. Update documentation as needed
4. Use meaningful commit messages

## AI-Assisted Development
This project is optimized for AI-assisted development. The comprehensive documentation and clear structure enable effective collaboration with AI tools like Claude Code.
"""
    
    return content


def generate_env_example(config: ProjectConfiguration) -> str:
    """Generate .env.example content.
    
    Args:
        config: Project configuration
        
    Returns:
        .env.example content as string
    """
    content = """# AI API Keys (choose one or multiple)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
ENV=development
DEBUG=true
"""
    
    if config.database:
        db_display = "PostgreSQL" if config.database == "postgresql" else config.database.title()
        content += f"""
# Database Configuration ({db_display})
DATABASE_URL=your_database_url_here
DB_HOST=localhost
DB_NAME={config.project_name.replace('-', '_')}
DB_USER=your_username
DB_PASSWORD=your_password
"""
        
        if config.database == "postgresql":
            content += "DB_PORT=5432\n"
        elif config.database == "mysql":
            content += "DB_PORT=3306\n"
        elif config.database == "sqlite":
            content += f"DB_FILE={config.project_name}.db\n"
    
    if config.backend:
        content += """
# Backend Settings
PORT=8000
"""
    
    if config.frontend:
        content += """
# Frontend Settings
VITE_API_URL=http://localhost:8000
"""
    
    return content


def generate_readme(config: ProjectConfiguration) -> str:
    """Generate README.md content.
    
    Args:
        config: Project configuration
        
    Returns:
        README.md content as string
    """
    return f"""# {config.project_name}

A modern application built with best practices for AI-assisted development.

## Quick Start

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your API keys

3. See `CLAUDE.md` for detailed setup and development instructions

## Technology Stack

{f"- Frontend: {config.frontend.title()}" if config.frontend else ""}
{f"- Backend: {config.backend.title()}" if config.backend else ""}
{f"- Database: {config.database.title()}" if config.database else ""}

## Documentation

- `CLAUDE.md` - Comprehensive development guide
- `.env.example` - Environment variables template

## Generated with create-claude-app

This project was scaffolded using [create-claude-app](https://github.com/swhsiang/create-claude-app), a tool for creating projects optimized for AI-assisted development.
"""


def generate_frontend_files(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate frontend-specific files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    frontend_path = project_path / 'frontend'
    
    # Generate package.json
    package_json_content = generate_package_json(config)
    if package_json_content:
        package_json_path = frontend_path / 'package.json'
        write_file_safe(str(package_json_path), package_json_content)
        files_created.append(str(package_json_path))
    
    # Generate frontend CLAUDE.md
    frontend_claude_md = generate_frontend_claude_md(config)
    claude_md_path = frontend_path / 'CLAUDE.md'
    write_file_safe(str(claude_md_path), frontend_claude_md)
    files_created.append(str(claude_md_path))
    
    return files_created


def generate_backend_files(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate backend-specific files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    backend_path = project_path / 'backend'
    
    # Generate requirements.txt for Python
    requirements_content = generate_requirements_txt(config)
    if requirements_content:
        requirements_path = backend_path / 'requirements.txt'
        write_file_safe(str(requirements_path), requirements_content)
        files_created.append(str(requirements_path))
    
    # Generate backend CLAUDE.md
    backend_claude_md = generate_backend_claude_md(config)
    claude_md_path = backend_path / 'CLAUDE.md'
    write_file_safe(str(claude_md_path), backend_claude_md)
    files_created.append(str(claude_md_path))
    
    return files_created


def generate_database_files(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate database-specific files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    
    # Generate docker-compose.yml
    docker_compose_content = generate_docker_compose(config)
    if docker_compose_content:
        docker_compose_path = project_path / 'docker-compose.yml'
        write_file_safe(str(docker_compose_path), docker_compose_content)
        files_created.append(str(docker_compose_path))
    
    return files_created


def generate_package_json(config: ProjectConfiguration) -> Optional[str]:
    """Generate package.json content for frontend.
    
    Args:
        config: Project configuration
        
    Returns:
        package.json content as string, or None if not applicable
    """
    if not config.frontend:
        return None
    
    package_data = {
        "name": config.project_name,
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": {},
        "devDependencies": {
            "vite": "^5.0.0"
        }
    }
    
    if config.frontend == "react":
        package_data["dependencies"]["react"] = "^18.0.0"
        package_data["dependencies"]["react-dom"] = "^18.0.0"
        package_data["devDependencies"]["@vitejs/plugin-react"] = "^4.0.0"
    elif config.frontend == "vue":
        package_data["dependencies"]["vue"] = "^3.0.0"
        package_data["devDependencies"]["@vitejs/plugin-vue"] = "^4.0.0"
    
    if config.ui_framework == "tailwind":
        package_data["devDependencies"]["tailwindcss"] = "^3.0.0"
        package_data["devDependencies"]["postcss"] = "^8.0.0"
        package_data["devDependencies"]["autoprefixer"] = "^10.0.0"
    
    return json.dumps(package_data, indent=2)


def generate_requirements_txt(config: ProjectConfiguration) -> Optional[str]:
    """Generate requirements.txt content for Python backend.
    
    Args:
        config: Project configuration
        
    Returns:
        requirements.txt content as string, or None if not applicable
    """
    if config.backend != "python":
        return None
    
    requirements = [
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0"
    ]
    
    if config.database == "postgresql":
        requirements.append("psycopg2-binary>=2.9.0")
        requirements.append("sqlalchemy>=2.0.0")
    elif config.database == "mysql":
        requirements.append("pymysql>=1.0.0")
        requirements.append("sqlalchemy>=2.0.0")
    elif config.database == "sqlite":
        requirements.append("sqlalchemy>=2.0.0")
    
    return "\n".join(requirements) + "\n"


def generate_docker_compose(config: ProjectConfiguration) -> Optional[str]:
    """Generate docker-compose.yml content.
    
    Args:
        config: Project configuration
        
    Returns:
        docker-compose.yml content as string, or None if not applicable
    """
    if not config.database:
        return None
    
    content = "version: '3.8'\n\nservices:\n"
    
    if config.database == "postgresql":
        content += """  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: """ + config.project_name.replace('-', '_') + """
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
    elif config.database == "mysql":
        content += """  mysql:
    image: mysql:8
    environment:
      MYSQL_DATABASE: """ + config.project_name.replace('-', '_') + """
      MYSQL_USER: mysql
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
"""
    
    return content


def generate_frontend_claude_md(config: ProjectConfiguration) -> str:
    """Generate CLAUDE.md for frontend directory."""
    framework_name = config.frontend.title() if config.frontend else "Frontend"
    
    content = f"""# {framework_name} Application

## Overview
{framework_name} frontend application for {config.project_name}.

## Technology Stack
- **Framework**: {framework_name}
"""
    
    if config.ui_framework:
        ui_name = "Tailwind CSS" if config.ui_framework == "tailwind" else "shadcn/ui"
        content += f"- **UI Framework**: {ui_name}\n"
    
    if config.package_manager:
        content += f"- **Package Manager**: {config.package_manager}\n"
    
    content += """
## Development Commands

```bash
# Install dependencies
""" + (config.package_manager or "npm") + """ install

# Start development server
""" + (config.package_manager or "npm") + """ run dev

# Build for production
""" + (config.package_manager or "npm") + """ run build
```

## Project Structure
- `src/` - Source code
- `public/` - Static assets
- `package.json` - Dependencies and scripts

## Development Guidelines
- Follow component-based architecture
- Use TypeScript for type safety
- Write tests for components
- Follow accessibility best practices
"""
    
    return content


def generate_backend_claude_md(config: ProjectConfiguration) -> str:
    """Generate CLAUDE.md for backend directory."""
    backend_name = "Python (FastAPI)" if config.backend == "python" else config.backend.title()
    
    content = f"""# {backend_name} API

## Overview
{backend_name} backend API for {config.project_name}.

## Technology Stack
- **Framework**: {backend_name}
"""
    
    if config.database:
        content += f"- **Database**: {config.database.title()}\n"
    
    content += """
## Development Commands

```bash
"""
    
    if config.backend == "python":
        content += """# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload

# Run tests
pytest tests/
"""
    
    content += """```

## Project Structure
- `app/` - Application code
  - `main.py` - FastAPI application entry point
  - `api/` - API routes
  - `domain/` - Domain models
  - `services/` - Business logic
  - `repositories/` - Data access layer
- `tests/` - Test files

## Development Guidelines
- Follow Domain-Driven Design principles
- Use dependency injection
- Write comprehensive tests
- Follow API versioning best practices
"""
    
    return content