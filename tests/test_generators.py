"""Tests for template generators module."""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from create_claude_app.generators import (
    generate_project,
    generate_claude_md,
    generate_env_example,
    generate_package_json,
    generate_requirements_txt,
    generate_docker_compose,
    TemplateGenerator,
    TemplateError,
)
from create_claude_app.prompts import ProjectConfiguration


class TestTemplateGenerator:
    """Test template generation functionality."""

    def test_generate_project_minimal(self):
        """Test generating a minimal project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ProjectConfiguration(
                project_name='test-project',
                frontend=None,
                backend=None,
                database=None,
                use_atlas=False
            )
            
            project_path = Path(temp_dir) / 'test-project'
            result = generate_project(str(project_path), config)
            
            # Check that project was created
            assert project_path.exists()
            assert result['success'] is True
            assert 'files_created' in result
            
            # Check that basic files were created
            assert (project_path / 'CLAUDE.md').exists()
            assert (project_path / '.env.example').exists()
            assert (project_path / 'README.md').exists()

    def test_generate_project_full_stack(self):
        """Test generating a full-stack project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ProjectConfiguration(
                project_name='fullstack-app',
                frontend='react',
                ui_framework='tailwind',
                backend='python',
                database='postgresql',
                package_manager='npm',
                use_atlas=True
            )
            
            project_path = Path(temp_dir) / 'fullstack-app'
            result = generate_project(str(project_path), config)
            
            # Check that project was created
            assert project_path.exists()
            assert result['success'] is True
            
            # Check directory structure
            assert (project_path / 'frontend').exists()
            assert (project_path / 'backend').exists()
            assert (project_path / 'migrations').exists()
            
            # Check configuration files
            assert (project_path / 'frontend' / 'package.json').exists()
            assert (project_path / 'backend' / 'requirements.txt').exists()
            assert (project_path / 'docker-compose.yml').exists()
            assert (project_path / 'CLAUDE.md').exists()

    def test_generate_project_existing_directory(self):
        """Test error when project directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = ProjectConfiguration(project_name='existing-project')
            
            project_path = Path(temp_dir) / 'existing-project'
            project_path.mkdir()
            
            with pytest.raises(TemplateError) as exc_info:
                generate_project(str(project_path), config)
            
            assert 'already exists' in str(exc_info.value)

    def test_generate_claude_md_minimal(self):
        """Test generating CLAUDE.md for minimal project."""
        config = ProjectConfiguration(
            project_name='test-project',
            frontend=None,
            backend=None,
            database=None
        )
        
        content = generate_claude_md(config)
        
        # Check basic structure
        assert '# test-project' in content
        assert 'Project Overview' in content
        assert 'Technology Stack' in content
        assert 'Development Commands' in content
        assert 'Environment Setup' in content

    def test_generate_claude_md_full_stack(self):
        """Test generating CLAUDE.md for full-stack project."""
        config = ProjectConfiguration(
            project_name='fullstack-app',
            frontend='react',
            ui_framework='tailwind',
            backend='python',
            database='postgresql',
            package_manager='npm',
            use_atlas=True
        )
        
        content = generate_claude_md(config)
        
        # Check technology stack mentions
        assert 'React' in content
        assert 'Tailwind CSS' in content
        assert 'Python' in content
        assert 'PostgreSQL' in content
        assert 'npm' in content
        assert 'Atlas' in content

    def test_generate_env_example_minimal(self):
        """Test generating .env.example for minimal project."""
        config = ProjectConfiguration(
            project_name='test-project',
            database=None
        )
        
        content = generate_env_example(config)
        
        # Check basic AI keys
        assert 'ANTHROPIC_API_KEY' in content
        assert 'OPENAI_API_KEY' in content
        assert 'GEMINI_API_KEY' in content
        
        # Should not include database config
        assert 'DATABASE_URL' not in content

    def test_generate_env_example_with_database(self):
        """Test generating .env.example with database configuration."""
        config = ProjectConfiguration(
            project_name='test-project',
            database='postgresql'
        )
        
        content = generate_env_example(config)
        
        # Check database configuration
        assert 'DATABASE_URL' in content
        assert 'DB_HOST' in content
        assert 'DB_PORT' in content
        assert 'PostgreSQL' in content

    def test_generate_package_json_react_npm(self):
        """Test generating package.json for React with npm."""
        config = ProjectConfiguration(
            project_name='react-app',
            frontend='react',
            ui_framework='tailwind',
            package_manager='npm'
        )
        
        content = generate_package_json(config)
        
        # Check basic structure
        assert '"name": "react-app"' in content
        assert '"react"' in content
        assert '"tailwindcss"' in content
        assert '"scripts"' in content
        assert '"dev"' in content

    def test_generate_package_json_vue_yarn(self):
        """Test generating package.json for Vue with yarn."""
        config = ProjectConfiguration(
            project_name='vue-app',
            frontend='vue',
            package_manager='yarn'
        )
        
        content = generate_package_json(config)
        
        # Check Vue-specific content
        assert '"vue"' in content
        assert 'yarn' in content or 'dev' in content

    def test_generate_requirements_txt_python(self):
        """Test generating requirements.txt for Python backend."""
        config = ProjectConfiguration(
            project_name='python-app',
            backend='python',
            database='postgresql'
        )
        
        content = generate_requirements_txt(config)
        
        # Check Python dependencies
        assert 'fastapi' in content
        assert 'psycopg2' in content or 'postgresql' in content.lower()
        assert 'uvicorn' in content

    def test_generate_requirements_txt_no_backend(self):
        """Test that requirements.txt returns None for non-Python projects."""
        config = ProjectConfiguration(
            project_name='frontend-only',
            frontend='react',
            backend=None
        )
        
        content = generate_requirements_txt(config)
        assert content is None

    def test_generate_docker_compose_with_database(self):
        """Test generating docker-compose.yml with database."""
        config = ProjectConfiguration(
            project_name='app-with-db',
            database='postgresql'
        )
        
        content = generate_docker_compose(config)
        
        # Check Docker Compose structure
        assert 'version:' in content
        assert 'services:' in content
        assert 'postgres' in content
        assert 'POSTGRES_DB' in content

    def test_generate_docker_compose_mysql(self):
        """Test generating docker-compose.yml with MySQL."""
        config = ProjectConfiguration(
            project_name='mysql-app',
            database='mysql'
        )
        
        content = generate_docker_compose(config)
        
        # Check MySQL-specific content
        assert 'mysql' in content
        assert 'MYSQL_DATABASE' in content

    def test_generate_docker_compose_no_database(self):
        """Test that docker-compose.yml returns None without database."""
        config = ProjectConfiguration(
            project_name='no-db-app',
            database=None
        )
        
        content = generate_docker_compose(config)
        assert content is None

    def test_template_generator_class(self):
        """Test TemplateGenerator class functionality."""
        config = ProjectConfiguration(
            project_name='test-project',
            frontend='react',
            backend='python'
        )
        
        generator = TemplateGenerator(config)
        
        # Test that generator has configuration
        assert generator.config == config
        assert generator.config.project_name == 'test-project'

    def test_template_error_is_exception(self):
        """Test that TemplateError is a proper exception."""
        error = TemplateError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_template_error_with_details(self):
        """Test TemplateError with additional details."""
        error = TemplateError("Test error", template="test.txt")
        assert str(error) == "Test error"
        assert error.template == "test.txt"