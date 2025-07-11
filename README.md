# create-claude-app

Interactive Python CLI tool that scaffolds new projects optimized for Claude Code development. Creates structured project templates with comprehensive CLAUDE.md files to enable developers to quickly start new projects with Claude Code.

## Features

- 🚀 **Quick Project Setup**: Bootstrap new projects in under 2 minutes
- 🎯 **Interactive Selection**: Choose from multiple frontend, backend, and database options
- 📋 **Comprehensive Documentation**: Auto-generated CLAUDE.md files for effective AI-assisted development
- 🏗️ **Clean Architecture**: Industry best practices with Domain-Driven Design patterns
- 🔧 **Multiple Tech Stacks**: Support for React, Vue, Angular, Python, Node.js, Golang, and more
- 📦 **Database Integration**: MySQL, PostgreSQL, SQLite with Atlas migration tool support
- 🎨 **UI Framework Support**: Tailwind CSS, shadcn/ui with automatic compatibility checking

## Installation

```bash
# Install via pip
pip install create-claude-app

# Install via homebrew (coming soon)
brew install create-claude-app
```

## Usage

```bash
# Create a new project
create-claude-app my-new-project

# Follow the interactive prompts to select your tech stack
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

### Additional Options
- Atlas migration tool (recommended)
- Package manager selection (npm, yarn, pnpm)

## Generated Project Structure

### Full Stack Example
```
my-project/
├── README.md
├── CLAUDE.md              # Main project documentation
├── .env.example           # Environment variables template
├── .gitignore
├── package.json           # Root-level npm scripts, workspaces
├── requirements.txt       # Project Python dependencies
├── docker-compose.yml     # Database services
├── frontend/              # React/Vue/Angular application
│   ├── CLAUDE.md          # Frontend-specific documentation
│   ├── package.json
│   ├── src/
│   └── ...
├── backend/               # Python/Node.js/Golang API
│   ├── CLAUDE.md          # Backend-specific documentation
│   ├── app/
│   ├── requirements.txt
│   └── ...
└── migrations/            # Database migrations (Atlas)
    ├── CLAUDE.md          # Migration documentation
    └── atlas.hcl          # Atlas configuration
```

## CLAUDE.md Documentation

Each generated project includes comprehensive CLAUDE.md files containing:

- **Project Description Template**
- **Technology Stack Overview**
- **Environment Setup Instructions**
- **Development Commands**
- **Architecture Patterns**
- **Coding Standards**
- **Testing Guidelines**
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

- Additional frontend frameworks (Svelte, Solid.js)
- More UI frameworks (Chakra UI, Material-UI)
- More backend options (Rust, Java, C#)
- CI/CD pipeline templates
- Docker deployment templates
- IDE configuration files