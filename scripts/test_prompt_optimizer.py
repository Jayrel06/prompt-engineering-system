#!/usr/bin/env python3
"""
Test Script for Prompt Optimizer

Runs basic tests to verify the optimizer is working correctly.
"""

import sys
import os

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_optimizer import (
    PromptOptimizer,
    PromptVariation,
    EvaluationCriteria,
    OptimizationTechnique,
    TestResult
)


def test_data_classes():
    """Test data class creation."""
    print("Testing data classes...")

    # Test EvaluationCriteria
    criteria = EvaluationCriteria(
        clarity=8.0,
        specificity=7.5,
        format_guidance=8.5,
        examples_quality=6.0,
        conciseness=7.0
    )

    overall = criteria.overall_score()
    assert 0 <= overall <= 10, f"Overall score out of range: {overall}"
    print(f"  [OK] EvaluationCriteria: overall_score = {overall:.2f}")

    # Test PromptVariation
    variation = PromptVariation(
        id="test123",
        content="Test prompt",
        technique_used="test",
        scores=criteria
    )

    total = variation.total_score()
    assert 0 <= total <= 10, f"Total score out of range: {total}"
    print(f"  [OK] PromptVariation: total_score = {total:.2f}")

    # Test with results
    variation.test_results = [
        TestResult("input1", "expected1", "actual1", True, 0.5),
        TestResult("input2", "expected2", "actual2", True, 0.6),
        TestResult("input3", "expected3", "actual3", False, 0.4),
    ]

    success_rate = variation.average_test_success_rate()
    assert success_rate == 2/3, f"Success rate incorrect: {success_rate}"
    print(f"  [OK] TestResult tracking: success_rate = {success_rate:.2%}")

    print("  [OK] All data classes working correctly\n")


def test_optimizer_init():
    """Test optimizer initialization."""
    print("Testing optimizer initialization...")

    try:
        # Test with Anthropic
        optimizer = PromptOptimizer(provider="anthropic")
        print(f"  [OK] Anthropic provider initialized: {optimizer.model}")

        assert optimizer.cache_dir.exists(), "Cache dir not created"
        assert optimizer.results_dir.exists(), "Results dir not created"
        print(f"  [OK] Directories created: {optimizer.results_dir}")

    except ImportError as e:
        print(f"  [WARN] Anthropic not installed: {e}")
        print("    Install with: pip install anthropic")

    try:
        # Test with OpenAI (may require API key)
        optimizer = PromptOptimizer(provider="openai")
        print(f"  [OK] OpenAI provider initialized: {optimizer.model}")

    except ImportError as e:
        print(f"  [WARN] OpenAI not installed: {e}")
        print("    Install with: pip install openai")
    except Exception as e:
        print(f"  [WARN] OpenAI requires API key: {str(e)[:60]}...")

    print()


def test_techniques():
    """Test optimization techniques enum."""
    print("Testing optimization techniques...")

    techniques = list(OptimizationTechnique)
    print(f"  Available techniques: {len(techniques)}")

    for tech in techniques:
        print(f"    - {tech.value}")

    assert len(techniques) >= 5, "Should have at least 5 techniques"
    print(f"  [OK] {len(techniques)} techniques available\n")


def test_evaluation_scoring():
    """Test evaluation scoring logic."""
    print("Testing evaluation scoring...")

    # Test perfect score
    perfect = EvaluationCriteria(
        clarity=10.0,
        specificity=10.0,
        format_guidance=10.0,
        examples_quality=10.0,
        conciseness=10.0
    )
    assert perfect.overall_score() == 10.0, "Perfect score should be 10.0"
    print("  [OK] Perfect score: 10.0")

    # Test zero score
    zero = EvaluationCriteria(0, 0, 0, 0, 0)
    assert zero.overall_score() == 0.0, "Zero score should be 0.0"
    print("  [OK] Zero score: 0.0")

    # Test weighted scoring
    weighted = EvaluationCriteria(
        clarity=8.0,  # weight: 0.25
        specificity=6.0,  # weight: 0.25
        format_guidance=7.0,  # weight: 0.20
        examples_quality=5.0,  # weight: 0.15
        conciseness=9.0  # weight: 0.15
    )
    expected = (8.0*0.25 + 6.0*0.25 + 7.0*0.20 + 5.0*0.15 + 9.0*0.15)
    actual = weighted.overall_score()
    assert abs(actual - expected) < 0.01, f"Weighted score incorrect: {actual} != {expected}"
    print(f"  [OK] Weighted scoring: {actual:.2f}")

    print()


