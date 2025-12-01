# LLM Model Pricing Reference

Last Updated: November 2024

## Overview

This document tracks current pricing for major LLM providers. Prices are per million tokens unless otherwise specified.

## Anthropic Claude Models

### Claude 3.5 Sonnet
- **Model ID**: `claude-3-5-sonnet-20241022`
- **Input**: $3.00 per million tokens
- **Output**: $15.00 per million tokens
- **Context Window**: 200,000 tokens
- **Best For**: Complex reasoning, coding, analysis, long-form content
- **Notes**: Most capable model for complex tasks requiring deep reasoning

### Claude 3 Haiku
- **Model ID**: `claude-3-haiku-20240307`
- **Input**: $0.25 per million tokens
- **Output**: $1.25 per million tokens
- **Context Window**: 200,000 tokens
- **Best For**: Fast responses, simple queries, high-volume tasks
- **Notes**: Fastest and most cost-effective for straightforward tasks

### Claude 3 Opus (Legacy)
- **Model ID**: `claude-3-opus-20240229`
- **Input**: $15.00 per million tokens
- **Output**: $75.00 per million tokens
- **Context Window**: 200,000 tokens
- **Best For**: Maximum capability tasks
- **Notes**: Largely superseded by Claude 3.5 Sonnet which offers better performance at lower cost

## OpenAI Models

### GPT-4o
- **Model ID**: `gpt-4o-2024-11-20`
- **Input**: $2.50 per million tokens
- **Output**: $10.00 per million tokens
- **Context Window**: 128,000 tokens
- **Best For**: Multimodal tasks, vision, structured outputs
- **Notes**: Latest GPT-4 optimized model with vision capabilities

### GPT-4o-mini
- **Model ID**: `gpt-4o-mini-2024-07-18`
- **Input**: $0.15 per million tokens
- **Output**: $0.60 per million tokens
- **Context Window**: 128,000 tokens
- **Best For**: Cost-effective tasks, high-volume operations
- **Notes**: Smaller, faster version of GPT-4o

### GPT-4 Turbo (Legacy)
- **Model ID**: `gpt-4-turbo-2024-04-09`
- **Input**: $10.00 per million tokens
- **Output**: $30.00 per million tokens
- **Context Window**: 128,000 tokens
- **Best For**: Complex reasoning (legacy)
- **Notes**: Superseded by GPT-4o

### GPT-3.5 Turbo
- **Model ID**: `gpt-3.5-turbo-0125`
- **Input**: $0.50 per million tokens
- **Output**: $1.50 per million tokens
- **Context Window**: 16,385 tokens
- **Best For**: Simple tasks, chatbots
- **Notes**: Previous generation, less capable than GPT-4o-mini

## Cost Optimization Strategies

### Model Selection Guidelines

1. **Use Haiku/GPT-4o-mini for**:
   - Simple classification tasks
   - Quick lookups and queries
   - High-volume repetitive tasks
   - Format conversion
   - Basic summarization

2. **Use Sonnet/GPT-4o for**:
   - Complex reasoning and analysis
   - Code generation and review
   - Long-form content creation
   - Multi-step problem solving
   - Strategic planning

3. **Use Opus only when**:
   - Absolute maximum capability required
   - Critical decision support
   - Very complex creative tasks
   - You've validated that smaller models can't handle it

### Token Optimization

1. **Reduce Input Tokens**:
   - Use context-loading rules to send only relevant information
   - Implement semantic search to find relevant context vs sending everything
   - Compress or summarize large documents before sending
   - Use structured formats (JSON) instead of verbose natural language when possible

2. **Reduce Output Tokens**:
   - Request concise responses when appropriate
   - Use structured outputs (JSON) vs prose
   - Set max_tokens limits
   - Use streaming to stop early if needed

3. **Caching Strategies** (Claude only):
   - Structure prompts with stable system context at the top
   - Prompt caching can reduce costs by 90% for repeated context
   - Cache hits: $0.30/$1.50 per million tokens (Sonnet)

### Cost-Effective Patterns

1. **Cascade Pattern**:
   - Try Haiku/mini first
   - Only escalate to Sonnet/4o if needed
   - Log quality metrics to tune decision

2. **Batch Processing**:
   - Aggregate similar requests
   - Use async APIs where available
   - Process in parallel to reduce wall-clock time

3. **Hybrid Approaches**:
   - Use smaller models for initial filtering/routing
   - Use larger models only for final processing
   - Example: Haiku classifies → Sonnet handles complex cases

## Monthly Budget Examples

### Small Team ($100/month)
- **Primary**: Claude Haiku or GPT-4o-mini
- **Capacity**: ~133M input tokens + ~13M output tokens (Haiku)
- **Use Cases**: Daily queries, simple automation, quick lookups
- **Strategy**: Reserve Sonnet for critical tasks only

### Medium Team ($500/month)
- **Primary**: Mix of Haiku and Sonnet
- **Capacity**: ~83M input + ~16M output (Sonnet) or mixed usage
- **Use Cases**: Code generation, analysis, planning, automation
- **Strategy**: 80% Haiku, 20% Sonnet based on task complexity

### Large Team ($2000/month)
- **Primary**: Primarily Sonnet with Haiku for simple tasks
- **Capacity**: ~333M input + ~66M output (Sonnet)
- **Use Cases**: Full engineering support, complex analysis, automation
- **Strategy**: Smart routing based on task type

## Tracking Recommendations

### What to Track
1. **Per Request**:
   - Model used
   - Input/output tokens
   - Category/use case
   - Timestamp
   - User/project

2. **Aggregate Metrics**:
   - Daily/weekly/monthly spend by model
   - Cost per category
   - Average tokens per request type
   - Model utilization percentages

### Alerts and Limits
- Set daily/weekly/monthly budget alerts
- Track anomalies (unusually high token counts)
- Monitor cost per request type trends
- Review model selection effectiveness

## Price Update Schedule

Pricing can change. Check official sources:
- **Anthropic**: https://www.anthropic.com/api
- **OpenAI**: https://openai.com/api/pricing/

**Review this document**: Monthly or when providers announce changes

## Integration with Cost Tracker

Use the `cost_tracker.py` script to:
```bash
# Log usage
python scripts/cost_tracker.py log --model claude-sonnet-3.5 --input-tokens 1000 --output-tokens 500

# View reports
python scripts/cost_tracker.py report --period weekly

# Export data
python scripts/cost_tracker.py export --format csv --output monthly_usage.csv
```

The tracker automatically uses these pricing rates for cost calculation.
