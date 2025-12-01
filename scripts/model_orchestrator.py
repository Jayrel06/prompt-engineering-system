#!/usr/bin/env python3
"""
Multi-Model Orchestration System

Intelligently routes prompts to the most appropriate LLM based on task complexity,
implements fallback chains, ensemble responses, and cost optimization.

Usage:
    model_orchestrator.py --prompt "Your prompt here" --strategy fallback
    model_orchestrator.py --prompt "Your prompt here" --strategy ensemble --max-cost 0.01
    model_orchestrator.py --prompt "Your prompt here" --strategy cheapest
    model_orchestrator.py --test  # Run test suite

Examples:
    # Fallback chain: Try Haiku, escalate to Sonnet if uncertain
    model_orchestrator.py --prompt "Explain quantum computing" --strategy fallback

    # Ensemble: Run on 3 models, synthesize best response
    model_orchestrator.py --prompt "Should I use REST or GraphQL?" --strategy ensemble --ensemble-size 3

    # Auto-route to cheapest model that can handle complexity
    model_orchestrator.py --prompt "What is 2+2?" --strategy cheapest

    # Set maximum cost budget
    model_orchestrator.py --prompt "Complex analysis task" --strategy fallback --max-cost 0.005
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib

# Import cost tracker for integration
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from cost_tracker import log_usage, calculate_cost, normalize_model_name
except ImportError:
    print("Warning: cost_tracker not found. Cost tracking will be limited.", file=sys.stderr)

    def log_usage(*args, **kwargs):
        pass

    def calculate_cost(model: str, input_tokens: int, output_tokens: int):
        return (Decimal("0"), Decimal("0"), Decimal("0"))

    def normalize_model_name(model: str):
        return model


# ============================================================================
# Configuration and Models
# ============================================================================

class ModelProvider(Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class ModelCapability(Enum):
    """Model capability categories."""
    BASIC = "basic"              # Simple Q&A, formatting
    INTERMEDIATE = "intermediate"  # Reasoning, code review
    ADVANCED = "advanced"         # Complex reasoning, architecture
    EXPERT = "expert"             # Research, multi-step analysis


@dataclass
class ModelConfig:
    """Configuration for a single model."""
    name: str
    provider: ModelProvider
    cost_per_1k_input_tokens: Decimal  # Cost in dollars
    cost_per_1k_output_tokens: Decimal
    max_tokens: int
    capabilities: List[ModelCapability]
    context_window: int
    supports_streaming: bool = True
    rate_limit_rpm: int = 50  # Requests per minute

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> Decimal:
        """Calculate cost for token usage."""
        input_cost = (Decimal(input_tokens) / Decimal(1000)) * self.cost_per_1k_input_tokens
        output_cost = (Decimal(output_tokens) / Decimal(1000)) * self.cost_per_1k_output_tokens
        return input_cost + output_cost

    def can_handle(self, capability: ModelCapability) -> bool:
        """Check if model can handle given capability level."""
        capability_order = [ModelCapability.BASIC, ModelCapability.INTERMEDIATE,
                          ModelCapability.ADVANCED, ModelCapability.EXPERT]
        model_level = max(capability_order.index(c) for c in self.capabilities)
        required_level = capability_order.index(capability)
        return model_level >= required_level


@dataclass
class OrchestrationResult:
    """Result of model orchestration."""
    response: str
    model_used: str
    cost: Decimal
    latency: float  # seconds
    confidence: float  # 0.0 to 1.0
    input_tokens: int
    output_tokens: int
    strategy: str
    fallback_chain: List[str] = field(default_factory=list)
    ensemble_models: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['cost'] = float(self.cost)
        return data


# Model Registry
MODEL_REGISTRY: Dict[str, ModelConfig] = {
    # Anthropic Models
    "claude-haiku-3.5": ModelConfig(
        name="claude-haiku-3.5",
        provider=ModelProvider.ANTHROPIC,
        cost_per_1k_input_tokens=Decimal("0.00080"),
        cost_per_1k_output_tokens=Decimal("0.00400"),
        max_tokens=8192,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE],
        context_window=200000,
        rate_limit_rpm=100
    ),
    "claude-sonnet-3.5": ModelConfig(
        name="claude-sonnet-3.5",
        provider=ModelProvider.ANTHROPIC,
        cost_per_1k_input_tokens=Decimal("0.00300"),
        cost_per_1k_output_tokens=Decimal("0.01500"),
        max_tokens=8192,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE, ModelCapability.ADVANCED],
        context_window=200000,
        rate_limit_rpm=50
    ),
    "claude-opus-3": ModelConfig(
        name="claude-opus-3",
        provider=ModelProvider.ANTHROPIC,
        cost_per_1k_input_tokens=Decimal("0.01500"),
        cost_per_1k_output_tokens=Decimal("0.07500"),
        max_tokens=4096,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE,
                     ModelCapability.ADVANCED, ModelCapability.EXPERT],
        context_window=200000,
        rate_limit_rpm=20
    ),

    # OpenAI Models
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        provider=ModelProvider.OPENAI,
        cost_per_1k_input_tokens=Decimal("0.00015"),
        cost_per_1k_output_tokens=Decimal("0.00060"),
        max_tokens=16384,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE],
        context_window=128000,
        rate_limit_rpm=100
    ),
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        provider=ModelProvider.OPENAI,
        cost_per_1k_input_tokens=Decimal("0.00250"),
        cost_per_1k_output_tokens=Decimal("0.01000"),
        max_tokens=16384,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE, ModelCapability.ADVANCED],
        context_window=128000,
        rate_limit_rpm=50
    ),
    "gpt-4": ModelConfig(
        name="gpt-4",
        provider=ModelProvider.OPENAI,
        cost_per_1k_input_tokens=Decimal("0.03000"),
        cost_per_1k_output_tokens=Decimal("0.06000"),
        max_tokens=8192,
        capabilities=[ModelCapability.BASIC, ModelCapability.INTERMEDIATE,
                     ModelCapability.ADVANCED, ModelCapability.EXPERT],
        context_window=128000,
        rate_limit_rpm=20
    ),
}


# Default fallback chains
FALLBACK_CHAINS = {
    "anthropic": ["claude-haiku-3.5", "claude-sonnet-3.5", "claude-opus-3"],
    "openai": ["gpt-4o-mini", "gpt-4o", "gpt-4"],
    "mixed": ["gpt-4o-mini", "claude-haiku-3.5", "claude-sonnet-3.5", "gpt-4o", "claude-opus-3"],
    "fast": ["claude-haiku-3.5", "gpt-4o-mini", "claude-sonnet-3.5"],
}

# Model name mappings for cost_tracker compatibility
COST_TRACKER_MODEL_MAP = {
    "claude-haiku-3.5": "claude-haiku-3",
    "claude-sonnet-3.5": "claude-sonnet-3.5",
    "claude-opus-3": "claude-sonnet-3.5",  # Fallback to Sonnet pricing for Opus
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4o": "gpt-4o",
    "gpt-4": "gpt-4o",  # Fallback to gpt-4o pricing
}


def log_orchestration_usage(model_name: str, input_tokens: int, output_tokens: int,
                            strategy: str, metadata: Dict = None):
    """Log usage with model name mapping for cost_tracker compatibility."""
    mapped_model = COST_TRACKER_MODEL_MAP.get(model_name, model_name)
    try:
        log_usage(
            model=mapped_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            category="orchestration",
            description=f"{strategy.capitalize()} strategy execution",
            metadata=metadata or {}
        )
    except Exception as e:
        print(f"Warning: Failed to log usage: {e}", file=sys.stderr)


# ============================================================================
# Complexity Scoring
# ============================================================================

class ComplexityAnalyzer:
    """Analyze prompt complexity to determine minimum required model."""

    # Patterns that indicate different complexity levels
    COMPLEXITY_INDICATORS = {
        ModelCapability.EXPERT: [
            r'\b(research|analyze deeply|comprehensive|multi-step|architecture)\b',
            r'\b(compare multiple|evaluate tradeoffs|design system)\b',
            r'\b(prove|derive|formalize|rigorous)\b',
            r'\b(phd|academic|scientific|peer-reviewed)\b',
        ],
        ModelCapability.ADVANCED: [
            r'\b(explain why|reasoning|justify|analyze)\b',
            r'\b(implement|build|create|design)\b',
            r'\b(optimize|refactor|improve)\b',
            r'\b(debug|troubleshoot|diagnose)\b',
            r'\b(compare|contrast|evaluate)\b',
        ],
        ModelCapability.INTERMEDIATE: [
            r'\b(write code|function|class|script)\b',
            r'\b(summarize|explain|describe)\b',
            r'\b(list|enumerate|identify)\b',
            r'\b(calculate|solve|compute)\b',
        ],
        ModelCapability.BASIC: [
            r'\b(what is|define|meaning)\b',
            r'\b(format|convert|translate)\b',
            r'\b(simple|basic|quick)\b',
        ],
    }

    @classmethod
    def score_complexity(cls, prompt: str) -> Tuple[ModelCapability, float]:
        """
        Score prompt complexity and return required capability level.

        Returns:
            Tuple of (required_capability, confidence_score)
        """
        prompt_lower = prompt.lower()

        # Calculate scores for each level
        scores = {}
        for capability, patterns in cls.COMPLEXITY_INDICATORS.items():
            matches = sum(1 for p in patterns if re.search(p, prompt_lower))
            scores[capability] = matches / len(patterns) if patterns else 0

        # Length-based adjustments
        word_count = len(prompt.split())
        if word_count > 200:
            scores[ModelCapability.ADVANCED] += 0.2
        elif word_count > 100:
            scores[ModelCapability.INTERMEDIATE] += 0.1

        # Multi-part questions
        question_marks = prompt.count('?')
        if question_marks > 2:
            scores[ModelCapability.ADVANCED] += 0.15

        # Code detection
        if '```' in prompt or re.search(r'\b(python|javascript|java|rust|go)\b', prompt_lower):
            scores[ModelCapability.ADVANCED] = max(scores.get(ModelCapability.ADVANCED, 0), 0.3)

        # Get the highest scoring capability
        if not scores or max(scores.values()) < 0.1:
            # Default to basic for unclear prompts
            return ModelCapability.BASIC, 0.5

        best_capability = max(scores, key=scores.get)
        confidence = min(scores[best_capability] * 1.5, 1.0)

        return best_capability, confidence


# ============================================================================
# Confidence Detection
# ============================================================================

class ConfidenceDetector:
    """Detect confidence level in model responses."""

    LOW_CONFIDENCE_PATTERNS = [
        r'\b(not sure|uncertain|unclear|might be|possibly|perhaps|maybe)\b',
        r'\b(I think|I believe|seems like|appears to|could be)\b',
        r'\b(limited information|need more context|would need to)\b',
        r'\b(disclaimer|caveat|however|but)\b',
        r'\b(may not|might not|unsure|don\'t know)\b',
    ]

    HIGH_CONFIDENCE_PATTERNS = [
        r'\b(definitely|certainly|clearly|obviously|undoubtedly)\b',
        r'\b(proven|established|confirmed|verified)\b',
        r'\b(always|never|must|will)\b',
        r'\b(conclusive|definitive|absolute)\b',
    ]

    @classmethod
    def detect_confidence(cls, response: str) -> float:
        """
        Detect confidence level in response.

        Returns:
            Confidence score from 0.0 to 1.0
        """
        response_lower = response.lower()

        # Count pattern matches
        low_matches = sum(1 for p in cls.LOW_CONFIDENCE_PATTERNS
                         if re.search(p, response_lower))
        high_matches = sum(1 for p in cls.HIGH_CONFIDENCE_PATTERNS
                          if re.search(p, response_lower))

        # Length penalty - very short responses are suspicious
        word_count = len(response.split())
        if word_count < 20:
            length_penalty = 0.2
        elif word_count < 50:
            length_penalty = 0.1
        else:
            length_penalty = 0

        # Calculate confidence
        base_confidence = 0.7  # Neutral starting point
        confidence = base_confidence + (high_matches * 0.05) - (low_matches * 0.1) - length_penalty

        # Clamp to valid range
        return max(0.1, min(1.0, confidence))


# ============================================================================
# Rate Limiting
# ============================================================================

class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self):
        self.call_times: Dict[str, List[float]] = {}

    def can_call(self, model_name: str) -> bool:
        """Check if we can make a call to this model."""
        model = MODEL_REGISTRY.get(model_name)
        if not model:
            return True

        now = time.time()
        if model_name not in self.call_times:
            self.call_times[model_name] = []

        # Remove calls older than 1 minute
        self.call_times[model_name] = [
            t for t in self.call_times[model_name]
            if now - t < 60
        ]

        # Check if under rate limit
        return len(self.call_times[model_name]) < model.rate_limit_rpm

    def register_call(self, model_name: str):
        """Register a call to this model."""
        if model_name not in self.call_times:
            self.call_times[model_name] = []
        self.call_times[model_name].append(time.time())

    def wait_if_needed(self, model_name: str, max_wait: float = 60.0):
        """Wait if necessary to respect rate limits."""
        model = MODEL_REGISTRY.get(model_name)
        if not model:
            return

        waited = 0
        while not self.can_call(model_name) and waited < max_wait:
            time.sleep(1)
            waited += 1


# Global rate limiter
RATE_LIMITER = RateLimiter()


# ============================================================================
# Mock LLM Interface (for demonstration)
# ============================================================================

class MockLLMClient:
    """
    Mock LLM client for demonstration purposes.

    In production, replace with actual API calls to Anthropic/OpenAI.
    """

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough token estimation (1 token ~= 4 characters)."""
        return len(text) // 4

    @classmethod
    def call_model(cls, model_name: str, prompt: str, max_retries: int = 3) -> Tuple[str, int, int]:
        """
        Mock model call. In production, implement actual API calls.

        Returns:
            Tuple of (response, input_tokens, output_tokens)
        """
        model = MODEL_REGISTRY.get(model_name)
        if not model:
            raise ValueError(f"Unknown model: {model_name}")

        # Simulate rate limiting
        RATE_LIMITER.wait_if_needed(model_name, max_wait=30)
        RATE_LIMITER.register_call(model_name)

        # Estimate tokens
        input_tokens = cls.estimate_tokens(prompt)

        # Simulate processing time
        time.sleep(0.1 + (0.05 * len(model.capabilities)))

        # Generate mock response based on model capability
        responses = {
            ModelCapability.BASIC: "Here's a concise answer based on my understanding.",
            ModelCapability.INTERMEDIATE: "Let me explain this step by step. First, we need to consider the context. Then, we can analyze the key factors.",
            ModelCapability.ADVANCED: "This is a complex question that requires careful analysis. Let me break it down: 1) Context and background, 2) Key considerations, 3) Trade-offs, 4) Recommendations with justification.",
            ModelCapability.EXPERT: "This requires comprehensive analysis. I'll provide: 1) Theoretical foundation, 2) Empirical evidence, 3) Multiple perspectives, 4) Synthesis and implications, 5) Future directions.",
        }

        max_capability = max(model.capabilities,
                           key=lambda c: [ModelCapability.BASIC, ModelCapability.INTERMEDIATE,
                                        ModelCapability.ADVANCED, ModelCapability.EXPERT].index(c))

        response = f"[{model_name}] {responses[max_capability]}\n\nPrompt received: {prompt[:100]}..."
        output_tokens = cls.estimate_tokens(response)

        return response, input_tokens, output_tokens


