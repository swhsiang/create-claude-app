# create-claude-app

Interactive Python CLI tool that scaffolds new projects optimized for Claude Code development. Creates structured project templates with comprehensive CLAUDE.md files to enable developers to quickly start new projects with Claude Code.

## Features

- 🚀 **Quick Project Setup**: Bootstrap new projects in under 2 minutes
- 🎯 **Interactive Selection**: Choose from multiple frontend, backend, and database options
- 💻 **CLI Arguments**: Non-interactive mode with full command-line argument support
- 📋 **Comprehensive Documentation**: Auto-generated CLAUDE.md files for effective AI-assisted development
- 🏗️ **Clean Architecture**: Industry best practices with Domain-Driven Design patterns
- 🔧 **Multiple Tech Stacks**: Support for React, Vue, Angular, Python, Node.js, Golang, and more
- 📦 **Database Integration**: MySQL, PostgreSQL, SQLite with Atlas migration tool support
- 🎨 **UI Framework Support**: Tailwind CSS, shadcn/ui with automatic compatibility checking
- ⚡ **Build Tool Selection**: Vite, Webpack, Babel + Webpack with optimized configurations
- 🔄 **GitHub Actions CI/CD**: Automated workflow generation for testing and deployment
- 📁 **Framework Entry Points**: Production-ready entry files for all supported frameworks
- 📚 **Enhanced README**: Detailed setup, development, and deployment instructions
- 🐳 **Docker Infrastructure**: Complete containerization with multi-stage builds and environment-specific configurations
- 🏗️ **Docker Compose**: Development, staging, and production docker-compose files with optimized configurations
- 🔌 **MCP Integration**: Model Context Protocol support with Context7 for enhanced AI-assisted development

## Installation

```bash
# Install via pip
pip install create-claude-app

# Install via homebrew (coming soon)
brew tap yourusername/create-claude-app
brew install create-claude-app
```

## Usage

### Interactive Mode (Default)

```bash
# Create a new project with interactive prompts
create-claude-app my-new-project

# Follow the interactive prompts to select your tech stack
```

### CLI Arguments Mode (Non-Interactive)

```bash
# Create a project with all options specified via command line
create-claude-app my-project --frontend react --backend python --database mysql

# Mixed mode - some CLI args with defaults for missing options
create-claude-app my-project --frontend vue --ui tailwind

# Use short flags for faster typing
create-claude-app my-project -f react -B python -d postgresql
```

### Available CLI Arguments

| Flag | Short | Options | Default | Description |
|------|-------|---------|---------|-------------|
| `--frontend` | `-f` | `react`, `vue`, `angular`, `none` | `none` | Frontend framework |
| `--backend` | `-B` | `python`, `nodejs`, `golang`, `none` | `none` | Backend language |
| `--database` | `-d` | `mysql`, `postgresql`, `sqlite`, `none` | `none` | Database system |
| `--ui` | `-u` | `tailwind`, `shadcn`, `none` | `none` | UI framework |
| `--build-tool` | `-b` | `vite`, `webpack`, `babel` | `vite` | Frontend build tool |
| `--package-manager` | `-p` | `npm`, `yarn` | `npm` | Package manager |
| `--atlas` | `-a` | flag | `false` | Enable Atlas migrations |
| `--github-actions` | `-g` | flag | `false` | Enable GitHub Actions |
| `--mcp` | `-m` | flag | `true` | Enable MCP integration |

### CLI Examples

```bash
# Full stack application with all features
create-claude-app my-app \
  --frontend react \
  --ui shadcn \
  --build-tool vite \
  --backend python \
  --database postgresql \
  --package-manager yarn \
  --atlas \
  --github-actions

# Minimal project with just frontend
create-claude-app simple-app --frontend vue --ui tailwind

# Backend-only API
create-claude-app api-server --backend python --database mysql --atlas

# Help and version information
create-claude-app --help
create-claude-app --version
```

## Interactive Component Selection

The tool will guide you through selecting components for your project:

### Frontend Framework Options
- React (TypeScript, modern hooks)
- Vue (Vue 3 with Composition API)
- Angular (Latest Angular with TypeScript)
- Skip

### UI Framework Options
- Tailwind CSS (complete setup with configuration)
- shadcn/ui (component library with TypeScript)
- None/Skip

### Backend Options
- Python (FastAPI with DDD/Service Layer)
- Node.js (Express.js with TypeScript)
- Golang (Gin framework with clean architecture)
- Skip

### Database Options
- MySQL
- PostgreSQL
- SQLite
- Skip

### Build Tool Options (for frontend)
- Vite (recommended - fast HMR, optimized builds)
- Webpack (traditional bundling with extensive configuration)
- Babel + Webpack (custom transpilation with webpack bundling)

### Additional Options
- Atlas migration tool (recommended)
- Package manager selection (npm, yarn)
- GitHub Actions CI/CD workflows (recommended)
- Docker infrastructure generation (automatic)
- Model Context Protocol (MCP) integration with Context7 (recommended)
- Comprehensive project documentation generation

## Generated Project Structure

