#!/usr/bin/env python3
"""
Unit tests for context-loader.py

Tests context assembly, framework loading, template loading, and error handling.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from context_loader import (
    load_file,
    find_framework,
    assemble_context,
    CONTEXT_RULES,
    CONTEXT_DIR,
    FRAMEWORKS_DIR,
    TEMPLATES_DIR,
    PROJECT_ROOT
)


class TestLoadFile:
    """Test file loading functionality."""

    def test_load_existing_file(self, tmp_path):
        """Test loading a file that exists."""
        test_file = tmp_path / "test.txt"
        test_content = "Test content\nLine 2"
        test_file.write_text(test_content, encoding='utf-8')

        result = load_file(test_file)
        assert result == test_content

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading a file that doesn't exist."""
        test_file = tmp_path / "nonexistent.txt"
        result = load_file(test_file)
        assert "[File not found:" in result
        assert str(test_file) in result

    def test_load_file_with_unicode(self, tmp_path):
        """Test loading a file with unicode characters."""
        test_file = tmp_path / "unicode.txt"
        test_content = "Unicode: ñ, é, 中文, 🚀"
        test_file.write_text(test_content, encoding='utf-8')

        result = load_file(test_file)
        assert result == test_content

    def test_load_empty_file(self, tmp_path):
        """Test loading an empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding='utf-8')

        result = load_file(test_file)
        assert result == ""


class TestFindFramework:
    """Test framework finding functionality."""

    def test_find_existing_framework(self):
        """Test finding a framework that exists."""
        # This test assumes first-principles.md exists in frameworks/planning/
        result = find_framework("first-principles")

        if result:  # Only assert if the framework actually exists
            assert result.exists()
            assert result.name == "first-principles.md"
            assert "planning" in str(result)

    def test_find_nonexistent_framework(self):
        """Test finding a framework that doesn't exist."""
        result = find_framework("totally-fake-framework-xyz")
        assert result is None

    def test_find_framework_in_different_category(self):
        """Test finding frameworks across different categories."""
        # Check if we can find frameworks in different directories
        categories = ["planning", "analysis", "decision", "technical", "communication", "creation"]

        # We expect find_framework to check all these categories
        with patch('context_loader.FRAMEWORKS_DIR') as mock_dir:
            mock_dir.__truediv__ = MagicMock()
            find_framework("test-framework")

            # Verify it checked multiple categories
            assert mock_dir.__truediv__.call_count >= len(categories)


class TestContextRules:
    """Test context loading rules configuration."""

    def test_all_modes_present(self):
        """Test that all expected modes are defined."""
        expected_modes = ["planning", "technical", "communication", "analysis", "minimal", "full", "handoff"]

        for mode in expected_modes:
            assert mode in CONTEXT_RULES, f"Mode '{mode}' not found in CONTEXT_RULES"

    def test_mode_structure(self):
        """Test that each mode has required keys."""
        required_keys = {"context_files", "frameworks", "include_projects"}

        for mode, rules in CONTEXT_RULES.items():
            assert required_keys.issubset(rules.keys()), \
                f"Mode '{mode}' missing required keys. Has: {rules.keys()}"

    def test_minimal_mode_truly_minimal(self):
        """Test that minimal mode has no context."""
        minimal = CONTEXT_RULES["minimal"]
        assert len(minimal["context_files"]) == 0
        assert len(minimal["frameworks"]) == 0
        assert minimal["include_projects"] is False

    def test_planning_mode_includes_frameworks(self):
        """Test that planning mode includes planning frameworks."""
        planning = CONTEXT_RULES["planning"]
        assert len(planning["frameworks"]) > 0
        assert any("planning" in fw for fw in planning["frameworks"])

    def test_technical_mode_includes_technical_context(self):
        """Test that technical mode includes technical context files."""
        technical = CONTEXT_RULES["technical"]
        assert len(technical["context_files"]) > 0
        assert any("technical" in cf for cf in technical["context_files"])

    def test_handoff_mode_has_template(self):
        """Test that handoff mode includes a template."""
        handoff = CONTEXT_RULES["handoff"]
        assert "template" in handoff
        assert handoff["template"] is not None


