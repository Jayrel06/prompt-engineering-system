# Prompt Versioning System - Quick Start Guide

## Overview

The prompt versioning system provides semantic versioning, diff tracking, and rollback capabilities for all prompt templates and files in your system.

## Files Created

1. **`scripts/version_manager.py`** - Core versioning engine (435 lines)
2. **`data/versions.json`** - Version history storage
3. **`scripts/prompt.sh`** - Updated with version commands

## Quick Start

### Save a Version

```bash
# Save current state of a file
prompt version save templates/voice-ai/vapi.md "Updated error handling"

# Save without a message
prompt version save templates/voice-ai/vapi.md
```

### List Version History

```bash
prompt version list templates/voice-ai/vapi.md
```

Output:
```
Version history for templates/voice-ai/vapi.md:

v0.2.0 [production]
  Date: 2025-11-28T00:09:34.983158
  Hash: cbc43ff98cf7
  Message: Updated error handling

v0.1.0
  Date: 2025-11-27T15:30:22.123456
  Hash: a1b2c3d4e5f6
  Message: Initial version
```

### Compare Versions

```bash
prompt version diff templates/voice-ai/vapi.md 0.1.0 0.2.0
```

Shows unified diff between the two versions.

### Rollback to Previous Version

```bash
# Rollback to specific version (creates backup first)
prompt version rollback templates/voice-ai/vapi.md 0.1.0
```

### Tag Versions

```bash
# Tag a version (e.g., production, staging, testing)
prompt version tag templates/voice-ai/vapi.md 0.2.0 production

# List all tags
prompt version tags templates/voice-ai/vapi.md
```

## How It Works

### Semantic Versioning

Version numbers follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** (>50% changed): Breaking changes or major rewrites
- **MINOR** (>20% changed): New features or significant updates
- **PATCH** (≤20% changed): Bug fixes or minor tweaks

The system auto-detects the appropriate bump type based on content changes.

### Manual Version Bumping

```bash
# Force a specific version bump type
python3 scripts/version_manager.py save <file> "message" --bump major
python3 scripts/version_manager.py save <file> "message" --bump minor
python3 scripts/version_manager.py save <file> "message" --bump patch
```

### Version Storage

All versions are stored in `data/versions.json` with:
- Full file content
- Timestamp
- SHA-256 hash (truncated)
- Commit message
- Version number
- Bump type

### Safety Features

1. **Auto-backup before rollback** - Creates backup of current state before reverting
2. **Content change detection** - Only creates new version if content actually changed
3. **Hash verification** - Uses SHA-256 to detect duplicate content
4. **Full content storage** - Complete file content stored for each version

## Advanced Usage

### Using Python Directly

```python
from version_manager import VersionManager

# Initialize
vm = VersionManager()

# Save version
version = vm.save_version(
    "templates/voice-ai/vapi.md",
    message="Updated error handling",
    bump="minor"  # optional
)

# List versions
versions = vm.list_versions("templates/voice-ai/vapi.md", limit=10)

# Get specific version
version_data = vm.get_version("templates/voice-ai/vapi.md", "0.1.0")

# Diff between versions
diff = vm.diff_versions("templates/voice-ai/vapi.md", "0.1.0", "0.2.0")

# Rollback
vm.rollback("templates/voice-ai/vapi.md", "0.1.0")

# Tag version
vm.tag_version("templates/voice-ai/vapi.md", "0.2.0", "production")

# Get version by tag
version = vm.get_tag("templates/voice-ai/vapi.md", "production")
```

## Best Practices

1. **Save before major changes** - Create a version before making significant edits
2. **Use descriptive messages** - Write clear commit messages explaining what changed
3. **Tag stable versions** - Tag versions that are deployed to production
4. **Regular snapshots** - Version prompts after testing or validation
5. **Review diffs** - Use diff to understand what changed between versions

## Example Workflow

```bash
# 1. Make changes to your prompt template
vim templates/voice-ai/vapi.md

# 2. Save the new version
prompt version save templates/voice-ai/vapi.md "Added multi-language support"

# 3. Tag it for testing
prompt version tag templates/voice-ai/vapi.md 0.2.0 testing

# 4. After testing, tag as production
prompt version tag templates/voice-ai/vapi.md 0.2.0 production

# 5. If issues arise, rollback
prompt version rollback templates/voice-ai/vapi.md 0.1.0

# 6. Compare what changed
prompt version diff templates/voice-ai/vapi.md 0.1.0 0.2.0
```

## Status Tracking

Check versioned files count in system status:

```bash
prompt status
```

Output includes:
```
Resources:
  Frameworks: 12
  Templates:  8
  Context:    25
  Versioned:  3
```

## Troubleshooting

### "No versions found"
The file hasn't been versioned yet. Run `prompt version save <file>` first.

### "Version X not found"
Check available versions with `prompt version list <file>`.

### Rollback creates new version
This is expected behavior - the backup is saved as the latest version before rollback.

## File Locations

- **Version data**: `data/versions.json`
- **Backups**: Created as new versions in the history
- **Version manager**: `scripts/version_manager.py`

## Notes

- All file paths are stored as absolute paths internally
- You can use relative paths in commands (relative to project root)
- Version history includes full file content, so `versions.json` will grow
- Tags are per-file (same tag name can be used for different files)
