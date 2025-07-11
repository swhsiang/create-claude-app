# create-claude-app Development Guide

## Project Overview
Interactive Python CLI tool that scaffolds new projects optimized for Claude Code development. Creates structured project templates with comprehensive CLAUDE.md files.

## Development Strategy and Testing Plan

### Test-Driven Development (TDD) Approach
Following TDD methodology with comprehensive test coverage before implementation.

### Testing Plan

#### Unit Tests Structure
```
tests/
├── test_cli.py              # CLI argument parsing, main entry point
├── test_prompts.py          # User interaction prompts
├── test_generators.py       # Template generation logic
├── test_validators.py       # Input validation and compatibility checks
├── test_file_operations.py  # File/directory creation and cleanup
└── fixtures/                # Test data and expected outputs
    ├── templates/           # Sample template files
    └── expected_projects/   # Expected project structures
```

#### Core Test Categories

**CLI Interface Tests (`test_cli.py`)**
- Command parsing with valid/invalid arguments
- Help text display
- Version information
- Error handling for missing arguments

**User Interaction Tests (`test_prompts.py`)**
- Frontend framework selection
- UI framework compatibility validation
- Backend and database option selection
- Package manager selection (npm, yarn)
- Atlas migration tool prompt
- Build tool selection (Vite, Webpack, Babel + Webpack)
- GitHub Actions CI/CD prompt

**Template Generation Tests (`test_generators.py`)**
- File structure creation for different combinations
- CLAUDE.md content generation
- Package.json/requirements.txt creation
- Docker infrastructure generation (infra/docker/ folder structure)
- Docker-compose.yml generation (main, dev, staging, prod variants)
- Frontend/Backend/Database Dockerfile generation
- .env.example file creation
- GitHub Actions workflow generation
- Framework entry point file generation
- Build tool configuration file generation
- Enhanced README.md with Docker commands section

**Validation Tests (`test_validators.py`)**
- Incompatible combination detection (Angular + shadcn/ui)
- Directory existence checks
- Input sanitization

**File Operations Tests (`test_file_operations.py`)**
- Directory creation and cleanup
- File writing with proper permissions
- Error recovery and rollback

#### Test Data Strategy
- Use `pytest.fixture` for temporary directories
- Mock user inputs with `unittest.mock.patch`
- Create sample template files in `tests/fixtures/`
- Use `pytest.parametrize` for testing multiple combinations

#### Integration Tests
- End-to-end project generation scenarios
- Template file validation
- Generated project structure verification
- Docker infrastructure validation (infra/docker/ folder structure)
- Docker-compose environment file validation (dev/staging/prod)
- Dockerfile generation for all components (frontend/backend/database)

#### Test Coverage Goals
- Aim for 90%+ code coverage
- Focus on edge cases and error conditions
- Test all user interaction paths

### Development Milestones
1. **Phase 1**: Core CLI infrastructure and basic project structure ✅ COMPLETED
2. **Phase 2**: User interaction prompts and input validation ✅ COMPLETED
3. **Phase 3**: Input validation and compatibility checking ✅ COMPLETED
4. **Phase 4**: File operations and error handling ✅ COMPLETED
5. **Phase 5**: Template generation system ✅ COMPLETED
6. **Phase 6**: Integration testing and package distribution ✅ COMPLETED
7. **Phase 7**: PRD Enhancement Implementation ✅ COMPLETED
8. **Phase 8**: Docker Infrastructure Implementation ✅ COMPLETED
9. **Phase 9**: MCP Integration Implementation 🔄 PLANNED

### Progress Update
**Completed:**
- ✅ Project structure setup with src/create_claude_app/
- ✅ CLI module with Click framework (test coverage: 100%)
- ✅ Prompts module with Rich library (test coverage: 99%)
- ✅ ProjectConfiguration dataclass
- ✅ Package configuration (pyproject.toml, requirements)
- ✅ Comprehensive test suite with pytest

**Next Steps (Phase 9 - MCP Integration):**
- 🔄 Add MCP prompt to user interaction flow
- 🔄 Implement MCP configuration validation
- 🔄 Generate .mcp.json file with Context7 configuration
- 🔄 Add MCP documentation to generated CLAUDE.md files
- 🔄 Integrate MCP workflow with existing project generation
- 🔄 Add comprehensive MCP test suite

**Completed Docker Infrastructure (Phase 8):**
- ✅ Implement Docker infrastructure generation (infra/docker/ folder structure)
- ✅ Generate build-tool specific frontend Dockerfiles
- ✅ Generate language-specific backend Dockerfiles
- ✅ Generate database Dockerfiles with standard images
- ✅ Generate environment-specific docker-compose files (dev/staging/prod)
- ✅ Update README.md generation to include Docker commands section
- ✅ Add Docker optimization documentation to backend README & CLAUDE.md

