# Product Requirements Document: create-claude-app

## Overview
`create-claude-app` is an interactive Python command-line tool that scaffolds new projects optimized for Claude Code development. It creates structured project templates with comprehensive CLAUDE.md files to enable developers to quickly start new projects with Claude Code.

## Goals
- Enable developers to quickly bootstrap new projects for Claude Code
- Provide clean architecture templates following industry best practices
- Generate comprehensive CLAUDE.md files for effective AI-assisted development
- Support multiple technology stacks (Frontend, Backend, Database)
- Distribute as a PyPI package for easy installation

## Installation & Usage

### Basic Installation
```bash
# Install via pip
pip install create-claude-app

# Install via homebrew (future)
brew install create-claude-app
```

### Usage Options

#### Interactive Mode (Default)
```bash
# Interactive prompts for all options
create-claude-app my-new-project
```

#### CLI Arguments Mode (Non-Interactive)
```bash
# Specify all options via command line flags
create-claude-app my-project --frontend react --backend python --database mysql

# Mix of flags and defaults
create-claude-app my-project --frontend vue --ui tailwind

# Use short flags
create-claude-app my-project -f react -B python -d postgresql
```

### Available CLI Arguments

| Flag | Short | Options | Default | Description |
|------|-------|---------|---------|-------------|
| `--frontend` | `-f` | `react`, `vue`, `angular`, `none` | `none` | Frontend framework |
| `--ui` | `-u` | `tailwind`, `shadcn`, `none` | `none` | UI framework |
| `--build-tool` | `-b` | `vite`, `webpack`, `babel` | `vite` | Frontend build tool |
| `--backend` | `-B` | `python`, `nodejs`, `golang`, `none` | `none` | Backend language |
| `--database` | `-d` | `mysql`, `postgresql`, `sqlite`, `none` | `none` | Database system |
| `--package-manager` | `-p` | `npm`, `yarn` | `npm` | Package manager |
| `--atlas` | `-a` | flag | `false` | Enable Atlas migrations |
| `--github-actions` | `-g` | flag | `false` | Enable GitHub Actions |
| `--mcp` | `-m` | flag | `true` | Enable MCP integration |

### CLI Argument Behavior

**Validation**: 
- Invalid combinations (e.g., `--frontend angular --ui shadcn`) will immediately error with clear messages
- Unknown values will show available options and exit

**Mixed Mode**: 
- CLI args override interactive prompts
- Missing options use defaults (no prompting)
- Maintains backward compatibility

**Help Documentation**:
```bash
create-claude-app --help
# Shows all available options with valid values
```

### Error Examples
```bash
# Invalid combination
$ create-claude-app test --frontend angular --ui shadcn
Error: Incompatible combination detected.
Angular frontend is not compatible with shadcn/ui framework.
Valid UI options for Angular: tailwind, none

# Invalid value
$ create-claude-app test --frontend react-native
Error: Invalid frontend option 'react-native'.
Valid options: react, vue, angular, none
```

## Interactive Component Selection

The tool will prompt users to select components with **single choice per category** plus **Skip option**:

### Frontend Framework Options
- ( ) React
- ( ) Vue  
- ( ) Angular
- ( ) Skip

### UI Framework Options (if frontend selected)
- ( ) Tailwind CSS
- ( ) shadcn/ui
- ( ) None/Skip

**Note**: Tool will warn users about incompatible combinations (e.g., Angular + shadcn/ui)

### Backend Options
- ( ) Python
- ( ) Node.js
- ( ) Golang
- ( ) Skip

### Database Options
- ( ) MySQL
- ( ) PostgreSQL
- ( ) SQLite
- ( ) Skip

### Database Migration Tool
- Prompt: "Would you like to include Atlas migration tool? (Y/n)"
- Default: Yes
- Provides Atlas installation instructions and sample configuration in generated documentation and CLAUDE.md files

### Package Manager Options (if frontend selected)
- ( ) npm
- ( ) yarn

### Frontend Build Tool Options (if frontend selected)
- ( ) Vite (recommended)
- ( ) Webpack
- ( ) Babel + Webpack

### GitHub Actions CI/CD
- Prompt: "Would you like to include GitHub Actions workflows? (Y/n)"
- Default: Yes
- Generates CI/CD workflow files based on selected technology stack
- Provides comprehensive workflow templates for testing, building, and deployment

### Model Context Protocol (MCP) Integration
- Prompt: "Would you like to include MCP (Model Context Protocol) configuration? (Y/n)"
- Default: Yes (recommended)
- **Conditional Generation**: `.mcp.json` file is only generated if user selects "Yes"
- If disabled: No MCP-related files or documentation are generated
- Provides project-specific context and tooling configuration for Claude Code and other AI assistants
- Enhances AI-assisted development workflow with project-aware context