def test_variation_generation():
    """Test variation generation (without API calls)."""
    print("Testing variation generation structure...")

    try:
        optimizer = PromptOptimizer(provider="anthropic")

        # We can't test actual generation without API calls,
        # but we can test the structure
        techniques = [
            OptimizationTechnique.MORE_SPECIFIC,
            OptimizationTechnique.MORE_CONCISE
        ]

        print(f"  [OK] Optimizer ready for generation")
        print(f"  [WARN] Actual API calls require valid API key")
        print(f"    Set ANTHROPIC_API_KEY to test full functionality")

    except ImportError as e:
        print(f"  [WARN] Cannot test: {e}")

    print()


def test_results_serialization():
    """Test results can be serialized to JSON."""
    print("Testing results serialization...")

    from prompt_optimizer import OptimizationResult
    from datetime import datetime

    # Create mock result
    variation = PromptVariation(
        id="test456",
        content="Optimized prompt",
        technique_used="more_specific",
        scores=EvaluationCriteria(8, 7, 9, 6, 7)
    )

    result = OptimizationResult(
        original="Original prompt",
        variations=[variation],
        winner=variation,
        improvement_percentage=25.5,
        timestamp=datetime.now().isoformat()
    )

    # Test serialization
    result_dict = result.to_dict()

    assert 'original' in result_dict
    assert 'variations' in result_dict
    assert 'winner' in result_dict
    assert 'improvement_percentage' in result_dict
    assert 'timestamp' in result_dict

    print("  [OK] Result serialization working")

    # Test JSON encoding
    import json
    json_str = json.dumps(result_dict, indent=2)
    assert len(json_str) > 0, "JSON serialization failed"
    print(f"  [OK] JSON encoding successful ({len(json_str)} chars)")

    # Test deserialization
    loaded = json.loads(json_str)
    assert loaded['original'] == result.original
    print("  [OK] JSON deserialization successful")

    print()


def test_file_operations():
    """Test file save/load operations."""
    print("Testing file operations...")

    try:
        from prompt_optimizer import OptimizationResult
        from datetime import datetime
        import tempfile
        import json

        optimizer = PromptOptimizer(provider="anthropic")

        # Create temporary result
        variation = PromptVariation(
            id="filetest",
            content="Test prompt",
            technique_used="test",
            scores=EvaluationCriteria(7, 8, 7, 5, 8)
        )

        result = OptimizationResult(
            original="Original",
            variations=[variation],
            winner=variation,
            improvement_percentage=15.0,
            timestamp=datetime.now().isoformat()
        )

        # Test save
        filepath = optimizer.save_results(result, filename="test_result.json")
        assert filepath.exists(), "Result file not created"
        print(f"  [OK] Save successful: {filepath.name}")

        # Test load
        loaded = optimizer.load_results("test_result.json")
        assert loaded['original'] == result.original
        assert loaded['improvement_percentage'] == result.improvement_percentage
        print(f"  [OK] Load successful")

        # Cleanup
        filepath.unlink()
        print(f"  [OK] Cleanup successful")

    except ImportError as e:
        print(f"  [WARN] Cannot test: {e}")

    print()


def test_winning_prompts():
    """Test winning prompts retrieval."""
    print("Testing winning prompts retrieval...")

    try:
        optimizer = PromptOptimizer(provider="anthropic")

        # Get winners (may be empty if no results saved)
        winners = optimizer.get_winning_prompts(
            min_score=0.0,
            limit=5
        )

        print(f"  [OK] Retrieved {len(winners)} winning prompts")

        if winners:
            print(f"    Top score: {winners[0]['score']:.2f}")
            print(f"    Top technique: {winners[0]['technique']}")

    except ImportError as e:
        print(f"  [WARN] Cannot test: {e}")

    print()


def run_all_tests():
    """Run all tests."""
    print("="*80)
    print("PROMPT OPTIMIZER TEST SUITE")
    print("="*80)
    print()

    tests = [
        test_data_classes,
        test_optimizer_init,
        test_techniques,
        test_evaluation_scoring,
        test_variation_generation,
        test_results_serialization,
        test_file_operations,
        test_winning_prompts
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("="*80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*80)

    if failed == 0:
        print("\n[OK] All tests passed!")
        print("\nTo test with API calls:")
        print("  1. Set ANTHROPIC_API_KEY environment variable")
        print("  2. Run: python prompt_optimizer.py --prompt 'test prompt'")
    else:
        print("\n[WARN] Some tests failed. Check errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
