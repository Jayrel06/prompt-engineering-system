#!/usr/bin/env python3
"""
Test suite for Prompt Doctor
Demonstrates diagnostic capabilities with example prompts
"""

import sys
from prompt_doctor import PromptDoctor, format_report


def test_prompts():
    """Test various prompt quality levels"""

    doctor = PromptDoctor(verbose=True)

    test_cases = [
        {
            "name": "Poor Prompt - Vague and Minimal",
            "prompt": "Write something about dogs."
        },
        {
            "name": "Fair Prompt - Basic but Incomplete",
            "prompt": "Create a blog post about the benefits of exercise. Make it engaging."
        },
        {
            "name": "Good Prompt - Clear with Some Details",
            "prompt": """
Generate a product description for a wireless mouse.
Target audience: Professional office workers
Length: 100-150 words
Tone: Professional but friendly
Highlight: Ergonomic design, battery life, precision
            """.strip()
        },
        {
            "name": "Excellent Prompt - Complete and Well-Structured",
            "prompt": """
Task: Generate a product description for an ergonomic wireless mouse

Context:
- Target audience: Office professionals who spend 8+ hours at desk
- Brand voice: Professional, helpful, benefit-focused
- Purpose: E-commerce product page

Format:
- 2-3 paragraphs
- Total length: 150-200 words
- Include bullet points for key features

Requirements:
- Must emphasize ergonomic benefits
- Highlight 3-year battery life
- Mention precision tracking
- Include call-to-action
- Avoid technical jargon

Example:
"Transform your workday with the ErgoGlide Pro. Designed by experts..."

Constraints:
- No hyperbolic claims
- Focus on concrete benefits
- Professional tone throughout
            """.strip()
        },
        {
            "name": "Complex Prompt - Too Many Tasks",
            "prompt": """
Write a story about a detective and also create character profiles
and additionally generate dialogue snippets and furthermore develop
a plot outline and then write chapter summaries and also create
a marketing description.
            """.strip()
        },
        {
            "name": "Ambiguous Prompt - Unclear Instructions",
            "prompt": """
Maybe write something that could possibly be a story or perhaps
an essay about things related to technology. It should be fairly
good and somewhat interesting.
            """.strip()
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'='*80}")
        print(f"\nPROMPT:\n{test_case['prompt']}")
        print()

        result = doctor.diagnose_prompt(test_case['prompt'])
        report = format_report(result, verbose=False)
        print(report)

        # Show auto-fix for poor prompts
        if result.quality_score < 60:
            print("\n" + "-"*80)
            print("AUTO-FIX SUGGESTIONS:")
            print("-"*80)
            fixed = doctor.auto_fix(test_case['prompt'], result)
            print(fixed)


if __name__ == '__main__':
    # Configure stdout for UTF-8 on Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    test_prompts()
