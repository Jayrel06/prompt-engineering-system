# MCP Server Update - Prompt Improvement Tools

## Summary
Updated the MCP server at `mcp-server/src/index.ts` to add 5 new prompt improvement tools.

## Changes Made

### New Tools Added

1. **improve_prompt**
   - Input: `prompt` (string), `auto_fix` (boolean, default: true)
   - Calls `scripts/prompt_doctor.py` to analyze and improve prompts
   - Returns improved prompt with explanation of changes
   - Uses AI-powered analysis to detect and fix issues

2. **diagnose_prompt**
   - Input: `prompt` (string)
   - Calls `scripts/prompt_doctor.py` for detailed analysis
   - Returns diagnostic report with:
     - Quality scores (clarity, specificity, completeness, etc.)
     - List of issues found with severity levels
     - Specific suggestions for improvement
     - Overall health assessment

3. **optimize_prompt**
   - Input: `prompt` (string), `num_variations` (number, default: 3)
   - Calls `scripts/prompt_optimizer.py` to generate variations
   - Tests different optimization techniques
   - Returns the best variation with detailed scoring

4. **get_prompting_best_practices**
   - Input: `topic` (string, optional)
   - Reads from `context/technical/prompting-best-practices.md`
   - If topic provided, filters content to relevant sections
   - Returns comprehensive best practices guide

5. **route_prompt**
   - Input: `task` (string)
   - Calls `scripts/prompt_router.py` to analyze task
   - Returns recommended:
     - Prompting framework to use
     - Specific techniques to apply
     - Model recommendation
     - Reasoning for selections

### Implementation Details

- All handlers include proper error handling and cleanup
- Temporary files created in `.tmp/` directory with automatic cleanup
- Large buffer size (10MB) for handling long prompts and outputs
- JSON parsing for structured responses where applicable
- Proper TypeScript typing for all parameters

### File Statistics

- Original file: 580 lines
- Updated file: 910 lines
- Added: 330+ lines of new code
- Total case handlers: 12 (7 original + 5 new)

### Python Script Dependencies

The new tools depend on these existing Python scripts:
- `scripts/prompt_doctor.py` - Diagnoses prompt issues
- `scripts/prompt_optimizer.py` - Generates and tests variations
- `scripts/prompt_router.py` - Routes to optimal framework
- `context/technical/prompting-best-practices.md` - Best practices guide

All scripts already exist in the repository.

### Backup

Original file backed up to: `mcp-server/src/index.ts.old`

## Usage Examples

### Improve a prompt
```typescript
{
  "tool": "improve_prompt",
  "arguments": {
    "prompt": "Write me a blog post",
    "auto_fix": true
  }
}
```

### Diagnose prompt quality
```typescript
{
  "tool": "diagnose_prompt",
  "arguments": {
    "prompt": "Summarize this article"
  }
}
```

### Optimize with variations
```typescript
{
  "tool": "optimize_prompt",
  "arguments": {
    "prompt": "Extract contact info from text",
    "num_variations": 5
  }
}
```

### Get best practices on a topic
```typescript
{
  "tool": "get_prompting_best_practices",
  "arguments": {
    "topic": "chain-of-thought"
  }
}
```

### Route task to framework
```typescript
{
  "tool": "route_prompt",
  "arguments": {
    "task": "Analyze code for security vulnerabilities"
  }
}
```

## Testing

To test the updated MCP server:

1. Rebuild the server: `npm run build` (if TypeScript is installed)
2. Restart the MCP server
3. Test each new tool with sample prompts
4. Verify Python scripts are accessible and working

## Notes

- The `improve_prompt` tool currently runs `prompt_doctor.py` twice when `auto_fix` is true (once for diagnosis, once for the fix). This could be optimized in future updates.
- Topic filtering in `get_prompting_best_practices` uses simple string matching and header detection. May not catch all relevant sections.
- All tools create temporary files in `.tmp/` directory which are cleaned up after execution.