### Full Stack Example
```
my-project/
├── README.md              # Comprehensive project documentation
├── CLAUDE.md              # Main project documentation
├── .env.example           # Environment variables template
├── .mcp.json              # Model Context Protocol configuration (if enabled)
├── .gitignore
├── package.json           # Root-level npm scripts, workspaces
├── requirements.txt       # Project Python dependencies
├── docker-compose.yml     # Main docker-compose configuration
├── docker-compose.dev.yml # Development environment configuration
├── docker-compose.staging.yml # Staging environment configuration
├── docker-compose.prod.yml # Production environment configuration
├── .github/               # GitHub Actions workflows
│   ├── workflows/
│   │   └── ci.yml         # Continuous integration
│   └── CLAUDE.md          # CI/CD documentation
├── infra/                 # Docker infrastructure
│   └── docker/
│       ├── frontend/
│       │   └── Dockerfile # Frontend container (multi-stage build)
│       ├── backend/
│       │   └── Dockerfile # Backend container (Python/Node.js/Golang)
│       └── database/
│           └── Dockerfile # Database container (MySQL/PostgreSQL)
├── frontend/              # React/Vue/Angular application
│   ├── CLAUDE.md          # Frontend-specific documentation
│   ├── package.json
│   ├── vite.config.ts     # Build tool configuration
│   ├── src/
│   │   ├── main.tsx       # Application entry point
│   │   └── App.tsx        # Main component
│   ├── public/
│   └── ...
├── backend/               # Python/Node.js/Golang API
│   ├── CLAUDE.md          # Backend-specific documentation
│   ├── app/
│   │   ├── main.py        # FastAPI application entry point
│   │   ├── api/           # API routes
│   │   ├── domain/        # Domain models
│   │   ├── services/      # Business logic
│   │   └── repositories/  # Data access layer
│   ├── requirements.txt
│   ├── Dockerfile         # Container configuration
│   └── ...
└── migrations/            # Database migrations (Atlas)
    ├── CLAUDE.md          # Migration documentation
    └── atlas.hcl          # Atlas configuration
```

## CLAUDE.md Documentation

Each generated project includes comprehensive CLAUDE.md files containing:

- **Project Description Template**
- **Technology Stack Overview** (including build tools and CI/CD)
- **Environment Setup Instructions**
- **Development Commands** (framework-specific with build tools)
- **Architecture Patterns**
- **Coding Standards**
- **Testing Guidelines**
- **Build and Deployment Instructions**
- **CI/CD Pipeline Documentation** (if GitHub Actions selected)
- **Docker Commands and Infrastructure** (complete containerization guide)
- **MCP Integration Guide** (if Context7 MCP enabled)
- **AI API Keys Setup** (ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY)

## Environment Variables

Generated projects include `.env.example` templates with:

```env
# AI API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_URL=your_database_url_here
DB_HOST=localhost
DB_PORT=5432

# Application Settings
ENV=development
DEBUG=true
PORT=8000
```

## Requirements

- Python 3.8+
- Cross-platform compatibility (Windows, macOS, Linux)

## Development

```bash
# Clone the repository
git clone https://github.com/swhsiang/create-claude-app.git
cd create-claude-app

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
pytest tests/ --cov=src/create_claude_app

# Run with coverage report
pytest tests/ --cov=src/create_claude_app --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow Google Python Style Guide
4. Add tests for new functionality
5. Submit a pull request

## Issues and Support

Report issues at: https://github.com/swhsiang/create-claude-app/issues

## License

MIT License - see LICENSE file for details

## Roadmap

### ✅ Recently Completed (v0.4.0)
- **CLI Arguments**: Complete non-interactive mode with all project options
- **Mixed Mode Support**: Partial CLI args with intelligent defaults
- **Enhanced Validation**: CLI argument compatibility checking
- **Backward Compatibility**: Maintained interactive mode when no args provided
- **Comprehensive Help**: Detailed CLI documentation with all valid options

### ✅ Previous Features (v0.3.0)
- **Docker Infrastructure**: Complete containerization with multi-stage builds
- **Environment-Specific Configurations**: dev, staging, prod docker-compose files
- **MCP Integration**: Model Context Protocol support with Context7
- **Enhanced Documentation**: MCP setup and integration guides

### ✅ Features (v0.2.0)
- **Frontend Build Tools**: Vite, Webpack, Babel + Webpack support
- **GitHub Actions CI/CD**: Comprehensive workflow generation
- **Framework Entry Points**: React, Vue, Angular, Python entry files
- **Enhanced README Generation**: Detailed development instructions
- **Build Tool Configurations**: Vite and Webpack config files
- **Package Manager Selection**: npm, yarn support

### 🔄 In Progress
- **Testing Framework Integration**: Jest, Vitest, Pytest templates
- **Database ORM Integration**: Prisma, SQLAlchemy, TypeORM

### 📋 Planned Features
- **IDE Configuration Files**: VS Code, JetBrains settings
- **Deployment Templates**: Vercel, Netlify, AWS, GCP configurations
- **Kubernetes Support**: Helm charts and k8s manifests
- **Advanced MCP Features**: Custom server configurations and additional MCP servers