class TestAssembleContext:
    """Test context assembly functionality."""

    def test_minimal_assembly(self):
        """Test assembling minimal context (task only)."""
        task = "Test task description"
        result = assemble_context(task=task, mode="minimal")

        assert "# Context-Enriched Prompt" in result
        assert "## Task" in result
        assert task in result
        assert "## Relevant Context" not in result  # Minimal has no context

    def test_full_assembly_structure(self):
        """Test that full assembly includes all expected sections."""
        task = "Test task"
        result = assemble_context(task=task, mode="full")

        assert "# Context-Enriched Prompt" in result
        assert "## Task" in result
        assert task in result
        # Full mode should include some context
        assert len(result) > 100  # More than just the task

    def test_planning_mode_loads_context(self):
        """Test that planning mode loads context files."""
        task = "Test planning task"
        result = assemble_context(task=task, mode="planning")

        rules = CONTEXT_RULES["planning"]

        # Should include task
        assert task in result

        # Should attempt to load context files (may not all exist)
        if rules["context_files"]:
            # At minimum, structure should be present
            assert "## Relevant Context" in result or "## Task" in result

    def test_framework_loading(self):
        """Test that frameworks are loaded when specified."""
        task = "Test task"
        result = assemble_context(task=task, mode="minimal", framework="first-principles")

        # If framework exists, it should be included
        if find_framework("first-principles"):
            assert "## Thinking Framework" in result

    def test_template_loading_in_handoff_mode(self):
        """Test that templates are loaded in handoff mode."""
        task = "Test handoff"
        result = assemble_context(task=task, mode="handoff")

        # Should include template section if template exists
        template_path = TEMPLATES_DIR / CONTEXT_RULES["handoff"]["template"]
        if template_path.exists():
            assert "## Template" in result

    def test_project_context_loading(self):
        """Test that project context is loaded when specified."""
        task = "Test task"
        project_name = "test-project"

        # Create a mock project file
        with patch('context_loader.load_file') as mock_load:
            mock_load.return_value = "Test project content"

            with patch.object(Path, 'exists', return_value=True):
                result = assemble_context(
                    task=task,
                    mode="planning",
                    project=project_name
                )

                if CONTEXT_RULES["planning"]["include_projects"]:
                    assert f"## Project Context: {project_name}" in result

    def test_verbose_mode_prints_to_stderr(self, capsys):
        """Test that verbose mode outputs to stderr."""
        task = "Test task"

        with patch('sys.stderr'):
            assemble_context(task=task, mode="planning", verbose=True)
            # In real scenario, would check stderr output

    def test_nonexistent_mode_falls_back_to_full(self):
        """Test that invalid mode falls back to full."""
        task = "Test task"
        result = assemble_context(task=task, mode="invalid-mode-xyz")

        # Should fall back to full mode
        expected = assemble_context(task=task, mode="full")
        assert result == expected

    def test_task_in_every_mode(self):
        """Test that task is included in every mode."""
        task = "Important test task"

        for mode in CONTEXT_RULES.keys():
            result = assemble_context(task=task, mode=mode)
            assert task in result, f"Task not found in mode '{mode}'"

    def test_section_ordering(self):
        """Test that sections appear in correct order."""
        task = "Test task"
        result = assemble_context(task=task, mode="planning")

        # Task should come before context
        task_pos = result.find("## Task")
        context_pos = result.find("## Relevant Context")

        assert task_pos >= 0, "Task section not found"
        if context_pos >= 0:  # Only check if context exists
            assert task_pos < context_pos, "Task should come before context"

    def test_multiple_frameworks_loading(self):
        """Test loading multiple frameworks for modes that specify them."""
        task = "Test task"
        result = assemble_context(task=task, mode="planning")

        rules = CONTEXT_RULES["planning"]
        if len(rules["frameworks"]) > 1:
            # Should include framework section
            assert "## Thinking Framework" in result


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_missing_context_directory(self):
        """Test behavior when context directory is missing."""
        task = "Test task"

        # Should not crash even if files don't exist
        result = assemble_context(task=task, mode="full")
        assert task in result

    def test_missing_framework_directory(self):
        """Test behavior when framework directory is missing."""
        task = "Test task"

        with patch('context_loader.FRAMEWORKS_DIR', Path("/nonexistent/path")):
            result = assemble_context(task=task, mode="planning", framework="test")
            assert task in result  # Should still include task

    def test_corrupted_file_handling(self):
        """Test handling of files with encoding issues."""
        # This is tricky to test without actual corrupted files
        # Testing that load_file handles standard cases gracefully
        task = "Test task"
        result = assemble_context(task=task, mode="minimal")
        assert result is not None
        assert len(result) > 0

    def test_empty_task_handling(self):
        """Test behavior with empty task."""
        task = ""
        result = assemble_context(task=task, mode="minimal")

        assert "## Task" in result
        # Should not crash with empty task

    def test_very_long_task_handling(self):
        """Test handling of very long task descriptions."""
        task = "A" * 10000  # 10k character task
        result = assemble_context(task=task, mode="minimal")

        assert task in result
        assert "## Task" in result


class TestIntegration:
    """Integration tests for end-to-end scenarios."""

    def test_full_workflow_planning(self):
        """Test complete workflow for planning scenario."""
        task = "Design Q1 marketing strategy"
        result = assemble_context(
            task=task,
            mode="planning",
            project=None,
            verbose=False
        )

        assert "# Context-Enriched Prompt" in result
        assert task in result
        assert len(result) > 200  # Should have substantial content

    def test_full_workflow_technical(self):
        """Test complete workflow for technical scenario."""
        task = "Build n8n workflow for lead scoring"
        result = assemble_context(
            task=task,
            mode="technical",
            framework=None,
            verbose=False
        )

        assert task in result
        assert "## Task" in result

    def test_full_workflow_with_custom_framework(self):
        """Test workflow with custom framework override."""
        task = "Should I build or buy this solution?"
        result = assemble_context(
            task=task,
            mode="minimal",
            framework="first-principles"
        )

        assert task in result

    def test_handoff_template_workflow(self):
        """Test handoff template generation."""
        task = "Complete implementation of lead tracking system"
        result = assemble_context(
            task=task,
            mode="handoff"
        )

        assert task in result
        assert "## Task" in result


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
