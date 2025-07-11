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
        
        # Generate GitHub Actions workflows
        if config.use_github_actions:
            workflow_files = generate_github_actions_files(project_path_obj, config)
            files_created.extend(workflow_files)
        
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
    content = f"""# {config.project_name}

A modern application built with best practices for AI-assisted development.

## Quick Start Guide

1. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your API keys**

3. **Install dependencies and start development servers** (see sections below)

## Technology Stack

"""
    
    # Add technology stack details
    if config.frontend:
        frontend_display = config.frontend.title()
        if config.build_tool:
            build_tool_display = config.build_tool.title()
            if config.build_tool == 'babel':
                build_tool_display = 'Babel + Webpack'
            frontend_display += f" ({build_tool_display})"
        content += f"- **Frontend**: {frontend_display}\n"
        
        if config.ui_framework:
            ui_display = "Tailwind CSS" if config.ui_framework == "tailwind" else "shadcn/ui"
            content += f"- **UI Framework**: {ui_display}\n"
    
    if config.backend:
        backend_display = "Python (FastAPI)" if config.backend == "python" else config.backend.title()
        content += f"- **Backend**: {backend_display}\n"
    
    if config.database:
        db_display = "PostgreSQL" if config.database == "postgresql" else ("MySQL" if config.database == "mysql" else config.database.title())
        content += f"- **Database**: {db_display}\n"
        if config.use_atlas:
            content += f"- **Migrations**: Atlas\n"
    
    if config.package_manager:
        content += f"- **Package Manager**: {config.package_manager}\n"
    
    if config.use_github_actions:
        content += f"- **CI/CD**: GitHub Actions\n"
    
    content += f"""
## Development Setup

### Prerequisites
- AI API keys (choose one or more):
  - Anthropic Claude API key
  - OpenAI API key
  - Google Gemini API key
"""
    
    if config.frontend:
        content += f"- Node.js 18+ and {config.package_manager or 'npm'}\n"
    
    if config.backend == "python":
        content += f"- Python 3.11+\n"
    
    if config.database:
        content += f"- Docker (for {config.database.title()} database)\n"
    
    content += f"""
### Environment Variables Setup
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:
   - Add your AI API keys
   - Configure database connection (if using database)
   - Set environment-specific variables

"""
    
    if config.database:
        content += f"""### Database Setup
Start the {config.database.title()} database using Docker:
```bash
docker-compose up -d
```

The database will be available at:
- Host: localhost
- Port: {get_database_port(config.database)}
- Database: {config.project_name.replace('-', '_')}

"""
    
    content += f"""### Dependency Installation

"""
    
    if config.frontend:
        content += f"""**Frontend Dependencies:**
```bash
cd frontend
{config.package_manager or 'npm'} install
```

"""
    
    if config.backend == "python":
        content += f"""**Backend Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

"""
    
    content += f"""## Development Commands

### Start Development Servers

"""
    
    if config.frontend:
        build_tool_cmd = "npm run dev"
        if config.build_tool == 'vite':
            build_tool_cmd = f"{config.package_manager or 'npm'} run dev"
        elif config.build_tool == 'webpack':
            build_tool_cmd = f"{config.package_manager or 'npm'} run dev"
        elif config.build_tool == 'babel':
            build_tool_cmd = f"{config.package_manager or 'npm'} run dev"
        
        content += f"""**Frontend Development Server:**
```bash
cd frontend
{build_tool_cmd}
```
- URL: http://localhost:3000
- Hot reload enabled
- Build tool: {config.build_tool.title() if config.build_tool else 'Default'}

"""
    
    if config.backend == "python":
        content += f"""**Backend Development Server:**
```bash
cd backend
uvicorn app.main:app --reload
```
- URL: http://localhost:8000
- Auto-reload enabled
- API documentation: http://localhost:8000/docs

"""
    
    content += f"""### Testing

"""
    
    if config.frontend:
        content += f"""**Frontend Tests:**
```bash
cd frontend
{config.package_manager or 'npm'} test
```

"""
    
    if config.backend == "python":
        content += f"""**Backend Tests:**
```bash
cd backend
pytest tests/
```

"""
    
    content += f"""### Build and Deployment

"""
    
    if config.frontend:
        content += f"""**Frontend Production Build:**
```bash
cd frontend
{config.package_manager or 'npm'} run build
```
- Output directory: `frontend/dist/`
- Optimized for production

"""
    
    if config.backend == "python":
        content += f"""**Backend Production:**
```bash
cd backend
# Using Docker
docker build -t {config.project_name}-backend .
docker run -p 8000:8000 {config.project_name}-backend

# Or directly with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

"""
    
    content += f"""## Project Structure

```
{config.project_name}/
├── README.md                    # This file
├── CLAUDE.md                    # AI development guide
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
"""
    
    if config.frontend:
        content += f"""├── frontend/                    # Frontend application
│   ├── src/                     # Source code
│   │   ├── main.{get_frontend_extension(config.frontend)}           # Application entry point
│   │   └── App.{get_frontend_extension(config.frontend)}            # Main component
│   ├── public/                  # Static assets
│   ├── package.json             # Node.js dependencies
"""
        if config.build_tool:
            config_file = get_build_tool_config_file(config.build_tool)
            content += f"""│   ├── {config_file}          # Build tool configuration
"""
        content += f"""│   └── CLAUDE.md               # Frontend development guide
"""
    
    if config.backend:
        content += f"""├── backend/                     # Backend API
│   ├── app/                     # Application code
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── api/                 # API routes
│   │   ├── domain/              # Domain models
│   │   ├── services/            # Business logic
│   │   └── repositories/        # Data access layer
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Container configuration
│   └── CLAUDE.md               # Backend development guide
"""
    
    if config.database:
        content += f"""├── migrations/                  # Database migrations
│   └── CLAUDE.md               # Database documentation
├── docker-compose.yml           # Database services
"""
    
    if config.use_github_actions:
        content += f"""├── .github/                     # GitHub configuration
│   ├── workflows/               # CI/CD workflows
│   │   └── ci.yml              # Continuous integration
│   └── CLAUDE.md               # GitHub Actions documentation
"""
    
    content += f"""└── requirements.txt             # Root Python dependencies (if any)
```

## Contributing Guidelines

1. Follow the existing code style and patterns
2. Write tests for new features
3. Update documentation as needed
4. Use meaningful commit messages
5. Create pull requests for all changes

## License and Links

This project was generated with [create-claude-app](https://github.com/swhsiang/create-claude-app), a tool for creating projects optimized for AI-assisted development.

## Documentation

- `CLAUDE.md` - Comprehensive development guide and AI collaboration tips
- `.env.example` - Environment variables template and configuration guide
- Component-specific CLAUDE.md files - Detailed guides for each part of the application

## Support

For questions and support:
1. Check the comprehensive documentation in `CLAUDE.md`
2. Review component-specific documentation
3. Check the [create-claude-app repository](https://github.com/swhsiang/create-claude-app) for updates
"""
    
    return content