# ============================================================================
# Orchestration Strategies
# ============================================================================

def route_to_model(prompt: str, max_cost: Optional[Decimal] = None) -> str:
    """
    Route prompt to the cheapest model that can handle the complexity.

    Args:
        prompt: The prompt to analyze
        max_cost: Maximum cost budget (optional)

    Returns:
        Selected model name
    """
    # Analyze complexity
    required_capability, confidence = ComplexityAnalyzer.score_complexity(prompt)

    # Filter models that can handle this capability
    capable_models = [
        (name, model) for name, model in MODEL_REGISTRY.items()
        if model.can_handle(required_capability)
    ]

    if not capable_models:
        raise ValueError(f"No model found for capability: {required_capability}")

    # Sort by cost (input + output cost average)
    capable_models.sort(key=lambda x: x[1].cost_per_1k_input_tokens + x[1].cost_per_1k_output_tokens)

    # Apply cost constraint if specified
    if max_cost:
        estimated_tokens = MockLLMClient.estimate_tokens(prompt)
        estimated_output = estimated_tokens  # Assume similar output size

        for name, model in capable_models:
            estimated_cost = model.calculate_cost(estimated_tokens, estimated_output)
            if estimated_cost <= max_cost:
                return name

        raise ValueError(f"No model found within budget: ${max_cost}")

    return capable_models[0][0]


