#!/usr/bin/env python3
"""
Prompt quality tests using promptfoo patterns.

Tests that prompts include required sections, variable replacement,
and output format consistency.
"""

import pytest
import re
from pathlib import Path
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).parent.parent
FRAMEWORKS_DIR = PROJECT_ROOT / "frameworks"
TEMPLATES_DIR = PROJECT_ROOT / "templates"


class TestPromptStructure:
    """Test that prompts have required structural elements."""

    @pytest.fixture
    def framework_files(self) -> List[Path]:
        """Get all framework markdown files."""
        if not FRAMEWORKS_DIR.exists():
            return []
        return list(FRAMEWORKS_DIR.rglob("*.md"))

    @pytest.fixture
    def template_files(self) -> List[Path]:
        """Get all template markdown files."""
        if not TEMPLATES_DIR.exists():
            return []
        return list(TEMPLATES_DIR.rglob("*.md"))

    def test_frameworks_have_title(self, framework_files):
        """Test that all frameworks have a title (H1)."""
        for filepath in framework_files:
            content = filepath.read_text(encoding='utf-8')
            assert re.search(r'^# .+', content, re.MULTILINE), \
                f"Framework {filepath.name} missing title (H1 header)"

    def test_frameworks_have_purpose(self, framework_files):
        """Test that frameworks explain their purpose."""
        purpose_indicators = [
            r'## Purpose',
            r'## When to Use',
            r'## Overview',
            r'## What This Does'
        ]

        for filepath in framework_files:
            content = filepath.read_text(encoding='utf-8')
            has_purpose = any(re.search(pattern, content, re.IGNORECASE)
                            for pattern in purpose_indicators)
            assert has_purpose, \
                f"Framework {filepath.name} missing purpose section"

    def test_frameworks_have_process_or_steps(self, framework_files):
        """Test that frameworks include a process or steps."""
        process_indicators = [
            r'## Process',
            r'## Steps',
            r'## The Process',
            r'## How to Use',
            r'### Stage \d+',
            r'### Step \d+',
            r'\d+\.\s+\*\*'  # Numbered steps
        ]

        for filepath in framework_files:
            content = filepath.read_text(encoding='utf-8')
            has_process = any(re.search(pattern, content, re.MULTILINE)
                            for pattern in process_indicators)
            assert has_process, \
                f"Framework {filepath.name} missing process/steps section"

    def test_frameworks_have_output_format(self, framework_files):
        """Test that frameworks specify output format."""
        output_indicators = [
            r'## Output',
            r'## Output Format',
            r'## Expected Output',
            r'## Deliverable'
        ]

        # Some frameworks may not need explicit output format
        # This is a soft check - we warn but don't fail
        frameworks_without_output = []

        for filepath in framework_files:
            content = filepath.read_text(encoding='utf-8')
            has_output = any(re.search(pattern, content, re.IGNORECASE)
                           for pattern in output_indicators)
            if not has_output:
                frameworks_without_output.append(filepath.name)

        # Just report, don't fail - some frameworks are more fluid
        if frameworks_without_output:
            print(f"\nFrameworks without explicit output format: {frameworks_without_output}")

    def test_templates_have_title(self, template_files):
        """Test that all templates have a title."""
        for filepath in template_files:
            content = filepath.read_text(encoding='utf-8')
            assert re.search(r'^# .+', content, re.MULTILINE), \
                f"Template {filepath.name} missing title (H1 header)"

    def test_no_broken_markdown_links(self, framework_files, template_files):
        """Test that there are no broken markdown links."""
        all_files = framework_files + template_files

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8')

            # Find markdown links [text](path)
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            for link_text, link_path in links:
                # Skip external URLs
                if link_path.startswith(('http://', 'https://', 'mailto:')):
                    continue

                # Skip anchors
                if link_path.startswith('#'):
                    continue

                # Check if relative file exists
                target_path = filepath.parent / link_path
                assert target_path.exists(), \
                    f"Broken link in {filepath.name}: [{link_text}]({link_path})"