### Technology Stack
- **CLI Framework**: click
- **Terminal UI**: rich
- **Template Engine**: jinja2
- **Testing**: pytest
- **File Operations**: pathlib

### Development Commands
```bash
# Setup development environment
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
pytest tests/ --cov=src/create_claude_app

# Run specific test file
pytest tests/test_cli.py -v

# Run with coverage report
pytest tests/ --cov=src/create_claude_app --cov-report=html

# Git workflow after each milestone
git add <files>
git commit -m "Clear commit message describing changes"
```

### Quality Assurance
- Follow Google Python Style Guide
- Use black for code formatting
- Use flake8 for linting
- Type hints with mypy
- Pre-commit hooks for code quality

### Git Workflow
**Important**: After completing each milestone, commit changes with clear messages:
1. Run tests to ensure everything passes
2. Add only the files that should be committed (check .gitignore)
3. Write descriptive commit messages explaining what was implemented
4. Update CLAUDE.md with progress status
5. Commit the documentation update separately if needed

### Current Status
- **Last Commit**: TBD - Implement CLI arguments feature with TDD
- **Implementation**: ✅ COMPLETE - All CLI arguments features implemented and integrated
- **Test Coverage**: 95% overall (137 tests passing)
  - CLI: 94%
  - Prompts: 100%
  - Validators: 100%
  - File Operations: 90%
  - Generators: 95%
  - Integration: 100%
- **Status**: Production ready with comprehensive CLI arguments support

### PRD Enhancement Phase ✅ COMPLETED
**Implemented PRD Requirements:**
1. **Frontend Build Tool Selection**: Vite (recommended), Webpack, Babel + Webpack ✅
2. **GitHub Actions CI/CD**: Optional workflow generation based on tech stack ✅
3. **Enhanced Entry Points**: Framework-specific entry point files with proper structure ✅
4. **Comprehensive README.md**: Detailed development instructions, build commands, deployment ✅
5. **Build Tool Configuration**: Vite/Webpack config files generation ✅
6. **Package Manager Selection**: npm, yarn support (removed npx) ✅

### Updated Development Milestones
**Phase 1-6: Core Implementation** ✅ COMPLETED
**Phase 7: PRD Enhancement Implementation** ✅ COMPLETED
- ✅ Frontend build tool selection prompts
- ✅ GitHub Actions workflow generation
- ✅ Enhanced entry point file generation
- ✅ Comprehensive README.md with build instructions
- ✅ Build tool configuration files

### Test Plan for PRD Enhancements ✅ COMPLETED
**Implemented Test Categories:**
- **Build Tool Selection Tests**: Vite/Webpack/Babel prompt handling ✅
- **CI/CD Generation Tests**: GitHub Actions workflow file creation ✅
- **Entry Point Tests**: Framework-specific entry file generation ✅
- **Enhanced README Tests**: Comprehensive development instruction validation ✅
- **Build Configuration Tests**: Vite/Webpack config file generation ✅

### Test Plan for MCP Integration Implementation ✅ COMPLETED
**Implemented Test Categories:**
- **MCP Prompt Tests**: User interaction for MCP configuration selection ✅
- **MCP Validation Tests**: Input validation for MCP configuration options ✅
- **MCP File Generation Tests**: .mcp.json creation with Context7 configuration ✅
- **MCP Documentation Tests**: CLAUDE.md integration with MCP setup instructions ✅
- **MCP Integration Tests**: End-to-end project generation with/without MCP ✅
- **MCP Conditional Tests**: Verify no MCP files generated when disabled ✅

### Test Plan for CLI Arguments Implementation ✅ COMPLETED
**Implemented Test Categories:**
- **CLI Parsing Tests**: Command line argument parsing and validation ✅
- **CLI Validation Tests**: Invalid combinations and values error handling ✅
- **CLI Defaults Tests**: Default value application when arguments missing ✅
- **CLI Compatibility Tests**: Interactive vs non-interactive mode compatibility ✅
- **CLI Help Tests**: Help documentation generation with all valid options ✅
- **CLI Integration Tests**: End-to-end project generation with CLI arguments ✅
- **CLI Error Handling Tests**: Clear error messages for invalid inputs ✅