def run_with_fallback(
    prompt: str,
    chain: Optional[List[str]] = None,
    confidence_threshold: float = 0.6,
    max_cost: Optional[Decimal] = None
) -> OrchestrationResult:
    """
    Run prompt with fallback chain.

    Try models in sequence, escalating to more capable models if confidence is low.

    Args:
        prompt: The prompt to run
        chain: Ordered list of model names (cheapest to most capable)
        confidence_threshold: Minimum confidence to accept response
        max_cost: Maximum total cost budget

    Returns:
        OrchestrationResult with final response
    """
    if chain is None:
        chain = FALLBACK_CHAINS["mixed"]

    total_cost = Decimal("0")
    fallback_history = []

    for i, model_name in enumerate(chain):
        if model_name not in MODEL_REGISTRY:
            print(f"Warning: Unknown model {model_name}, skipping", file=sys.stderr)
            continue

        model = MODEL_REGISTRY[model_name]
        fallback_history.append(model_name)

        # Check cost budget
        if max_cost and total_cost >= max_cost:
            raise ValueError(f"Cost budget exceeded: ${total_cost} >= ${max_cost}")

        try:
            start_time = time.time()
            response, input_tokens, output_tokens = MockLLMClient.call_model(model_name, prompt)
            latency = time.time() - start_time

            # Calculate cost
            cost = model.calculate_cost(input_tokens, output_tokens)
            total_cost += cost

            # Detect confidence
            confidence = ConfidenceDetector.detect_confidence(response)

            # Log usage
            try:
                log_usage(
                    model=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    category="orchestration",
                    description="Fallback chain execution",
                    metadata={"strategy": "fallback", "position": i}
                )
            except Exception as e:
                print(f"Warning: Failed to log usage: {e}", file=sys.stderr)

            # Check if we should accept this response
            is_last_model = (i == len(chain) - 1)
            if confidence >= confidence_threshold or is_last_model:
                return OrchestrationResult(
                    response=response,
                    model_used=model_name,
                    cost=total_cost,
                    latency=latency,
                    confidence=confidence,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    strategy="fallback",
                    fallback_chain=fallback_history,
                    metadata={
                        "attempts": i + 1,
                        "confidence_threshold": confidence_threshold
                    }
                )

            # Low confidence, try next model
            print(f"Low confidence ({confidence:.2f}) from {model_name}, trying next model...",
                  file=sys.stderr)

        except Exception as e:
            print(f"Error with model {model_name}: {e}", file=sys.stderr)
            if i == len(chain) - 1:
                raise
            continue

    raise ValueError("All models in fallback chain failed")