def get_frontend_extension(frontend: str) -> str:
    """Get file extension for frontend framework."""
    extensions = {
        'react': 'tsx',
        'vue': 'vue',
        'angular': 'ts'
    }
    return extensions.get(frontend, 'js')


def get_build_tool_config_file(build_tool: str) -> str:
    """Get configuration file name for build tool."""
    config_files = {
        'vite': 'vite.config.ts',
        'webpack': 'webpack.config.js',
        'babel': 'babel.config.js'
    }
    return config_files.get(build_tool, 'package.json')


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
    
    # Generate entry point files
    entry_point_files = generate_frontend_entry_points(project_path, config)
    files_created.extend(entry_point_files)
    
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
    
    # Generate entry point files
    backend_entry_files = generate_backend_entry_points(project_path, config)
    files_created.extend(backend_entry_files)
    
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


def generate_github_actions_files(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate GitHub Actions workflow files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    
    # Create .github/workflows directory
    workflows_path = project_path / '.github' / 'workflows'
    workflows_path.mkdir(parents=True, exist_ok=True)
    
    # Generate CI workflow
    ci_workflow_content = generate_ci_workflow(config)
    ci_workflow_path = workflows_path / 'ci.yml'
    write_file_safe(str(ci_workflow_path), ci_workflow_content)
    files_created.append(str(ci_workflow_path))
    
    # Generate GitHub Actions CLAUDE.md
    github_claude_md = generate_github_actions_claude_md(config)
    claude_md_path = project_path / '.github' / 'CLAUDE.md'
    write_file_safe(str(claude_md_path), github_claude_md)
    files_created.append(str(claude_md_path))
    
    return files_created


def generate_ci_workflow(config: ProjectConfiguration) -> str:
    """Generate CI workflow content.
    
    Args:
        config: Project configuration
        
    Returns:
        CI workflow YAML content
    """
    content = f"""name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
"""
    
    if config.frontend:
        content += f"""  frontend:
    name: Frontend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: '{config.package_manager or "npm"}'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: {config.package_manager or "npm"} install
    
    - name: Run tests
      run: {config.package_manager or "npm"} test
    
    - name: Build project
      run: {config.package_manager or "npm"} run build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: frontend-build
        path: frontend/dist/

"""
    
    if config.backend == "python":
        content += f"""  backend:
    name: Backend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: backend

"""
    
    if config.database:
        content += f"""  database:
    name: Database Tests
    runs-on: ubuntu-latest
    
    services:
      {config.database}:
        image: {get_database_image(config.database)}
        env:
          {get_database_env_vars(config)}
        ports:
          - {get_database_port(config.database)}:{get_database_port(config.database)}
        options: --health-cmd="{get_database_health_cmd(config.database)}" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Test database connection
      run: |
        {get_database_test_cmd(config.database)}

"""
    
    return content


def generate_github_actions_claude_md(config: ProjectConfiguration) -> str:
    """Generate CLAUDE.md for GitHub Actions directory."""
    content = f"""# GitHub Actions CI/CD

## Overview
Automated workflows for {config.project_name} using GitHub Actions.

## Workflows

### CI Workflow (ci.yml)
Runs on every push and pull request to main branch.

**Jobs:**
"""
    
    if config.frontend:
        content += f"""- **Frontend Tests**: Node.js {config.package_manager or "npm"} test and build
"""
    
    if config.backend == "python":
        content += f"""- **Backend Tests**: Python pytest with coverage reporting
"""
    
    if config.database:
        content += f"""- **Database Tests**: {config.database.title()} connection and health checks
"""
    
    content += f"""
## Configuration

### Secrets Required
- `ANTHROPIC_API_KEY`: Claude API key for AI features
- `CODECOV_TOKEN`: Coverage reporting (optional)

### Environment Variables
- See `.env.example` for required variables

## Deployment
- Builds are automatically created on successful tests
- Artifacts are uploaded for each successful build
- Coverage reports are sent to Codecov

## Customization
- Add deployment jobs to `ci.yml` for your hosting platform
- Configure additional test environments as needed
- Add security scanning jobs for production use
"""
    
    return content


def get_database_image(database: str) -> str:
    """Get Docker image for database."""
    images = {
        'postgresql': 'postgres:15',
        'mysql': 'mysql:8',
        'sqlite': 'alpine:latest'  # SQLite doesn't need a service
    }
    return images.get(database, 'postgres:15')


def get_database_env_vars(config: ProjectConfiguration) -> str:
    """Get environment variables for database service."""
    if config.database == 'postgresql':
        return f"""POSTGRES_DB: {config.project_name.replace('-', '_')}
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres"""
    elif config.database == 'mysql':
        return f"""MYSQL_DATABASE: {config.project_name.replace('-', '_')}
          MYSQL_USER: mysql
          MYSQL_PASSWORD: mysql
          MYSQL_ROOT_PASSWORD: root"""
    return ""


def get_database_port(database: str) -> str:
    """Get port for database service."""
    ports = {
        'postgresql': '5432',
        'mysql': '3306',
        'sqlite': '3306'  # Not used for SQLite
    }
    return ports.get(database, '5432')


def get_database_health_cmd(database: str) -> str:
    """Get health check command for database."""
    commands = {
        'postgresql': 'pg_isready -U postgres',
        'mysql': 'mysqladmin ping -h localhost',
        'sqlite': 'echo "OK"'
    }
    return commands.get(database, 'pg_isready -U postgres')


def get_database_test_cmd(database: str) -> str:
    """Get test command for database connection."""
    commands = {
        'postgresql': 'psql -h localhost -U postgres -c "SELECT 1"',
        'mysql': 'mysql -h localhost -u mysql -pmysql -e "SELECT 1"',
        'sqlite': 'echo "SQLite test passed"'
    }
    return commands.get(database, 'psql -h localhost -U postgres -c "SELECT 1"')


def generate_frontend_entry_points(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate frontend entry point files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    
    if not config.frontend:
        return files_created
    
    frontend_path = project_path / 'frontend'
    
    # Create src directory
    src_path = frontend_path / 'src'
    src_path.mkdir(parents=True, exist_ok=True)
    
    # Create public directory
    public_path = frontend_path / 'public'
    public_path.mkdir(parents=True, exist_ok=True)
    
    if config.frontend == 'react':
        # Generate index.html
        index_html = generate_react_index_html(config)
        index_path = public_path / 'index.html'
        write_file_safe(str(index_path), index_html)
        files_created.append(str(index_path))
        
        # Generate main.tsx
        main_tsx = generate_react_main_tsx(config)
        main_path = src_path / 'main.tsx'
        write_file_safe(str(main_path), main_tsx)
        files_created.append(str(main_path))
        
        # Generate App.tsx
        app_tsx = generate_react_app_tsx(config)
        app_path = src_path / 'App.tsx'
        write_file_safe(str(app_path), app_tsx)
        files_created.append(str(app_path))
        
        # Generate build tool config
        if config.build_tool == 'vite':
            vite_config = generate_vite_config(config)
            vite_path = frontend_path / 'vite.config.ts'
            write_file_safe(str(vite_path), vite_config)
            files_created.append(str(vite_path))
        elif config.build_tool == 'webpack':
            webpack_config = generate_webpack_config(config)
            webpack_path = frontend_path / 'webpack.config.js'
            write_file_safe(str(webpack_path), webpack_config)
            files_created.append(str(webpack_path))
    
    elif config.frontend == 'vue':
        # Generate Vue entry points
        index_html = generate_vue_index_html(config)
        index_path = public_path / 'index.html'
        write_file_safe(str(index_path), index_html)
        files_created.append(str(index_path))
        
        main_ts = generate_vue_main_ts(config)
        main_path = src_path / 'main.ts'
        write_file_safe(str(main_path), main_ts)
        files_created.append(str(main_path))
        
        app_vue = generate_vue_app_vue(config)
        app_path = src_path / 'App.vue'
        write_file_safe(str(app_path), app_vue)
        files_created.append(str(app_path))
        
        # Generate build tool config
        if config.build_tool == 'vite':
            vite_config = generate_vite_config_vue(config)
            vite_path = frontend_path / 'vite.config.ts'
            write_file_safe(str(vite_path), vite_config)
            files_created.append(str(vite_path))
        elif config.build_tool == 'webpack':
            webpack_config = generate_webpack_config_vue(config)
            webpack_path = frontend_path / 'webpack.config.js'
            write_file_safe(str(webpack_path), webpack_config)
            files_created.append(str(webpack_path))
    
    elif config.frontend == 'angular':
        # Generate Angular entry points
        main_ts = generate_angular_main_ts(config)
        main_path = src_path / 'main.ts'
        write_file_safe(str(main_path), main_ts)
        files_created.append(str(main_path))
        
        app_component = generate_angular_app_component(config)
        app_path = src_path / 'app' / 'app.component.ts'
        app_path.parent.mkdir(parents=True, exist_ok=True)
        write_file_safe(str(app_path), app_component)
        files_created.append(str(app_path))
    
    return files_created


def generate_backend_entry_points(project_path: Path, config: ProjectConfiguration) -> List[str]:
    """Generate backend entry point files.
    
    Args:
        project_path: Path to the project root
        config: Project configuration
        
    Returns:
        List of created file paths
    """
    files_created = []
    
    if not config.backend:
        return files_created
    
    backend_path = project_path / 'backend'
    
    if config.backend == 'python':
        # Create app directory structure
        app_path = backend_path / 'app'
        app_path.mkdir(parents=True, exist_ok=True)
        
        # Generate main.py
        main_py = generate_python_main_py(config)
        main_path = app_path / 'main.py'
        write_file_safe(str(main_path), main_py)
        files_created.append(str(main_path))
        
        # Generate __init__.py
        init_py = generate_python_init_py(config)
        init_path = app_path / '__init__.py'
        write_file_safe(str(init_path), init_py)
        files_created.append(str(init_path))
        
        # Create directory structure
        for subdir in ['api', 'domain', 'services', 'repositories', 'infrastructure']:
            subdir_path = app_path / subdir
            subdir_path.mkdir(exist_ok=True)
            init_path = subdir_path / '__init__.py'
            write_file_safe(str(init_path), "")
            files_created.append(str(init_path))
        
        # Generate Dockerfile
        dockerfile = generate_python_dockerfile(config)
        docker_path = backend_path / 'Dockerfile'
        write_file_safe(str(docker_path), dockerfile)
        files_created.append(str(docker_path))
    
    return files_created


def generate_react_index_html(config: ProjectConfiguration) -> str:
    """Generate index.html for React."""
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{config.project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""


def generate_react_main_tsx(config: ProjectConfiguration) -> str:
    """Generate main.tsx for React."""
    return f"""import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
{f"import './index.css'" if config.ui_framework == 'tailwind' else ""}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""


def generate_react_app_tsx(config: ProjectConfiguration) -> str:
    """Generate App.tsx for React."""
    return f"""import React from 'react'
{f"import './App.css'" if config.ui_framework != 'tailwind' else ""}

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to {config.project_name}</h1>
        <p>
          A modern React application built with{' '}
          {config.ui_framework == 'tailwind' and 'Tailwind CSS' or 
           config.ui_framework == 'shadcn' and 'shadcn/ui' or 'React'}
        </p>
      </header>
    </div>
  )
}}