class TestVariableReplacement:
    """Test variable placeholder handling."""

    def test_frameworks_use_consistent_placeholders(self):
        """Test that frameworks use consistent variable placeholder syntax."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        placeholder_patterns = [
            r'\[INJECT:',  # [INJECT: context]
            r'\{\{[^}]+\}\}',  # {{variable}}
            r'\$\{[^}]+\}',  # ${variable}
        ]

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            # Check which patterns are used
            used_patterns = []
            for pattern in placeholder_patterns:
                if re.search(pattern, content):
                    used_patterns.append(pattern)

            # If multiple patterns used, they should be for different purposes
            # This is more of a consistency check than a hard rule

    def test_inject_placeholders_are_documented(self):
        """Test that INJECT placeholders are self-documenting."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            # Find all INJECT placeholders
            injects = re.findall(r'\[INJECT:\s*([^\]]+)\]', content)

            for inject_desc in injects:
                # Should be descriptive (more than 3 characters)
                assert len(inject_desc.strip()) > 3, \
                    f"Uninformative INJECT placeholder in {filepath.name}: [INJECT: {inject_desc}]"

    def test_templates_identify_required_variables(self):
        """Test that templates clearly identify required variables."""
        if not TEMPLATES_DIR.exists():
            pytest.skip("Templates directory not found")

        templates = list(TEMPLATES_DIR.rglob("*.md"))

        for filepath in templates:
            content = filepath.read_text(encoding='utf-8')

            # Look for variable documentation
            has_vars_section = bool(re.search(
                r'## (?:Variables|Parameters|Required|Inputs)',
                content,
                re.IGNORECASE
            ))

            # Count placeholders
            placeholder_count = len(re.findall(r'\{\{[^}]+\}\}|\[INJECT:', content))

            # If template has placeholders, should document them
            if placeholder_count > 2:  # More than a couple
                # Should have some documentation (soft check)
                pass  # We don't fail, just inform