def run_ensemble(
    prompt: str,
    models: Optional[List[str]] = None,
    ensemble_size: int = 3,
    max_cost: Optional[Decimal] = None
) -> OrchestrationResult:
    """
    Run prompt on multiple models and synthesize the best response.

    Args:
        prompt: The prompt to run
        models: List of model names to use (or None for auto-select)
        ensemble_size: Number of models to use
        max_cost: Maximum total cost budget

    Returns:
        OrchestrationResult with synthesized response
    """
    if models is None:
        # Auto-select diverse models
        models = ["claude-haiku-3.5", "gpt-4o-mini", "claude-sonnet-3.5"][:ensemble_size]
    else:
        models = models[:ensemble_size]

    responses = []
    total_cost = Decimal("0")
    total_latency = 0.0
    total_input_tokens = 0
    total_output_tokens = 0

    # Run on each model
    for model_name in models:
        if model_name not in MODEL_REGISTRY:
            print(f"Warning: Unknown model {model_name}, skipping", file=sys.stderr)
            continue

        model = MODEL_REGISTRY[model_name]

        # Check cost budget
        if max_cost and total_cost >= max_cost:
            print(f"Warning: Cost budget reached, stopping ensemble at {len(responses)} models",
                  file=sys.stderr)
            break

        try:
            start_time = time.time()
            response, input_tokens, output_tokens = MockLLMClient.call_model(model_name, prompt)
            latency = time.time() - start_time

            cost = model.calculate_cost(input_tokens, output_tokens)
            confidence = ConfidenceDetector.detect_confidence(response)

            responses.append({
                'model': model_name,
                'response': response,
                'confidence': confidence,
                'cost': cost,
                'latency': latency,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens
            })

            total_cost += cost
            total_latency += latency
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens

            # Log usage
            try:
                log_usage(
                    model=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    category="orchestration",
                    description="Ensemble execution",
                    metadata={"strategy": "ensemble"}
                )
            except Exception as e:
                print(f"Warning: Failed to log usage: {e}", file=sys.stderr)

        except Exception as e:
            print(f"Error with model {model_name}: {e}", file=sys.stderr)
            continue

    if not responses:
        raise ValueError("No models produced responses")

    # Synthesize responses
    synthesized = synthesize_responses(responses)

    return OrchestrationResult(
        response=synthesized['response'],
        model_used=synthesized['best_model'],
        cost=total_cost,
        latency=total_latency / len(responses),  # Average latency
        confidence=synthesized['confidence'],
        input_tokens=total_input_tokens,
        output_tokens=total_output_tokens,
        strategy="ensemble",
        ensemble_models=[r['model'] for r in responses],
        metadata={
            'ensemble_size': len(responses),
            'all_confidences': [r['confidence'] for r in responses]
        }
    )