export default App"""


def generate_vite_config(config: ProjectConfiguration) -> str:
    """Generate vite.config.ts for React."""
    return f"""import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({{
  plugins: [react()],
  server: {{
    port: 3000,
    open: true,
  }},
  build: {{
    outDir: 'dist',
    sourcemap: true,
  }},
}})"""


def generate_vite_config_vue(config: ProjectConfiguration) -> str:
    """Generate vite.config.ts for Vue."""
    return f"""import {{ defineConfig }} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({{
  plugins: [vue()],
  server: {{
    port: 3000,
    open: true,
  }},
  build: {{
    outDir: 'dist',
    sourcemap: true,
  }},
}}))"""


def generate_webpack_config(config: ProjectConfiguration) -> str:
    """Generate webpack.config.js for React."""
    return f"""const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {{
  mode: 'development',
  entry: './src/main.tsx',
  output: {{
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  }},
  resolve: {{
    extensions: ['.tsx', '.ts', '.js'],
  }},
  module: {{
    rules: [
      {{
        test: /\\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      }},
      {{
        test: /\\.css$/,
        use: ['style-loader', 'css-loader'],
      }},
    ],
  }},
  plugins: [
    new HtmlWebpackPlugin({{
      template: './public/index.html',
    }}),
  ],
  devServer: {{
    static: './dist',
    hot: true,
    port: 3000,
  }},
}};"""


def generate_webpack_config_vue(config: ProjectConfiguration) -> str:
    """Generate webpack.config.js for Vue."""
    return f"""const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {{ VueLoaderPlugin }} = require('vue-loader');