## Project Structure

### Root Level Structure
```
/my-project-root/
├── README.md
├── CLAUDE.md              # Main project documentation
├── .env.example           # Environment variables template
├── .mcp.json              # Model Context Protocol configuration (only if MCP enabled)
├── .gitignore
├── package.json           # (optional) For root-level npm scripts, workspaces
├── requirements.txt       # Project Python dependencies
├── infra/                 # Docker infrastructure (mandatory)
│   └── docker/
│       ├── frontend/
│       ├── backend/
│       ├── db/
│       └── docker-compose*.yml
├── .github/               # (if GitHub Actions selected)
│   └── workflows/         # CI/CD workflow files
├── frontend/              # (if frontend selected)
├── backend/               # (if backend selected)
└── migrations/            # (if database + Atlas selected)
```

### Frontend Structure (React Example)
```
frontend/
├── CLAUDE.md              # Frontend-specific documentation
├── package.json
├── tailwind.config.js     # (if Tailwind CSS selected)
├── components.json        # (if shadcn/ui selected)
├── public/
├── src/
│   ├── components/
│   │   └── ui/            # (if shadcn/ui selected)
│   ├── pages/
│   ├── hooks/
│   ├── lib/               # (if shadcn/ui selected)
│   ├── App.tsx
│   └── index.tsx
└── tsconfig.json
```

### Backend Structure (Python Example - DDD/Service Layer)
```
backend/
├── CLAUDE.md              # Backend-specific documentation
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI/Flask entry point
│   ├── api/               # API routes/controllers
│   ├── domain/            # Domain models and business logic
│   ├── services/          # Service layer
│   ├── repositories/      # Data access layer
│   └── infrastructure/    # External services, database
├── requirements.txt
└── tests/
```

### Database Structure
```
migrations/
├── CLAUDE.md              # Database migration documentation
├── atlas.hcl              # Atlas configuration
└── migrations/            # Migration files (if Atlas selected)
```

### Infrastructure Structure
```
infra/
└── docker/
    ├── frontend/
    │   └── Dockerfile         # Build-tool specific (Vite/Webpack/Babel)
    ├── backend/
    │   └── Dockerfile         # Language-specific (Python/Node.js/Golang)
    ├── db/
    │   └── Dockerfile         # Standard database image configuration
    ├── docker-compose.yml     # Main compose file
    ├── docker-compose.dev.yml # Development environment
    ├── docker-compose.staging.yml # Staging environment
    └── docker-compose.prod.yml # Production environment
```

### GitHub Actions Structure
```
.github/
├── workflows/
│   ├── ci.yml             # Continuous Integration workflow
│   ├── cd.yml             # Continuous Deployment workflow (optional)
│   └── test.yml           # Test workflow (if separate from CI)
└── CLAUDE.md              # GitHub Actions documentation
```

## CLAUDE.md Content Structure

### Root CLAUDE.md
- **Project Description Template**
- **Technology Stack Overview**
- **Environment Setup Instructions**
  - .env file configuration
  - Required environment variables
  - AI API keys setup (GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY)
- **Development Commands**
  - Setup instructions
  - Development server commands
  - Build commands
  - Test commands
- **CI/CD Pipeline Documentation** (if GitHub Actions selected)
  - Workflow overview
  - Deployment process
  - Environment-specific configurations
  - Secrets management
- **Google Coding Style Guide Reference**
- **Project Architecture Overview**
- **Contributing Guidelines**

### Component-Specific Documentation
Each subfolder with code will have its own CLAUDE.md containing:
- **Component Overview**
- **Local Development Commands**
- **Architecture Patterns**
- **Coding Standards**
- **Testing Guidelines**
- **Common Tasks**

### README.md Content Structure
**Root README.md:**
- **Quick Start Guide** with immediate setup steps
- **Technology Stack Overview** with chosen frameworks
- **Development Setup Instructions**
  - Prerequisites installation
  - Environment variables setup
  - Database setup (if applicable)
  - Dependency installation commands
- **Development Commands**
  - Frontend: Start development server with chosen build tool (Vite/Webpack/Babel)
  - Backend: Start server with framework-specific commands
  - Database: Migration and seeding commands
  - Testing: Unit and integration test commands
- **Docker Commands**
  - Start all services: `docker-compose -f infra/docker/docker-compose.yml up`
  - Development environment: `docker-compose -f infra/docker/docker-compose.dev.yml up`
  - Stop services: `docker-compose -f infra/docker/docker-compose.yml down`
  - Rebuild containers: `docker-compose -f infra/docker/docker-compose.yml up --build`