def synthesize_responses(responses: List[Dict]) -> Dict:
    """
    Synthesize multiple model responses into a single best response.

    Uses a combination of confidence scoring and consensus detection.

    Args:
        responses: List of response dictionaries

    Returns:
        Dict with synthesized response and metadata
    """
    if not responses:
        raise ValueError("No responses to synthesize")

    if len(responses) == 1:
        return {
            'response': responses[0]['response'],
            'best_model': responses[0]['model'],
            'confidence': responses[0]['confidence'],
            'method': 'single'
        }

    # Score each response
    scores = []
    for r in responses:
        # Factors: confidence, response length, model capability
        model = MODEL_REGISTRY[r['model']]
        capability_score = len(model.capabilities) / 4.0  # Normalize to 0-1
        length_score = min(len(r['response'].split()) / 200.0, 1.0)

        score = (r['confidence'] * 0.5) + (capability_score * 0.3) + (length_score * 0.2)
        scores.append(score)

    # Select best response
    best_idx = scores.index(max(scores))
    best_response = responses[best_idx]

    # Check for consensus (similar key points across responses)
    consensus_boost = 0.0
    best_text_lower = best_response['response'].lower()
    for other in responses:
        if other is best_response:
            continue
        # Simple overlap check - in production, use semantic similarity
        other_text_lower = other['response'].lower()
        common_words = set(best_text_lower.split()) & set(other_text_lower.split())
        if len(common_words) > 20:  # Arbitrary threshold
            consensus_boost += 0.05

    final_confidence = min(best_response['confidence'] + consensus_boost, 1.0)

    # Create synthesis note
    synthesis_note = f"\n\n--- Ensemble Synthesis ---\n"
    synthesis_note += f"Selected best response from {best_response['model']} "
    synthesis_note += f"(confidence: {final_confidence:.2f})\n"
    synthesis_note += f"Considered {len(responses)} model responses\n"

    return {
        'response': best_response['response'] + synthesis_note,
        'best_model': best_response['model'],
        'confidence': final_confidence,
        'method': 'scored_selection',
        'scores': scores
    }


