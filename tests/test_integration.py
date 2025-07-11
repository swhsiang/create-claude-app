"""Integration tests for create-claude-app."""
import pytest
import tempfile
import os
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch

from create_claude_app.cli import main


class TestIntegration:
    """Test end-to-end functionality."""

    def test_create_minimal_project_integration(self):
        """Test creating a minimal project end-to-end."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Mock user inputs for minimal project
                inputs = [
                    '4',  # Skip frontend
                    '4',  # Skip backend  
                    '4',  # Skip database
                    'n',  # No Atlas
                    'n'   # No GitHub Actions
                ]
                
                result = runner.invoke(main, ['minimal-project'], input='\n'.join(inputs))
                
                # Check command succeeded
                assert result.exit_code == 0
                assert 'created successfully' in result.output
                
                # Check project directory was created
                project_path = Path('minimal-project')
                assert project_path.exists()
                assert project_path.is_dir()
                
                # Check basic files were created
                assert (project_path / 'CLAUDE.md').exists()
                assert (project_path / '.env.example').exists()
                assert (project_path / 'README.md').exists()
                
                # Check that optional directories were NOT created
                assert not (project_path / 'frontend').exists()
                assert not (project_path / 'backend').exists()
                assert not (project_path / 'migrations').exists()
                
            finally:
                os.chdir(original_cwd)

    def test_create_fullstack_project_integration(self):
        """Test creating a full-stack project end-to-end."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Mock user inputs for full-stack project
                inputs = [
                    '1',  # React
                    '1',  # Tailwind CSS
                    '1',  # Vite (build tool)
                    '1',  # Python
                    '2',  # PostgreSQL
                    '1',  # npm
                    'y',  # Yes to Atlas
                    'y'   # Yes to GitHub Actions
                ]
                
                result = runner.invoke(main, ['fullstack-app'], input='\n'.join(inputs))
                
                # Check command succeeded
                assert result.exit_code == 0
                assert 'created successfully' in result.output
                
                # Check project directory was created
                project_path = Path('fullstack-app')
                assert project_path.exists()
                
                # Check directory structure
                assert (project_path / 'frontend').exists()
                assert (project_path / 'backend').exists()
                assert (project_path / 'migrations').exists()
                
                # Check core files
                assert (project_path / 'CLAUDE.md').exists()
                assert (project_path / '.env.example').exists()
                assert (project_path / 'README.md').exists()
                assert (project_path / 'docker-compose.yml').exists()
                
                # Check frontend files
                assert (project_path / 'frontend' / 'package.json').exists()
                assert (project_path / 'frontend' / 'CLAUDE.md').exists()
                
                # Check backend files
                assert (project_path / 'backend' / 'requirements.txt').exists()
                assert (project_path / 'backend' / 'CLAUDE.md').exists()
                
                # Check new features - entry points
                assert (project_path / 'frontend' / 'src' / 'main.tsx').exists()
                assert (project_path / 'frontend' / 'src' / 'App.tsx').exists()
                assert (project_path / 'frontend' / 'vite.config.ts').exists()
                assert (project_path / 'backend' / 'app' / 'main.py').exists()
                assert (project_path / 'backend' / 'Dockerfile').exists()
                
                # Check GitHub Actions
                assert (project_path / '.github' / 'workflows' / 'ci.yml').exists()
                assert (project_path / '.github' / 'CLAUDE.md').exists()
                
                # Validate file contents
                claude_md = (project_path / 'CLAUDE.md').read_text()
                assert 'React' in claude_md
                assert 'Tailwind CSS' in claude_md
                assert 'Python' in claude_md
                assert 'PostgreSQL' in claude_md
                
                env_example = (project_path / '.env.example').read_text()
                assert 'ANTHROPIC_API_KEY' in env_example
                assert 'DATABASE_URL' in env_example
                assert 'PostgreSQL' in env_example
                
            finally:
                os.chdir(original_cwd)

    def test_invalid_project_name_integration(self):
        """Test handling of invalid project names."""
        runner = CliRunner()
        
        # Test with invalid character
        result = runner.invoke(main, ['invalid/name'])
        assert result.exit_code != 0
        assert 'Invalid project name' in result.output

    def test_existing_directory_integration(self):
        """Test handling of existing directory."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create existing directory
                existing_dir = Path('existing-project')
                existing_dir.mkdir()
                
                result = runner.invoke(main, ['existing-project'])
                assert result.exit_code != 0
                assert 'already exists' in result.output
                
            finally:
                os.chdir(original_cwd)

    def test_incompatible_combination_validation(self):
        """Test that incompatible combinations are properly validated."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Try Angular + shadcn/ui (incompatible)
                inputs = [
                    '3',  # Angular
                    '2',  # shadcn/ui (incompatible with Angular)
                    '1',  # Vite (build tool)
                    '4',  # Skip backend
                    '4',  # Skip database
                    'n',  # No Atlas
                    'n'   # No GitHub Actions
                ]
                
                result = runner.invoke(main, ['angular-app'], input='\n'.join(inputs))
                
                # Should show warning during prompts AND fail validation
                assert 'not recommended' in result.output or 'incompatible' in result.output.lower()
                
                # Command should fail due to validation
                assert result.exit_code != 0
                
                # Project should NOT be created
                project_path = Path('angular-app')
                assert not project_path.exists()
                
            finally:
                os.chdir(original_cwd)

    def test_create_project_with_new_features_integration(self):
        """Test creating a project with all new PRD features."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Mock user inputs for project with all new features
                inputs = [
                    '2',  # Vue
                    '1',  # Tailwind CSS
                    '2',  # Webpack (build tool)
                    '1',  # Python
                    '1',  # MySQL
                    '3',  # yarn
                    'y',  # Yes to Atlas
                    'y'   # Yes to GitHub Actions
                ]
                
                result = runner.invoke(main, ['feature-rich-app'], input='\n'.join(inputs))
                
                # Check command succeeded
                assert result.exit_code == 0
                assert 'created successfully' in result.output
                
                # Check project directory was created
                project_path = Path('feature-rich-app')
                assert project_path.exists()
                
                # Check all new features are present
                # Build tool configuration
                assert (project_path / 'frontend' / 'webpack.config.js').exists()
                
                # Entry points
                assert (project_path / 'frontend' / 'src' / 'main.ts').exists()
                assert (project_path / 'frontend' / 'src' / 'App.vue').exists()
                assert (project_path / 'backend' / 'app' / 'main.py').exists()
                
                # GitHub Actions
                assert (project_path / '.github' / 'workflows' / 'ci.yml').exists()
                
                # Enhanced README
                readme_content = (project_path / 'README.md').read_text()
                assert 'Vue (Webpack)' in readme_content
                assert 'Tailwind CSS' in readme_content
                assert 'Python (FastAPI)' in readme_content
                assert 'Mysql' in readme_content
                assert 'yarn' in readme_content
                assert 'GitHub Actions' in readme_content
                assert 'Development Setup' in readme_content
                assert 'yarn install' in readme_content
                assert 'yarn run dev' in readme_content
                assert 'Project Structure' in readme_content
                
                # CI workflow content
                ci_content = (project_path / '.github' / 'workflows' / 'ci.yml').read_text()
                assert 'name: CI' in ci_content
                assert 'yarn' in ci_content
                assert 'mysql' in ci_content
                
            finally:
                os.chdir(original_cwd)