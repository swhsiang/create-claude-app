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
- Docker-compose.yml generation
- .env.example file creation
- GitHub Actions workflow generation
- Framework entry point file generation
- Build tool configuration file generation

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

#### Test Coverage Goals
- Aim for 90%+ code coverage
- Focus on edge cases and error conditions
- Test all user interaction paths

### Development Milestones
1. **Phase 1**: Core CLI infrastructure and basic project structure ✅ COMPLETED
2. **Phase 2**: User interaction prompts and input validation ✅ COMPLETED
3. **Phase 3**: Input validation and compatibility checking 🔄 IN PROGRESS
4. **Phase 4**: File operations and error handling
5. **Phase 5**: Template generation system
6. **Phase 6**: Integration testing and package distribution

### Progress Update
**Completed:**
- ✅ Project structure setup with src/create_claude_app/
- ✅ CLI module with Click framework (test coverage: 100%)
- ✅ Prompts module with Rich library (test coverage: 99%)
- ✅ ProjectConfiguration dataclass
- ✅ Package configuration (pyproject.toml, requirements)
- ✅ Comprehensive test suite with pytest

**Next Steps:**
- 🔄 Implement validators module with TDD
- 🔄 Implement file operations module with TDD
- 🔄 Implement template generation system

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
- **Last Commit**: bfc3db1 - Implement comprehensive PRD enhancements with TDD
- **Implementation**: ✅ COMPLETE - All PRD enhancements implemented and integrated
- **Test Coverage**: 94% overall (84 tests passing)
  - CLI: 97%
  - Prompts: 100%
  - Validators: 100%
  - File Operations: 88%
  - Generators: 93%
  - Integration: 100%
- **Status**: Production ready with all PRD features implemented

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

### Implementation Summary
✅ **Core TDD Phases Completed**:
1. ✅ Core CLI infrastructure and project structure
2. ✅ Interactive prompts and input validation  
3. ✅ Input validation and compatibility checking
4. ✅ File operations and error handling
5. ✅ Template generation system
6. ✅ End-to-end integration testing

🔄 **PRD Enhancement Phase**:
7. 🔄 Frontend build tool selection and configuration
8. 🔄 GitHub Actions CI/CD workflow generation
9. 🔄 Enhanced entry points and README.md generation

**Current Tool Features**:
- Interactive CLI with rich terminal UI
- Support for React, Vue, Angular frontends
- Tailwind CSS and shadcn/ui integration
- Python (FastAPI), Node.js, Golang backends
- PostgreSQL, MySQL, SQLite databases
- Comprehensive CLAUDE.md generation
- Project scaffolding with best practices
- Error handling with cleanup mechanisms

**Planned PRD Enhancement Features**:
- Frontend build tool selection (Vite/Webpack/Babel)
- GitHub Actions CI/CD workflow generation
- Framework-specific entry point files
- Enhanced README.md with comprehensive development instructions
- Build tool configuration files (vite.config.js, webpack.config.js)