### Test Plan for Docker Infrastructure Implementation ✅ COMPLETED
**Implemented Test Categories:**
- **Docker Infrastructure Tests**: infra/docker/ folder structure creation ✅
- **Frontend Dockerfile Tests**: Build-tool specific Dockerfile generation (Vite/Webpack/Babel) ✅
- **Backend Dockerfile Tests**: Language-specific Dockerfile generation (Python/Node.js/Golang) ✅
- **Database Dockerfile Tests**: Standard image configuration generation ✅
- **Docker Compose Tests**: Environment-specific file generation (main/dev/staging/prod) ✅
- **README Docker Commands Tests**: Docker commands section validation ✅
- **Documentation Tests**: Docker optimization notes in backend README & CLAUDE.md ✅

### Implementation Summary
✅ **Core TDD Phases Completed**:
1. ✅ Core CLI infrastructure and project structure
2. ✅ Interactive prompts and input validation  
3. ✅ Input validation and compatibility checking
4. ✅ File operations and error handling
5. ✅ Template generation system
6. ✅ End-to-end integration testing

✅ **PRD Enhancement Phase**:
7. ✅ Frontend build tool selection and configuration
8. ✅ GitHub Actions CI/CD workflow generation
9. ✅ Enhanced entry points and README.md generation

✅ **Docker Infrastructure Phase**:
10. ✅ Docker infrastructure folder structure (infra/docker/)
11. ✅ Frontend Dockerfiles (build-tool specific)
12. ✅ Backend Dockerfiles (language-specific)
13. ✅ Database Dockerfiles (standard images)
14. ✅ Environment-specific docker-compose files
15. ✅ README.md Docker commands section

✅ **MCP Integration Phase**:
16. ✅ MCP user prompt and validation
17. ✅ Context7 .mcp.json generation
18. ✅ MCP documentation integration
19. ✅ MCP test suite implementation

✅ **CLI Arguments Phase**:
20. ✅ CLI argument parsing and validation
21. ✅ Non-interactive mode implementation
22. ✅ CLI compatibility validation
23. ✅ Enhanced help documentation
24. ✅ CLI arguments test suite

### CLI Arguments Implementation Details ✅ COMPLETED

**Comprehensive CLI Support:**
- **9 CLI Arguments**: All project configuration options available via command line
- **Non-Interactive Mode**: Complete project generation without prompts
- **Mixed Mode**: Partial CLI args with intelligent defaults
- **Backward Compatibility**: Interactive mode preserved when no args provided
- **Validation**: All existing validation logic maintained for CLI mode
- **Error Handling**: Clear, actionable error messages for invalid inputs

**CLI Arguments Available:**
```bash
-f, --frontend [react|vue|angular|none]     # Frontend framework
-B, --backend [python|nodejs|golang|none]  # Backend language  
-d, --database [mysql|postgresql|sqlite|none] # Database system
-u, --ui [tailwind|shadcn|none]            # UI framework
-b, --build-tool [vite|webpack|babel]      # Frontend build tool
-p, --package-manager [npm|yarn]           # Package manager
-a, --atlas                                # Enable Atlas migrations
-g, --github-actions                       # Enable GitHub Actions
-m, --mcp / --no-mcp                       # Enable/disable MCP (default: enabled)
```

**Usage Examples:**
```bash
# Interactive mode (default)
create-claude-app my-project

# Full CLI mode
create-claude-app my-project --frontend react --backend python --database mysql

# Mixed mode with defaults
create-claude-app my-project --frontend vue --ui tailwind

# Short flags
create-claude-app my-project -f react -B python -d postgresql
```

**Test Coverage for CLI Arguments:**
- **27 new CLI argument tests**: Covering all validation scenarios
- **3 new integration tests**: End-to-end CLI workflows
- **16 CLI test categories**: Parsing, validation, defaults, compatibility, help, error handling
- **Incompatible combination validation**: Angular + shadcn/ui properly detected
- **Default application logic**: Missing options use sensible defaults

**Current Tool Features**:
- Interactive CLI with rich terminal UI
- Non-interactive CLI arguments mode with all options
- Support for React, Vue, Angular frontends
- Tailwind CSS and shadcn/ui integration
- Python (FastAPI), Node.js, Golang backends
- PostgreSQL, MySQL, SQLite databases
- Comprehensive CLAUDE.md generation
- Project scaffolding with best practices
- Error handling with cleanup mechanisms
- Model Context Protocol (MCP) integration with Context7
- CLI argument validation and error handling
- Backward compatibility with interactive mode

**Implemented Docker Infrastructure Features**:
- Docker infrastructure folder structure (infra/docker/)
- Build-tool specific frontend Dockerfiles (Vite/Webpack/Babel)
- Language-specific backend Dockerfiles (Python/Node.js/Golang)
- Database Dockerfiles with standard images (MySQL/PostgreSQL/SQLite)
- Environment-specific docker-compose files (dev/staging/prod)
- README.md Docker commands section
- Docker optimization documentation in backend README & CLAUDE.md