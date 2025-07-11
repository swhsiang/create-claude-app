"""Tests for CLI module."""
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from create_claude_app.cli import main
from create_claude_app.prompts import ProjectConfiguration


class TestCLI:
    """Test CLI functionality."""

    def test_cli_requires_project_name(self):
        """Test that CLI requires a project name argument."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output

    def test_cli_accepts_project_name(self):
        """Test that CLI accepts a valid project name."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['my-test-project'])
            
            assert result.exit_code == 0
            mock_create.assert_called_once_with('my-test-project')

    def test_cli_shows_help(self):
        """Test that CLI shows help information."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "create-claude-app" in result.output
        assert "Interactive Python CLI tool" in result.output

    def test_cli_shows_version(self):
        """Test that CLI shows version information."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_handles_invalid_project_name(self):
        """Test that CLI handles invalid project names."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.side_effect = ValueError("Invalid project name")
            result = runner.invoke(main, ['invalid/project/name'])
            
            assert result.exit_code != 0
            assert "Invalid project name" in result.output

    def test_cli_handles_existing_directory(self):
        """Test that CLI handles existing directory gracefully."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.side_effect = FileExistsError("Directory already exists")
            result = runner.invoke(main, ['existing-project'])
            
            assert result.exit_code != 0
            assert "Directory already exists" in result.output