# ============================================================================
# Main CLI
# ============================================================================

def run_orchestration(
    prompt: str,
    strategy: str = "fallback",
    max_cost: Optional[float] = None,
    chain: Optional[List[str]] = None,
    ensemble_size: int = 3,
    verbose: bool = False
) -> OrchestrationResult:
    """
    Main orchestration function.

    Args:
        prompt: The prompt to run
        strategy: "fallback", "ensemble", or "cheapest"
        max_cost: Maximum cost budget in dollars
        chain: Custom fallback chain (for fallback strategy)
        ensemble_size: Number of models for ensemble
        verbose: Print detailed progress

    Returns:
        OrchestrationResult
    """
    max_cost_decimal = Decimal(str(max_cost)) if max_cost else None

    if verbose:
        print(f"Strategy: {strategy}", file=sys.stderr)
        print(f"Max cost: ${max_cost}" if max_cost else "Max cost: unlimited", file=sys.stderr)
        print(f"Prompt: {prompt[:100]}...\n", file=sys.stderr)

    if strategy == "cheapest":
        model_name = route_to_model(prompt, max_cost_decimal)
        if verbose:
            print(f"Selected model: {model_name}", file=sys.stderr)

        start_time = time.time()
        response, input_tokens, output_tokens = MockLLMClient.call_model(model_name, prompt)
        latency = time.time() - start_time

        model = MODEL_REGISTRY[model_name]
        cost = model.calculate_cost(input_tokens, output_tokens)
        confidence = ConfidenceDetector.detect_confidence(response)

        # Log usage
        try:
            log_usage(
                model=model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                category="orchestration",
                description="Cheapest model routing"
            )
        except Exception:
            pass

        return OrchestrationResult(
            response=response,
            model_used=model_name,
            cost=cost,
            latency=latency,
            confidence=confidence,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            strategy="cheapest"
        )

    elif strategy == "fallback":
        return run_with_fallback(prompt, chain, max_cost=max_cost_decimal)

    elif strategy == "ensemble":
        return run_ensemble(prompt, ensemble_size=ensemble_size, max_cost=max_cost_decimal)

    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def print_result(result: OrchestrationResult, verbose: bool = False):
    """Print orchestration result in a readable format."""
    print("\n" + "=" * 80)
    print("ORCHESTRATION RESULT")
    print("=" * 80)

    print(f"\nStrategy: {result.strategy}")
    print(f"Model Used: {result.model_used}")
    print(f"Cost: ${result.cost:.6f}")
    print(f"Latency: {result.latency:.2f}s")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Tokens: {result.input_tokens} input + {result.output_tokens} output")

    if result.fallback_chain:
        print(f"Fallback Chain: {' -> '.join(result.fallback_chain)}")

    if result.ensemble_models:
        print(f"Ensemble Models: {', '.join(result.ensemble_models)}")

    if verbose and result.metadata:
        print(f"\nMetadata: {json.dumps(result.metadata, indent=2)}")

    print("\n" + "-" * 80)
    print("RESPONSE")
    print("-" * 80)
    print(result.response)
    print("\n" + "=" * 80 + "\n")


