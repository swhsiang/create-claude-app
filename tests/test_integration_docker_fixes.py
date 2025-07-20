"""Integration tests for Docker infrastructure fixes."""
import pytest
import tempfile
import os
from pathlib import Path
from click.testing import CliRunner

from create_claude_app.cli import main
from create_claude_app.prompts import ProjectConfiguration
from create_claude_app.generators import (
    generate_frontend_dockerfile_dev,
    generate_docker_compose_dev,
    generate_vite_config,
    generate_dev_script,
)


class TestDockerInfrastructureFixes:
    """Test that Docker infrastructure generation has all the fixes applied."""

    def test_docker_infrastructure_fixes_integration(self):
        """Test that Docker infrastructure generation has all the fixes applied."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create a project with Docker infrastructure
                inputs = [
                    '1',  # React
                    '1',  # Tailwind CSS
                    '1',  # Vite
                    '1',  # Python
                    '2',  # PostgreSQL
                    '1',  # npm
                    'n',  # No Atlas
                    'n',  # No GitHub Actions
                    'n'   # No MCP
                ]
                
                result = runner.invoke(main, ['docker-test-app'], input='\n'.join(inputs))
                assert result.exit_code == 0
                
                project_path = Path('docker-test-app')
                
                # Test 1: Docker Compose files should not have version attribute
                docker_compose_files = [
                    project_path / 'docker-compose.yml',
                    project_path / 'infra' / 'docker' / 'docker-compose.dev.yml',
                    project_path / 'infra' / 'docker' / 'docker-compose.staging.yml',
                    project_path / 'infra' / 'docker' / 'docker-compose.prod.yml'
                ]
                
                for compose_file in docker_compose_files:
                    if compose_file.exists():
                        content = compose_file.read_text()
                        assert "version:" not in content, f"{compose_file} should not contain version attribute"
                
                # Test 2: Vite projects should have index.html in frontend root
                if (project_path / 'frontend' / 'vite.config.ts').exists():
                    assert (project_path / 'frontend' / 'index.html').exists(), "Vite project should have index.html in frontend root"
                    assert not (project_path / 'frontend' / 'public' / 'index.html').exists(), "Vite project should NOT have index.html in public directory"
                
                # Test 3: Tailwind CSS files should be generated
                assert (project_path / 'frontend' / 'src' / 'index.css').exists(), "Tailwind project should have index.css"
                assert (project_path / 'frontend' / 'tailwind.config.js').exists(), "Tailwind project should have tailwind.config.js"
                assert (project_path / 'frontend' / 'postcss.config.js').exists(), "Tailwind project should have postcss.config.js"
                
                # Check CSS content
                css_content = (project_path / 'frontend' / 'src' / 'index.css').read_text()
                assert '@tailwind base' in css_content
                assert '@tailwind components' in css_content
                assert '@tailwind utilities' in css_content
                
                # Test 4: Database Dockerfiles should not have COPY init commands
                db_dockerfile = project_path / 'infra' / 'docker' / 'database' / 'Dockerfile'
                if db_dockerfile.exists():
                    dockerfile_content = db_dockerfile.read_text()
                    assert 'COPY init/' not in dockerfile_content, "Database Dockerfile should not COPY non-existent init directory"
                    assert 'COPY database/' not in dockerfile_content, "Database Dockerfile should not COPY non-existent database directory"
                
                # Test 5: docker-compose.dev.yml should not mount non-existent init directory
                dev_compose = project_path / 'infra' / 'docker' / 'docker-compose.dev.yml'
                if dev_compose.exists():
                    dev_compose_content = dev_compose.read_text()
                    assert './database/init:/docker-entrypoint-initdb.d' not in dev_compose_content, "docker-compose.dev.yml should not mount non-existent init directory"
                    
                    # Test 6: Frontend service should have CHOKIDAR_USEPOLLING for macOS hot reload
                    if 'frontend' in dev_compose_content:
                        assert 'CHOKIDAR_USEPOLLING=true' in dev_compose_content, "Frontend service should have CHOKIDAR_USEPOLLING for hot reload"
                
            finally:
                os.chdir(original_cwd)

    def test_webpack_project_structure(self):
        """Test that Webpack projects have correct index.html placement."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create a project with Webpack
                inputs = [
                    '1',  # React
                    '1',  # Tailwind CSS
                    '2',  # Webpack
                    '4',  # No backend
                    '4',  # No database
                    '1',  # npm
                    'n',  # No Atlas
                    'n',  # No GitHub Actions
                    'n'   # No MCP
                ]
                
                result = runner.invoke(main, ['webpack-test-app'], input='\n'.join(inputs))
                assert result.exit_code == 0
                
                project_path = Path('webpack-test-app')
                
                # Webpack projects should have index.html in public directory
                assert (project_path / 'frontend' / 'public' / 'index.html').exists(), "Webpack project should have index.html in public directory"
                assert not (project_path / 'frontend' / 'index.html').exists(), "Webpack project should NOT have index.html in frontend root"
                
            finally:
                os.chdir(original_cwd)

    def test_vue_tailwind_css_files(self):
        """Test that Vue projects with Tailwind generate style.css instead of index.css."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create a Vue project with Tailwind
                inputs = [
                    '2',  # Vue
                    '1',  # Tailwind CSS
                    '1',  # Vite
                    '4',  # No backend
                    '4',  # No database
                    '1',  # npm
                    'n',  # No Atlas
                    'n',  # No GitHub Actions
                    'n'   # No MCP
                ]
                
                result = runner.invoke(main, ['vue-tailwind-app'], input='\n'.join(inputs))
                assert result.exit_code == 0
                
                project_path = Path('vue-tailwind-app')
                
                # Vue projects should have style.css instead of index.css
                assert (project_path / 'frontend' / 'src' / 'style.css').exists(), "Vue Tailwind project should have style.css"
                assert not (project_path / 'frontend' / 'src' / 'index.css').exists(), "Vue project should NOT have index.css"
                
                # Check CSS content
                css_content = (project_path / 'frontend' / 'src' / 'style.css').read_text()
                assert '@tailwind base' in css_content
                assert '@tailwind components' in css_content
                assert '@tailwind utilities' in css_content
                
            finally:
                os.chdir(original_cwd)

    def test_dev_script_generation(self):
        """Test that dev.sh script is generated with proper content."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create a project with Docker support
                inputs = [
                    '1',  # React
                    '3',  # No UI framework
                    '1',  # Vite
                    '1',  # Python
                    '2',  # PostgreSQL
                    '1',  # npm
                    'n',  # No Atlas
                    'n',  # No GitHub Actions
                    'n'   # No MCP
                ]
                
                result = runner.invoke(main, ['dev-script-test'], input='\n'.join(inputs))
                assert result.exit_code == 0
                
                project_path = Path('dev-script-test')
                
                # Check dev.sh exists
                dev_script_path = project_path / 'dev.sh'
                assert dev_script_path.exists(), "dev.sh script should be generated"
                
                # Check script is executable
                import stat
                file_stat = os.stat(str(dev_script_path))
                assert file_stat.st_mode & stat.S_IEXEC, "dev.sh should be executable"
                
                # Check script content
                script_content = dev_script_path.read_text()
                assert '#!/bin/bash' in script_content
                assert 'COMPOSE_DOCKER_CLI_BUILD=0' in script_content
                assert 'kill_port' in script_content
                assert 'docker-compose' in script_content
                assert 'Frontend: http://localhost:3001' in script_content
                assert 'Backend: http://localhost:8000' in script_content
                assert 'Database: localhost:5432' in script_content
                
            finally:
                os.chdir(original_cwd)