module.exports = {{
  mode: 'development',
  entry: './src/main.ts',
  output: {{
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  }},
  resolve: {{
    extensions: ['.vue', '.ts', '.js'],
  }},
  module: {{
    rules: [
      {{
        test: /\\.vue$/,
        loader: 'vue-loader',
      }},
      {{
        test: /\\.ts$/,
        loader: 'ts-loader',
        options: {{
          appendTsSuffixTo: [/\\.vue$/],
        }},
        exclude: /node_modules/,
      }},
      {{
        test: /\\.css$/,
        use: ['style-loader', 'css-loader'],
      }},
    ],
  }},
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({{
      template: './public/index.html',
    }}),
  ],
  devServer: {{
    static: './dist',
    hot: true,
    port: 3000,
  }},
}};"""


def generate_vue_index_html(config: ProjectConfiguration) -> str:
    """Generate index.html for Vue."""
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.project_name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>"""


def generate_vue_main_ts(config: ProjectConfiguration) -> str:
    """Generate main.ts for Vue."""
    return f"""import {{ createApp }} from 'vue'
import App from './App.vue'
{f"import './style.css'" if config.ui_framework == 'tailwind' else ""}

createApp(App).mount('#app')"""


def generate_vue_app_vue(config: ProjectConfiguration) -> str:
    """Generate App.vue for Vue."""
    return f"""<template>
  <div class="app">
    <header class="app-header">
      <h1>Welcome to {config.project_name}</h1>
      <p>
        A modern Vue application built with
        {config.ui_framework == 'tailwind' and 'Tailwind CSS' or 'Vue 3'}
      </p>
    </header>
  </div>
</template>

<script setup lang="ts">
// Vue 3 Composition API
</script>

<style scoped>
.app {{
  text-align: center;
  padding: 2rem;
}}

.app-header {{
  background-color: #f0f0f0;
  padding: 2rem;
  border-radius: 8px;
}}
</style>"""