def run_tests():
    """Run test suite to verify orchestration system."""
    print("Running Model Orchestrator Tests...\n")

    test_prompts = [
        ("What is 2+2?", "cheapest", ModelCapability.BASIC),
        ("Explain how neural networks work", "cheapest", ModelCapability.INTERMEDIATE),
        ("Design a distributed system architecture for a high-traffic e-commerce platform",
         "cheapest", ModelCapability.ADVANCED),
        ("Conduct a comprehensive analysis of quantum computing implications for cryptography",
         "cheapest", ModelCapability.EXPERT),
    ]

    print("=" * 80)
    print("TEST 1: Complexity Scoring")
    print("=" * 80)
    for prompt, _, expected in test_prompts:
        capability, confidence = ComplexityAnalyzer.score_complexity(prompt)
        status = "[PASS]" if capability == expected else "[FAIL]"
        print(f"{status} '{prompt[:60]}...'")
        print(f"  Expected: {expected.value}, Got: {capability.value}, Confidence: {confidence:.2f}\n")

    print("=" * 80)
    print("TEST 2: Model Routing")
    print("=" * 80)
    for prompt, strategy, _ in test_prompts:
        try:
            model = route_to_model(prompt)
            print(f"[PASS] '{prompt[:60]}...'")
            print(f"  Routed to: {model}\n")
        except Exception as e:
            print(f"[FAIL] Error: {e}\n")

    print("=" * 80)
    print("TEST 3: Fallback Chain")
    print("=" * 80)
    test_prompt = "Explain quantum entanglement"
    try:
        result = run_with_fallback(test_prompt, chain=["claude-haiku-3.5", "claude-sonnet-3.5"])
        print(f"[PASS] Fallback test completed")
        print(f"  Final model: {result.model_used}")
        print(f"  Cost: ${result.cost:.6f}")
        print(f"  Confidence: {result.confidence:.2f}\n")
    except Exception as e:
        print(f"[FAIL] Error: {e}\n")

    print("=" * 80)
    print("TEST 4: Ensemble")
    print("=" * 80)
    try:
        result = run_ensemble(test_prompt, ensemble_size=2)
        print(f"[PASS] Ensemble test completed")
        print(f"  Models used: {', '.join(result.ensemble_models)}")
        print(f"  Best model: {result.model_used}")
        print(f"  Total cost: ${result.cost:.6f}")
        print(f"  Confidence: {result.confidence:.2f}\n")
    except Exception as e:
        print(f"[FAIL] Error: {e}\n")

    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Model Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--prompt", "-p",
        help="Prompt to run (required unless --test)"
    )

    parser.add_argument(
        "--strategy", "-s",
        choices=["fallback", "ensemble", "cheapest"],
        default="fallback",
        help="Orchestration strategy (default: fallback)"
    )

    parser.add_argument(
        "--max-cost", "-c",
        type=float,
        help="Maximum cost budget in dollars"
    )

    parser.add_argument(
        "--chain",
        help="Custom fallback chain (comma-separated model names)"
    )

    parser.add_argument(
        "--ensemble-size", "-e",
        type=int,
        default=3,
        help="Number of models for ensemble strategy (default: 3)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test suite"
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file for JSON result"
    )

    args = parser.parse_args()

    # List models
    if args.list_models:
        print("\nAvailable Models:")
        print("=" * 80)
        for name, model in sorted(MODEL_REGISTRY.items()):
            print(f"\n{name}")
            print(f"  Provider: {model.provider.value}")
            print(f"  Input: ${model.cost_per_1k_input_tokens}/1K tokens")
            print(f"  Output: ${model.cost_per_1k_output_tokens}/1K tokens")
            print(f"  Capabilities: {', '.join(c.value for c in model.capabilities)}")
            print(f"  Context: {model.context_window:,} tokens")
        print("\n" + "=" * 80)
        return

    # Run tests
    if args.test:
        run_tests()
        return

    # Require prompt
    if not args.prompt:
        parser.print_help()
        print("\nError: --prompt is required (or use --test)", file=sys.stderr)
        sys.exit(1)

    # Parse chain
    chain = None
    if args.chain:
        chain = [m.strip() for m in args.chain.split(",")]

    # Run orchestration
    try:
        result = run_orchestration(
            prompt=args.prompt,
            strategy=args.strategy,
            max_cost=args.max_cost,
            chain=chain,
            ensemble_size=args.ensemble_size,
            verbose=args.verbose
        )

        # Print result
        print_result(result, verbose=args.verbose)

        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2)
            print(f"Result saved to: {output_path}")

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