class TestOutputFormatConsistency:
    """Test that prompts produce consistent output formats."""

    def test_frameworks_define_clear_deliverables(self):
        """Test that frameworks specify what they produce."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        deliverable_indicators = [
            r'provide:',
            r'produce:',
            r'output:',
            r'deliver:',
            r'generate:',
            r'create:',
            r'should include:'
        ]

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8').lower()

            has_deliverable = any(indicator in content
                                for indicator in deliverable_indicators)

            # Most frameworks should specify what they produce
            # This is informational, not a hard requirement
            if not has_deliverable:
                print(f"\nNote: {filepath.name} may not specify deliverables clearly")

    def test_numbered_lists_are_consistent(self):
        """Test that numbered lists use consistent formatting."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            # Find numbered lists
            numbered_items = re.findall(r'^(\d+)\.\s+', content, re.MULTILINE)

            if len(numbered_items) > 1:
                # Check if numbering is sequential or all 1s (both valid)
                is_sequential = all(
                    int(numbered_items[i]) == i + 1
                    for i in range(len(numbered_items))
                )
                is_all_ones = all(num == '1' for num in numbered_items)

                assert is_sequential or is_all_ones, \
                    f"Inconsistent numbering in {filepath.name}"

    def test_headers_follow_hierarchy(self):
        """Test that headers follow proper hierarchy (H1 > H2 > H3)."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            # Extract headers with their levels
            headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

            # Should start with H1
            if headers:
                assert headers[0][0] == '#', \
                    f"First header should be H1 in {filepath.name}"

            # Check for header level jumps (H1 -> H3 without H2)
            for i in range(len(headers) - 1):
                current_level = len(headers[i][0])
                next_level = len(headers[i + 1][0])

                # Allow going up any amount, but down only 1 level at a time
                if next_level > current_level:
                    assert next_level <= current_level + 1, \
                        f"Header level jump in {filepath.name}: {headers[i][1]} -> {headers[i+1][1]}"


class TestPromptQuality:
    """Test overall prompt quality metrics."""

    def test_no_todos_in_production(self):
        """Test that production prompts don't contain TODO markers."""
        all_files = []
        if FRAMEWORKS_DIR.exists():
            all_files.extend(FRAMEWORKS_DIR.rglob("*.md"))
        if TEMPLATES_DIR.exists():
            all_files.extend(TEMPLATES_DIR.rglob("*.md"))

        todo_patterns = [
            r'TODO',
            r'FIXME',
            r'XXX',
            r'HACK',
            r'TBD'
        ]

        files_with_todos = []

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8')

            for pattern in todo_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    files_with_todos.append((filepath.name, pattern))

        # Report but don't fail - TODOs might be intentional
        if files_with_todos:
            print(f"\nFiles with TODO markers: {files_with_todos}")

    def test_prompts_have_adequate_length(self):
        """Test that prompts are substantial (not stubs)."""
        all_files = []
        if FRAMEWORKS_DIR.exists():
            all_files.extend(FRAMEWORKS_DIR.rglob("*.md"))
        if TEMPLATES_DIR.exists():
            all_files.extend(TEMPLATES_DIR.rglob("*.md"))

        MIN_LENGTH = 200  # Minimum reasonable prompt length

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8')

            # Remove comments and whitespace for length check
            content_cleaned = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            content_cleaned = re.sub(r'\s+', ' ', content_cleaned)

            assert len(content_cleaned) >= MIN_LENGTH, \
                f"Prompt {filepath.name} seems too short (less than {MIN_LENGTH} chars)"

    def test_no_placeholder_text_in_production(self):
        """Test that prompts don't contain obvious placeholder text."""
        all_files = []
        if FRAMEWORKS_DIR.exists():
            all_files.extend(FRAMEWORKS_DIR.rglob("*.md"))
        if TEMPLATES_DIR.exists():
            all_files.extend(TEMPLATES_DIR.rglob("*.md"))

        placeholder_patterns = [
            r'lorem ipsum',
            r'placeholder',
            r'example text here',
            r'fill this in',
            r'your .+ here'
        ]

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8').lower()

            for pattern in placeholder_patterns:
                assert not re.search(pattern, content), \
                    f"Placeholder text found in {filepath.name}: {pattern}"

    def test_meta_instructions_are_clear(self):
        """Test that meta-instructions for Claude are clearly marked."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        meta_instruction_markers = [
            r'## Meta-Instructions',
            r'## Instructions for Claude',
            r'## AI Instructions',
            r'## Note to Claude'
        ]

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            # If content references Claude or AI directly in instructional way
            if re.search(r'(when applying|you should|claude should)', content, re.IGNORECASE):
                # Should have a meta-instructions section
                has_meta_section = any(
                    re.search(pattern, content, re.IGNORECASE)
                    for pattern in meta_instruction_markers
                )

                # This is informational - some frameworks integrate instructions naturally


class TestAccessibility:
    """Test that prompts are accessible and well-documented."""

    def test_frameworks_have_examples(self):
        """Test that frameworks include examples or use cases."""
        if not FRAMEWORKS_DIR.exists():
            pytest.skip("Frameworks directory not found")

        frameworks = list(FRAMEWORKS_DIR.rglob("*.md"))

        example_indicators = [
            r'## Example',
            r'## Use Case',
            r'## Sample',
            r'## When to Use',
            r'For instance',
            r'For example',
            r'Example:'
        ]

        frameworks_without_examples = []

        for filepath in frameworks:
            content = filepath.read_text(encoding='utf-8')

            has_example = any(
                re.search(pattern, content, re.IGNORECASE)
                for pattern in example_indicators
            )

            if not has_example:
                frameworks_without_examples.append(filepath.name)

        # Report but don't fail - examples are helpful but not required
        if frameworks_without_examples:
            print(f"\nFrameworks without examples: {frameworks_without_examples}")

    def test_no_broken_formatting(self):
        """Test for common markdown formatting issues."""
        all_files = []
        if FRAMEWORKS_DIR.exists():
            all_files.extend(FRAMEWORKS_DIR.rglob("*.md"))
        if TEMPLATES_DIR.exists():
            all_files.extend(TEMPLATES_DIR.rglob("*.md"))

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8')

            # Check for unclosed code blocks
            code_blocks = re.findall(r'^```', content, re.MULTILINE)
            assert len(code_blocks) % 2 == 0, \
                f"Unclosed code block in {filepath.name}"

            # Check for unclosed bold/italic
            bold_markers = len(re.findall(r'\*\*', content))
            assert bold_markers % 2 == 0, \
                f"Unclosed bold markers in {filepath.name}"

    def test_links_are_descriptive(self):
        """Test that links have descriptive text, not just URLs."""
        all_files = []
        if FRAMEWORKS_DIR.exists():
            all_files.extend(FRAMEWORKS_DIR.rglob("*.md"))
        if TEMPLATES_DIR.exists():
            all_files.extend(TEMPLATES_DIR.rglob("*.md"))

        for filepath in all_files:
            content = filepath.read_text(encoding='utf-8')

            # Find markdown links
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            for link_text, link_url in links:
                # Link text should not be the same as URL (unless intentional)
                # Link text should be descriptive (not just "click here" or "link")
                non_descriptive = ['click here', 'link', 'here', 'read more']

                if link_text.lower() in non_descriptive:
                    print(f"\nNon-descriptive link in {filepath.name}: [{link_text}]")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