class TestCLIArguments:
    """Test CLI argument parsing and validation."""

    def test_cli_frontend_argument_valid_options(self):
        """Test CLI frontend argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['react', 'vue', 'angular', 'none']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                result = runner.invoke(main, ['test-project', '--frontend', option])
                
                assert result.exit_code == 0
                # Verify config was created with correct frontend
                args, kwargs = mock_create.call_args
                config = args[1]  # Second argument is config
                assert config.frontend == (option if option != 'none' else None)

    def test_cli_frontend_argument_invalid_option(self):
        """Test CLI frontend argument rejects invalid options."""
        runner = CliRunner()
        
        result = runner.invoke(main, ['test-project', '--frontend', 'invalid'])
        
        assert result.exit_code != 0
        assert 'Invalid value for' in result.output
        assert "'invalid' is not one of" in result.output
        assert 'react' in result.output and 'vue' in result.output

    def test_cli_backend_argument_valid_options(self):
        """Test CLI backend argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['python', 'nodejs', 'golang', 'none']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                result = runner.invoke(main, ['test-project', '--backend', option])
                
                assert result.exit_code == 0
                args, kwargs = mock_create.call_args
                config = args[1]
                assert config.backend == (option if option != 'none' else None)

    def test_cli_database_argument_valid_options(self):
        """Test CLI database argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['mysql', 'postgresql', 'sqlite', 'none']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                result = runner.invoke(main, ['test-project', '--database', option])
                
                assert result.exit_code == 0
                args, kwargs = mock_create.call_args
                config = args[1]
                assert config.database == (option if option != 'none' else None)

    def test_cli_ui_argument_valid_options(self):
        """Test CLI UI framework argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['tailwind', 'shadcn', 'none']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                # Provide frontend to avoid validation error when UI is specified
                frontend = 'react' if option == 'shadcn' else 'vue'
                result = runner.invoke(main, ['test-project', '--frontend', frontend, '--ui', option])
                
                assert result.exit_code == 0
                args, kwargs = mock_create.call_args
                config = args[1]
                assert config.ui_framework == (option if option != 'none' else None)

    def test_cli_build_tool_argument_valid_options(self):
        """Test CLI build tool argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['vite', 'webpack', 'babel']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                result = runner.invoke(main, ['test-project', '--build-tool', option])
                
                assert result.exit_code == 0
                args, kwargs = mock_create.call_args
                config = args[1]
                assert config.build_tool == option

    def test_cli_package_manager_argument_valid_options(self):
        """Test CLI package manager argument accepts valid options."""
        runner = CliRunner()
        valid_options = ['npm', 'yarn']
        
        for option in valid_options:
            with patch('create_claude_app.cli.create_project_with_config') as mock_create:
                mock_create.return_value = None
                result = runner.invoke(main, ['test-project', '--package-manager', option])
                
                assert result.exit_code == 0
                args, kwargs = mock_create.call_args
                config = args[1]
                assert config.package_manager == option

    def test_cli_boolean_flags(self):
        """Test CLI boolean flags (atlas, github-actions, mcp)."""
        runner = CliRunner()
        
        # Test atlas flag
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['test-project', '--atlas'])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            assert config.use_atlas is True

        # Test github-actions flag
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['test-project', '--github-actions'])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            assert config.use_github_actions is True

        # Test mcp flag disabled (since default is True)
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['test-project', '--no-mcp'])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            assert config.use_mcp is False

    def test_cli_short_flags(self):
        """Test CLI short flags work correctly."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, [
                'test-project', 
                '-f', 'react', 
                '-B', 'python', 
                '-d', 'postgresql',
                '-u', 'tailwind',
                '-b', 'vite',
                '-p', 'yarn',
                '-a',  # atlas
                '-g'   # github-actions
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            assert config.frontend == 'react'
            assert config.backend == 'python'
            assert config.database == 'postgresql'
            assert config.ui_framework == 'tailwind'
            assert config.build_tool == 'vite'
            assert config.package_manager == 'yarn'
            assert config.use_atlas is True
            assert config.use_github_actions is True

    def test_cli_incompatible_combination_validation(self):
        """Test CLI validates incompatible combinations."""
        runner = CliRunner()
        
        # Test Angular + shadcn/ui (incompatible)
        result = runner.invoke(main, [
            'test-project',
            '--frontend', 'angular',
            '--ui', 'shadcn'
        ])
        
        assert result.exit_code != 0
        assert 'shadcn/ui is incompatible with angular' in result.output

    def test_cli_defaults_applied_when_missing(self):
        """Test CLI applies defaults for missing arguments."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, ['test-project', '--frontend', 'react'])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            
            # Check that defaults are applied
            assert config.frontend == 'react'
            assert config.backend is None  # default: none
            assert config.database is None  # default: none
            assert config.ui_framework is None  # default: none
            assert config.build_tool == 'vite'  # default: vite
            assert config.package_manager == 'npm'  # default: npm
            assert config.use_atlas is False  # default: false
            assert config.use_github_actions is False  # default: false
            assert config.use_mcp is True  # default: true

    def test_cli_mixed_mode_with_some_args(self):
        """Test CLI mixed mode with some arguments provided."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, [
                'test-project',
                '--frontend', 'vue',
                '--database', 'mysql',
                '--github-actions'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            
            # Provided arguments
            assert config.frontend == 'vue'
            assert config.database == 'mysql'
            assert config.use_github_actions is True
            
            # Defaults for missing arguments
            assert config.backend is None
            assert config.ui_framework is None
            assert config.build_tool == 'vite'
            assert config.package_manager == 'npm'
            assert config.use_atlas is False
            assert config.use_mcp is True

    def test_cli_all_arguments_provided(self):
        """Test CLI with all arguments provided."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project_with_config') as mock_create:
            mock_create.return_value = None
            result = runner.invoke(main, [
                'full-project',
                '--frontend', 'react',
                '--ui', 'shadcn',
                '--build-tool', 'webpack',
                '--backend', 'python',
                '--database', 'postgresql',
                '--package-manager', 'yarn',
                '--atlas',
                '--github-actions',
                '--no-mcp'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_create.call_args
            config = args[1]
            
            assert config.project_name == 'full-project'
            assert config.frontend == 'react'
            assert config.ui_framework == 'shadcn'
            assert config.build_tool == 'webpack'
            assert config.backend == 'python'
            assert config.database == 'postgresql'
            assert config.package_manager == 'yarn'
            assert config.use_atlas is True
            assert config.use_github_actions is True
            assert config.use_mcp is False

    def test_cli_help_shows_all_options(self):
        """Test CLI help shows all available options."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        
        # Check that help includes all CLI arguments
        assert '--frontend' in result.output
        assert '--backend' in result.output
        assert '--database' in result.output
        assert '--ui' in result.output
        assert '--build-tool' in result.output
        assert '--package-manager' in result.output
        assert '--atlas' in result.output
        assert '--github-actions' in result.output
        assert '--mcp' in result.output
        
        # Check that some valid options are shown (flexibility for Click formatting)
        assert 'react' in result.output
        assert 'python' in result.output
        assert 'mysql' in result.output
        assert 'tailwind' in result.output
        assert 'vite' in result.output
        assert 'npm' in result.output

    def test_cli_backward_compatibility_no_args(self):
        """Test CLI maintains backward compatibility when no args provided."""
        runner = CliRunner()
        
        with patch('create_claude_app.cli.create_project') as mock_create:
            mock_create.return_value = None
            with runner.isolated_filesystem():
                result = runner.invoke(main, ['interactive-project'])
                
                assert result.exit_code == 0
                # Should call the interactive create_project function
                mock_create.assert_called_once_with('interactive-project')

    def test_cli_error_messages_for_invalid_values(self):
        """Test CLI provides clear error messages for invalid values."""
        runner = CliRunner()
        
        test_cases = [
            (['--frontend', 'invalid'], 'react', 'vue', 'angular'),
            (['--backend', 'invalid'], 'python', 'nodejs', 'golang'),
            (['--database', 'invalid'], 'mysql', 'postgresql', 'sqlite'),
            (['--ui', 'invalid'], 'tailwind', 'shadcn'),
            (['--build-tool', 'invalid'], 'vite', 'webpack', 'babel'),
            (['--package-manager', 'invalid'], 'npm', 'yarn'),
        ]
        
        for args, *valid_options in test_cases:
            result = runner.invoke(main, ['test-project'] + args)
            
            assert result.exit_code != 0
            assert 'Invalid value for' in result.output
            assert "'invalid' is not one of" in result.output
            # Check that at least one valid option is mentioned
            assert any(option in result.output for option in valid_options)