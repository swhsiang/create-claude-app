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
```bash
# Install via pip
pip install create-claude-app

# Install via homebrew (future)
brew install create-claude-app

# Usage
create-claude-app my-new-project
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

### Package Manager Options (if Node.js selected)
- ( ) npm
- ( ) npx  
- ( ) yarn

## Project Structure

### Root Level Structure
```
/my-project-root/
├── README.md
├── CLAUDE.md              # Main project documentation
├── .env.example           # Environment variables template
├── .gitignore
├── package.json           # (optional) For root-level npm scripts, workspaces
├── requirements.txt       # Project Python dependencies
├── docker-compose.yml     # (if database selected)
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
├── Dockerfile
└── tests/
```

### Database Structure
```
migrations/
├── CLAUDE.md              # Database migration documentation
├── atlas.hcl              # Atlas configuration
└── migrations/            # Migration files (if Atlas selected)
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
- **Google Coding Style Guide Reference**
- **Project Architecture Overview**
- **Contributing Guidelines**

### Component-Specific CLAUDE.md Files
Each subfolder with code will have its own CLAUDE.md containing:
- **Component Overview**
- **Local Development Commands**
- **Architecture Patterns**
- **Coding Standards**
- **Testing Guidelines**
- **Common Tasks**

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
- **React**: TypeScript, modern hooks, component structure
- **Vue**: Vue 3 with Composition API, TypeScript
- **Angular**: Latest Angular with TypeScript

### UI Framework Integration
- **Tailwind CSS**: Complete setup with configuration files, utility classes
- **shadcn/ui**: Component library setup with TypeScript, theming system

### Backend Templates
- **Python**: FastAPI with DDD/Service Layer architecture
- **Node.js**: Express.js with TypeScript, layered architecture
- **Golang**: Gin framework with clean architecture

### Database Integration
- **Docker Compose**: Service definitions for selected databases
- **Atlas Migration Tool**: 
  - Installation instructions in generated documentation and CLAUDE.md files
  - Sample configuration files
  - Basic migration templates
  - Database connection configuration files (not implementation)

## File Generation Strategy

### Basic Starter Files
- Generate minimal, functional starter files
- Include basic configuration (package.json, requirements.txt, etc.)
- Provide working entry points (main.py, App.tsx, etc.)
- Include essential folder structure
- Create .env.example with default fields
- Use version ranges for dependencies (not exact pins)

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