- **MCP Integration** (if MCP selected)
  - Context7 MCP server configuration in `.mcp.json`
  - Claude Desktop integration setup instructions
  - Context7 installation and usage guidelines
  - Enhanced AI-assisted development workflow with intelligent context
- **Build and Deployment**
  - Production build commands
  - Environment-specific configurations
  - Deployment instructions
- **Project Structure** overview
- **Contributing Guidelines**
- **License and Links**

## Environment Variables Configuration

### .env.example Template
```env
# AI API Keys (choose one or multiple)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration (if database selected)
DATABASE_URL=your_database_url_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# Application Settings
ENV=development
DEBUG=true
PORT=8000
```

### Root CLAUDE.md Environment Instructions
- Copy .env.example to .env
- Configure required API keys for AI services
- Database connection strings
- Development vs production settings
- Security best practices for environment variables

## Technology Stack Templates

### Frontend Templates
- **React**: TypeScript, modern hooks, component structure with chosen build tool
  - Vite: Fast HMR, optimized builds, modern ESM
  - Webpack: Traditional bundling with extensive configuration
  - Babel + Webpack: Custom transpilation with webpack bundling
- **Vue**: Vue 3 with Composition API, TypeScript, Vite setup
- **Angular**: Latest Angular with TypeScript, Angular CLI

### UI Framework Integration
- **Tailwind CSS**: Complete setup with configuration files, utility classes
- **shadcn/ui**: Component library setup with TypeScript, theming system

### Backend Templates
- **Python**: FastAPI with DDD/Service Layer architecture
  - Entry point: `app/main.py`
  - Development: `uvicorn app.main:app --reload`
  - Production: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Node.js**: Express.js with TypeScript, layered architecture
  - Entry point: `src/server.ts` or `src/app.js`
  - Development: `npm run dev` (nodemon) or `yarn dev`
  - Production: `npm start` or `yarn start`
- **Golang**: Gin framework with clean architecture
  - Entry point: `main.go`
  - Development: `go run main.go` or `air` for hot reload
  - Production: `go build && ./app-name`

### Database Integration
- **Docker Infrastructure**: Service definitions in infra/docker/docker-compose.yml
- **Atlas Migration Tool**: 
  - Installation instructions in generated documentation and CLAUDE.md files
  - Sample configuration files
  - Basic migration templates
  - Database connection configuration files (not implementation)

## File Generation Strategy

### Basic Starter Files
- Generate minimal, functional starter files
- Include basic configuration (package.json, requirements.txt, etc.)
- Provide working entry points with clear development instructions
- Include essential folder structure
- Create .env.example with default fields
- Use version ranges for dependencies (not exact pins)
- Generate README.md with comprehensive development setup instructions

### Entry Points and Development Instructions
**Frontend Entry Points:**
- React: `src/main.tsx` or `src/index.tsx` with chosen build tool
- Vue: `src/main.ts` with Vue 3 Composition API
- Angular: `src/main.ts` with Angular CLI structure

**Backend Entry Points:**
- Python: `app/main.py` with FastAPI/Flask application
- Node.js: `src/server.ts` or `src/app.js` with Express setup
- Golang: `main.go` with Gin/Echo framework setup

**README.md Development Instructions:**
- Step-by-step setup process
- Environment variable configuration
- Database setup commands (if applicable)
- Frontend development server commands with chosen build tool
- Backend development server commands with framework-specific instructions
- Testing commands for both frontend and backend
- Build and deployment instructions

### UI Framework Setup
- **Tailwind CSS**: Install dependencies, create config files, add sample components
- **shadcn/ui**: Install CLI, setup components.json, add sample UI components

### Template Quality
- Follow Google Coding Style Guide
- Include proper TypeScript/type annotations
- Provide working examples, not just empty files
- Include basic error handling and logging
- Testing frameworks mentioned in CLAUDE.md files only

### Template Storage
- Templates stored as separate files in `templates/` directory
- Organized by component type (frontend, backend, database, ui)

## Package Structure

### PyPI Package Layout
```
create-claude-app/
├── pyproject.toml         # Package configuration
├── README.md
├── LICENSE
├── src/
│   └── create_claude_app/
│       ├── __init__.py
│       ├── cli.py         # Main CLI interface
│       ├── templates/     # Template files
│       │   ├── frontend/
│       │   ├── backend/
│       │   ├── database/
│       │   └── ui/        # UI framework templates
│       └── generators/    # Code generators
├── tests/
└── docs/
```

### Entry Point
- Command: `create-claude-app`
- Entry point: `create_claude_app.cli:main`

