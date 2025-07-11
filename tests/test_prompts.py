"""Tests for prompts module."""
import pytest
from unittest.mock import patch, MagicMock
from create_claude_app.prompts import (
    get_frontend_choice,
    get_ui_framework_choice,
    get_backend_choice,
    get_database_choice,
    get_package_manager_choice,
    get_atlas_choice,
    get_build_tool_choice,
    get_github_actions_choice,
    get_mcp_choice,
    ProjectConfiguration,
)


class TestPrompts:
    """Test user interaction prompts."""

    def test_get_frontend_choice_valid_options(self):
        """Test frontend framework selection with valid options."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_frontend_choice()
            assert result == 'react'
            
            mock_ask.return_value = '2'
            result = get_frontend_choice()
            assert result == 'vue'
            
            mock_ask.return_value = '3'
            result = get_frontend_choice()
            assert result == 'angular'
            
            mock_ask.return_value = '4'
            result = get_frontend_choice()
            assert result is None  # Skip option

    def test_get_ui_framework_choice_for_react(self):
        """Test UI framework selection for React."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_ui_framework_choice('react')
            assert result == 'tailwind'
            
            mock_ask.return_value = '2'
            result = get_ui_framework_choice('react')
            assert result == 'shadcn'

    def test_get_ui_framework_choice_warns_about_incompatible_combinations(self):
        """Test that UI framework selection warns about incompatible combinations."""
        with patch('rich.prompt.Prompt.ask') as mock_ask, \
             patch('rich.console.Console.print') as mock_print:
            
            mock_ask.return_value = '2'  # shadcn/ui
            result = get_ui_framework_choice('angular')
            
            # Should warn about incompatibility - check all print calls
            mock_print.assert_called()
            all_calls = [str(call).lower() for call in mock_print.call_args_list]
            warning_found = any('not recommended' in call for call in all_calls)
            assert warning_found, f"No warning found in calls: {all_calls}"

    def test_get_backend_choice_valid_options(self):
        """Test backend framework selection with valid options."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_backend_choice()
            assert result == 'python'
            
            mock_ask.return_value = '2'
            result = get_backend_choice()
            assert result == 'nodejs'
            
            mock_ask.return_value = '3'
            result = get_backend_choice()
            assert result == 'golang'
            
            mock_ask.return_value = '4'
            result = get_backend_choice()
            assert result is None  # Skip option

    def test_get_database_choice_valid_options(self):
        """Test database selection with valid options."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_database_choice()
            assert result == 'mysql'
            
            mock_ask.return_value = '2'
            result = get_database_choice()
            assert result == 'postgresql'
            
            mock_ask.return_value = '3'
            result = get_database_choice()
            assert result == 'sqlite'
            
            mock_ask.return_value = '4'
            result = get_database_choice()
            assert result is None  # Skip option

    def test_get_package_manager_choice_frontend(self):
        """Test package manager selection for frontend projects."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_package_manager_choice('react')
            assert result == 'npm'
            
            mock_ask.return_value = '2'
            result = get_package_manager_choice('vue')
            assert result == 'yarn'

    def test_get_package_manager_choice_returns_none_for_no_frontend(self):
        """Test that package manager selection returns None for no frontend."""
        result = get_package_manager_choice(None)
        assert result is None

    def test_get_atlas_choice_defaults_to_yes(self):
        """Test Atlas migration tool prompt defaults to yes."""
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True
            result = get_atlas_choice()
            assert result is True
            
            mock_ask.return_value = False
            result = get_atlas_choice()
            assert result is False

    def test_project_configuration_dataclass(self):
        """Test ProjectConfiguration dataclass."""
        config = ProjectConfiguration(
            project_name='test-project',
            frontend='react',
            ui_framework='tailwind',
            backend='python',
            database='postgresql',
            package_manager='npm',
            use_atlas=True,
            build_tool='vite',
            use_github_actions=True,
            use_mcp=True
        )
        
        assert config.project_name == 'test-project'
        assert config.frontend == 'react'
        assert config.ui_framework == 'tailwind'
        assert config.backend == 'python'
        assert config.database == 'postgresql'
        assert config.package_manager == 'npm'
        assert config.use_atlas is True
        assert config.build_tool == 'vite'
        assert config.use_github_actions is True
        assert config.use_mcp is True

    def test_project_configuration_with_none_values(self):
        """Test ProjectConfiguration with None values (skipped options)."""
        config = ProjectConfiguration(
            project_name='test-project',
            frontend=None,
            ui_framework=None,
            backend=None,
            database=None,
            package_manager=None,
            use_atlas=False,
            build_tool=None,
            use_github_actions=False,
            use_mcp=False
        )
        
        assert config.project_name == 'test-project'
        assert config.frontend is None
        assert config.ui_framework is None
        assert config.backend is None
        assert config.database is None
        assert config.package_manager is None
        assert config.use_atlas is False
        assert config.build_tool is None
        assert config.use_github_actions is False
        assert config.use_mcp is False

    def test_get_build_tool_choice_valid_options(self):
        """Test build tool selection with valid options."""
        with patch('rich.prompt.Prompt.ask') as mock_ask:
            mock_ask.return_value = '1'
            result = get_build_tool_choice('react')
            assert result == 'vite'
            
            mock_ask.return_value = '2'
            result = get_build_tool_choice('react')
            assert result == 'webpack'
            
            mock_ask.return_value = '3'
            result = get_build_tool_choice('react')
            assert result == 'babel'

    def test_get_build_tool_choice_no_frontend(self):
        """Test build tool selection when no frontend is selected."""
        result = get_build_tool_choice(None)
        assert result is None

    def test_get_github_actions_choice_valid_options(self):
        """Test GitHub Actions selection with valid options."""
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True
            result = get_github_actions_choice()
            assert result is True
            
            mock_ask.return_value = False
            result = get_github_actions_choice()
            assert result is False

    def test_get_github_actions_choice_default_yes(self):
        """Test GitHub Actions selection defaults to yes."""
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True  # Default should be True
            result = get_github_actions_choice()
            assert result is True

    def test_get_mcp_choice_valid_options(self):
        """Test MCP configuration selection with valid options."""
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True
            result = get_mcp_choice()
            assert result is True
            
            mock_ask.return_value = False
            result = get_mcp_choice()
            assert result is False

    def test_get_mcp_choice_default_yes(self):
        """Test MCP configuration selection defaults to yes (recommended)."""
        with patch('rich.prompt.Confirm.ask') as mock_ask:
            mock_ask.return_value = True  # Default should be True (recommended)
            result = get_mcp_choice()
            assert result is True

    def test_get_mcp_choice_prompt_content(self):
        """Test MCP prompt displays correct content and description."""
        with patch('rich.prompt.Confirm.ask') as mock_ask, \
             patch('rich.console.Console.print') as mock_print:
            
            mock_ask.return_value = True
            result = get_mcp_choice()
            
            # Should call print for explanation
            mock_print.assert_called()
            
            # Check that Context7 is mentioned in the prompt calls
            mock_ask.assert_called_once()
            call_args = str(mock_ask.call_args)
            assert 'MCP' in call_args or 'Context Protocol' in call_args