class TestDockerDevelopmentImprovements:
    """Test Docker development environment improvements from user feedback."""
    
    def test_generate_development_specific_dockerfile(self):
        """Test generating development-specific Dockerfile for frontend."""
        config = ProjectConfiguration(
            project_name='dev-app',
            frontend='react',
            build_tool='vite',
            package_manager='npm'
        )
        
        content = generate_frontend_dockerfile_dev(config)
        
        # Check development-specific content
        assert 'FROM node:18-alpine' in content
        assert 'WORKDIR /app' in content
        assert 'apk add --no-cache python3 make g++' in content
        assert 'COPY package*.json ./' in content
        assert 'RUN npm install' in content
        assert 'COPY . .' in content
        assert 'EXPOSE 3001' in content
        assert 'CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]' in content

    def test_generate_vite_config_with_port_3001(self):
        """Test Vite config uses port 3001 for development."""
        config = ProjectConfiguration(
            project_name='vite-3001-app',
            frontend='react',
            build_tool='vite'
        )
        
        content = generate_vite_config(config)
        
        # Check port configuration
        assert 'port: 3001' in content
        assert 'host: true' in content  # Allow external connections

    def test_generate_docker_compose_dev_with_dockerfile_dev(self):
        """Test docker-compose.dev.yml uses Dockerfile.dev."""
        config = ProjectConfiguration(
            project_name='dev-compose-app',
            frontend='react',
            backend='python',
            database='postgresql',
            build_tool='vite'
        )
        
        content = generate_docker_compose_dev(config)
        
        # Check frontend service configuration
        assert 'frontend:' in content
        assert 'dockerfile: Dockerfile.dev' in content
        assert '"3001:3001"' in content  # Port mapping
        assert 'context: ./infra/docker/frontend' in content
        assert 'volumes:' in content
        assert './frontend:/app' in content
        assert '/app/node_modules' in content
        
        # Should not have target: builder
        assert 'target: builder' not in content

    def test_generate_enhanced_dev_script(self):
        """Test enhanced dev.sh script with better port handling."""
        config = ProjectConfiguration(
            project_name='enhanced-dev-app',
            frontend='react',
            backend='python',
            database='postgresql',
            build_tool='vite'
        )
        
        content = generate_dev_script(config)
        
        # Check enhanced features
        assert 'kill_port 3001 "Frontend"' in content
        assert 'docker-compose down --volumes --remove-orphans' in content
        assert 'sleep 2' in content  # Delay for port release
        assert 'docker-compose -f docker-compose.dev.yml up --build' in content
        assert 'Frontend: http://localhost:3001' in content

    def test_complete_dev_environment_integration(self):
        """Test complete development environment with all improvements."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create a project with full stack
                inputs = [
                    '1',  # React
                    '1',  # Tailwind CSS
                    '1',  # Vite
                    '1',  # Python
                    '2',  # PostgreSQL
                    '1',  # npm
                    'n',  # No Atlas
                    'n',  # No GitHub Actions
                    'n'   # No MCP
                ]
                
                result = runner.invoke(main, ['dev-improved-app'], input='\n'.join(inputs))
                assert result.exit_code == 0
                
                project_path = Path('dev-improved-app')
                
                # Check development Dockerfile exists
                dev_dockerfile = project_path / 'infra' / 'docker' / 'frontend' / 'Dockerfile.dev'
                assert dev_dockerfile.exists(), "Development Dockerfile should exist"
                
                # Check development Dockerfile content
                dev_dockerfile_content = dev_dockerfile.read_text()
                assert 'EXPOSE 3001' in dev_dockerfile_content
                assert 'CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]' in dev_dockerfile_content
                
                # Check Vite config has port 3001
                vite_config_path = project_path / 'frontend' / 'vite.config.ts'
                if vite_config_path.exists():
                    vite_content = vite_config_path.read_text()
                    assert 'port: 3001' in vite_content
                    assert 'host: true' in vite_content
                
                # Check docker-compose.dev.yml uses Dockerfile.dev
                dev_compose = project_path / 'docker-compose.dev.yml'
                if dev_compose.exists():
                    dev_compose_content = dev_compose.read_text()
                    assert 'dockerfile: Dockerfile.dev' in dev_compose_content
                    assert '3001:3001' in dev_compose_content
                    assert 'context: ./infra/docker/frontend' in dev_compose_content
                
                # Check dev.sh script
                dev_script = project_path / 'dev.sh'
                if dev_script.exists():
                    script_content = dev_script.read_text()
                    assert 'kill_port 3001' in script_content
                    assert 'docker-compose down --volumes --remove-orphans' in script_content
                    assert 'Frontend: http://localhost:3001' in script_content
                
                # Check README mentions port 3001
                readme = project_path / 'README.md'
                if readme.exists():
                    readme_content = readme.read_text()
                    assert 'http://localhost:3001' in readme_content
                
                # Check CLAUDE.md mentions port 3001
                claude_md = project_path / 'CLAUDE.md'
                if claude_md.exists():
                    claude_content = claude_md.read_text()
                    assert '3001' in claude_content
                
            finally:
                os.chdir(original_cwd)