## Infrastructure Configuration

### Docker Infrastructure (Mandatory Feature)
The tool automatically generates Docker infrastructure for all projects, creating a standardized development and deployment environment.

#### Infrastructure Structure
```
/my-project-root/
├── infra/
│   └── docker/
│       ├── frontend/
│       │   └── Dockerfile        # Build-tool specific Dockerfile
│       ├── backend/
│       │   └── Dockerfile        # Language-specific Dockerfile
│       ├── db/
│       │   └── Dockerfile        # Standard database image configuration
│       ├── docker-compose.yml    # Main compose file
│       ├── docker-compose.dev.yml     # Development environment
│       ├── docker-compose.staging.yml # Staging environment
│       └── docker-compose.prod.yml    # Production environment
```

#### Frontend Dockerfiles
- **Build-tool specific**: Different Dockerfile templates for Vite, Webpack, and Babel + Webpack
- **Single-stage builds**: Simplified containerization without multi-stage optimization
- **Development focused**: Optimized for development workflow with hot reloading support

#### Backend Dockerfiles
- **Language-specific**: Separate Dockerfile templates for Python, Node.js, and Golang
- **Framework-agnostic**: Focus on language runtime rather than specific frameworks
- **Optimization documentation**: Include brief optimization notes in backend README.md and CLAUDE.md

#### Database Dockerfiles
- **Standard images**: Use official database images (mysql:8.0, postgres:15, sqlite)
- **Configuration-based**: Environment-specific configuration through compose files
- **Volume management**: Persistent data storage configuration

#### Docker Compose Files
- **Base compose**: `docker-compose.yml` with core service definitions
- **Environment-specific**: Development, staging, and production variants
- **Service orchestration**: Frontend, backend, and database service coordination
- **Network configuration**: Internal service communication setup

#### Generated Documentation
- **Docker optimization sections**: Brief optimization notes added to backend README.md and CLAUDE.md
- **Development workflow**: Instructions for using Docker in development
- **Environment management**: Guide for switching between dev/staging/prod environments

## Model Context Protocol (MCP) Configuration

### MCP Integration (Recommended Feature)
The tool optionally generates Model Context Protocol configuration to enhance AI-assisted development workflows with project-aware context and tooling.

#### MCP Configuration Structure
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7"
      ],
      "env": {}
    }
  }
}
```

**Context7 MCP Server Features:**
- **Intelligent Context Management**: Automatically provides relevant project context to AI assistants
- **Smart File Discovery**: Identifies and surfaces important project files and documentation
- **Project Understanding**: Analyzes project structure and provides contextual information
- **Technology Stack Awareness**: Understands the project's technology choices and conventions
- **Codebase Navigation**: Helps AI assistants navigate and understand the project structure

#### MCP Features
- **Intelligent Context**: Context7 automatically provides relevant project information to AI assistants
- **Smart Project Analysis**: Understands project structure, technology stack, and conventions
- **Enhanced AI Assistance**: Enables AI assistants to provide more accurate and contextual help
- **Claude Desktop Integration**: Seamless integration with Claude Desktop and other MCP-compatible clients
- **Zero Configuration**: Works out-of-the-box with minimal setup required

#### Generated MCP Documentation
- **Context7 setup instructions**: Added to main CLAUDE.md file with Claude Desktop configuration
- **Installation guide**: Step-by-step setup for Context7 MCP server
- **Usage guidelines**: How to leverage Context7 for enhanced AI assistance
- **Development workflow**: Best practices for AI-assisted development with Context7

## Technical Requirements

### Dependencies
- **click**: CLI framework
- **rich**: Beautiful terminal output
- **colorama**: Cross-platform colored terminal text
- **jinja2**: Template engine
- **pathlib**: File system operations

### Python Version Support
- Python 3.8+
- Cross-platform compatibility (Windows, macOS, Linux)

### Error Handling
- Graceful handling of existing directories
- Clear error messages
- Validation of user inputs
- Clean up partially created files on failures
- Direct users to report issues at https://github.com/swhsiang/create-claude-app/issues

## Success Metrics
- Easy project setup (< 2 minutes from command to working project)
- Comprehensive CLAUDE.md files enable effective AI assistance
- Clean, maintainable code architecture
- Positive developer feedback
- Growing adoption via PyPI downloads

## Future Enhancements
- Additional frontend frameworks (Svelte, Solid.js)
- More UI frameworks (Chakra UI, Material-UI)
- More backend options (Rust, Java, C#)
- Database ORM integration
- CI/CD pipeline templates
- Docker deployment templates
- Testing framework integration
- IDE configuration files