def generate_angular_main_ts(config: ProjectConfiguration) -> str:
    """Generate main.ts for Angular."""
    return f"""import {{ platformBrowserDynamic }} from '@angular/platform-browser-dynamic';
import {{ AppModule }} from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));"""


def generate_angular_app_component(config: ProjectConfiguration) -> str:
    """Generate app.component.ts for Angular."""
    return f"""import {{ Component }} from '@angular/core';

@Component({{
  selector: 'app-root',
  template: `
    <div class="app">
      <header class="app-header">
        <h1>Welcome to {config.project_name}</h1>
        <p>
          A modern Angular application
        </p>
      </header>
    </div>
  `,
  styles: [`
    .app {{
      text-align: center;
      padding: 2rem;
    }}
    .app-header {{
      background-color: #f0f0f0;
      padding: 2rem;
      border-radius: 8px;
    }}
  `]
}})
export class AppComponent {{
  title = '{config.project_name}';
}}"""


def generate_python_main_py(config: ProjectConfiguration) -> str:
    """Generate main.py for Python FastAPI."""
    return f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="{config.project_name}",
    description="A modern FastAPI application for {config.project_name}",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {{"message": "Welcome to {config.project_name} API"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)"""


def generate_python_init_py(config: ProjectConfiguration) -> str:
    """Generate __init__.py for Python app."""
    return f"""\"\"\"
{config.project_name} - A modern FastAPI application
\"\"\"

__version__ = "1.0.0"
"""


def generate_python_dockerfile(config: ProjectConfiguration) -> str:
    """Generate Dockerfile for Python backend."""
    return f"""FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]"""