#!/usr/bin/env python3
"""
Prompt Version Manager
Manages semantic versioning for prompts and templates with history tracking
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import difflib
import argparse


class VersionManager:
    def __init__(self, version_file: str = None):
        """Initialize version manager with version storage file"""
        if version_file is None:
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            version_file = project_root / "data" / "versions.json"

        self.version_file = Path(version_file)
        self.versions = self._load_versions()

    def _load_versions(self) -> Dict:
        """Load version history from JSON file"""
        if not self.version_file.exists():
            return {"files": {}}

        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {self.version_file}, starting fresh")
            return {"files": {}}

    def _save_versions(self):
        """Save version history to JSON file"""
        self.version_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, indent=2, ensure_ascii=False)

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]

    def _get_file_key(self, filepath: str) -> str:
        """Get normalized file key for storage"""
        return str(Path(filepath).resolve())

    def _read_file(self, filepath: str) -> str:
        """Read file content"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def _write_file(self, filepath: str, content: str):
        """Write content to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def _increment_version(self, current: str, bump: str = 'patch') -> str:
        """Increment semantic version number"""
        if current == "0.0.0":
            return "0.1.0"

        try:
            major, minor, patch = map(int, current.split('.'))
        except ValueError:
            return "0.1.0"

        if bump == 'major':
            return f"{major + 1}.0.0"
        elif bump == 'minor':
            return f"{major}.{minor + 1}.0"
        else:  # patch
            return f"{major}.{minor}.{patch + 1}"

    def _auto_detect_bump(self, old_content: str, new_content: str) -> str:
        """Auto-detect version bump type based on content changes"""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()

        # Calculate change ratio
        diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=''))
        changes = [line for line in diff if line.startswith('+') or line.startswith('-')]

        if not old_lines:
            return 'minor'

        change_ratio = len(changes) / (len(old_lines) + len(new_lines))

        # Major: > 50% changed
        if change_ratio > 0.5:
            return 'major'
        # Minor: > 20% changed
        elif change_ratio > 0.2:
            return 'minor'
        # Patch: <= 20% changed
        else:
            return 'patch'

    def save_version(self, filepath: str, message: str = "",
                    bump: Optional[str] = None, auto_increment: bool = True) -> str:
        """
        Save a new version of a file

        Args:
            filepath: Path to the file to version
            message: Commit message describing changes
            bump: Version bump type (major/minor/patch) or None for auto-detect
            auto_increment: Whether to auto-increment version

        Returns:
            Version number assigned
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        file_key = self._get_file_key(filepath)
        content = self._read_file(filepath)
        content_hash = self._compute_hash(content)

        # Initialize file history if needed
        if file_key not in self.versions["files"]:
            self.versions["files"][file_key] = {
                "current_version": "0.0.0",
                "history": [],
                "tags": {}
            }

        file_data = self.versions["files"][file_key]

        # Check if content has changed
        if file_data["history"]:
            last_version = file_data["history"][-1]
            if last_version["hash"] == content_hash:
                print(f"No changes detected in {filepath}")
                return last_version["version"]

        # Determine version number
        if auto_increment:
            # Auto-detect bump type if not specified
            if bump is None and file_data["history"]:
                old_content = file_data["history"][-1]["content"]
                bump = self._auto_detect_bump(old_content, content)

            new_version = self._increment_version(
                file_data["current_version"],
                bump or 'patch'
            )
        else:
            new_version = file_data["current_version"]

        # Create version entry
        version_entry = {
            "version": new_version,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "hash": content_hash,
            "content": content,
            "bump_type": bump or 'auto'
        }

        # Add to history
        file_data["history"].append(version_entry)
        file_data["current_version"] = new_version

        self._save_versions()

        return new_version

    def list_versions(self, filepath: str, limit: Optional[int] = None) -> List[Dict]:
        """
        List version history for a file

        Args:
            filepath: Path to the file
            limit: Maximum number of versions to return

        Returns:
            List of version entries (newest first)
        """
        file_key = self._get_file_key(filepath)

        if file_key not in self.versions["files"]:
            return []

        history = self.versions["files"][file_key]["history"]

        # Return in reverse chronological order
        result = list(reversed(history))

        if limit:
            result = result[:limit]

        return result

    def get_version(self, filepath: str, version: str) -> Optional[Dict]:
        """Get specific version of a file"""
        file_key = self._get_file_key(filepath)

        if file_key not in self.versions["files"]:
            return None

        for entry in self.versions["files"][file_key]["history"]:
            if entry["version"] == version:
                return entry

        return None

    def diff_versions(self, filepath: str, version1: str, version2: str) -> str:
        """
        Generate diff between two versions

        Args:
            filepath: Path to the file
            version1: First version (older)
            version2: Second version (newer)

        Returns:
            Unified diff string
        """
        v1 = self.get_version(filepath, version1)
        v2 = self.get_version(filepath, version2)

        if not v1:
            raise ValueError(f"Version {version1} not found")
        if not v2:
            raise ValueError(f"Version {version2} not found")

        diff = difflib.unified_diff(
            v1["content"].splitlines(keepends=True),
            v2["content"].splitlines(keepends=True),
            fromfile=f"{filepath} (v{version1})",
            tofile=f"{filepath} (v{version2})",
            lineterm=''
        )

        return ''.join(diff)

    def rollback(self, filepath: str, version: str, create_backup: bool = True) -> bool:
        """
        Rollback file to a specific version

        Args:
            filepath: Path to the file
            version: Version to rollback to
            create_backup: Whether to save current state before rollback

        Returns:
            True if successful
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        target_version = self.get_version(filepath, version)

        if not target_version:
            raise ValueError(f"Version {version} not found")

        # Create backup of current state if requested
        if create_backup:
            current_content = self._read_file(filepath)
            file_key = self._get_file_key(filepath)
            file_data = self.versions["files"][file_key]

            # Only backup if content is different
            if not file_data["history"] or file_data["history"][-1]["content"] != current_content:
                self.save_version(
                    filepath,
                    f"Auto-backup before rollback to {version}",
                    auto_increment=True
                )

        # Write the target version content
        self._write_file(filepath, target_version["content"])

        return True

    def tag_version(self, filepath: str, version: str, tag: str) -> bool:
        """
        Tag a specific version with a label (e.g., 'production', 'testing')

        Args:
            filepath: Path to the file
            version: Version to tag
            tag: Tag name

        Returns:
            True if successful
        """
        file_key = self._get_file_key(filepath)

        if file_key not in self.versions["files"]:
            raise ValueError(f"No versions found for {filepath}")

        # Verify version exists
        if not self.get_version(filepath, version):
            raise ValueError(f"Version {version} not found")

        # Add tag
        self.versions["files"][file_key]["tags"][tag] = version
        self._save_versions()

        return True

    def get_tag(self, filepath: str, tag: str) -> Optional[str]:
        """Get version number for a tag"""
        file_key = self._get_file_key(filepath)

        if file_key not in self.versions["files"]:
            return None

        return self.versions["files"][file_key]["tags"].get(tag)

    def list_tags(self, filepath: str) -> Dict[str, str]:
        """List all tags for a file"""
        file_key = self._get_file_key(filepath)

        if file_key not in self.versions["files"]:
            return {}

        return self.versions["files"][file_key]["tags"]


def main():
    """CLI interface for version manager"""
    parser = argparse.ArgumentParser(description="Prompt Version Manager")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Save command
    save_parser = subparsers.add_parser('save', help='Save a new version')
    save_parser.add_argument('file', help='File to version')
    save_parser.add_argument('message', nargs='?', default='', help='Commit message')
    save_parser.add_argument('--bump', choices=['major', 'minor', 'patch'],
                            help='Version bump type')

    # List command
    list_parser = subparsers.add_parser('list', help='List version history')
    list_parser.add_argument('file', help='File to list versions for')
    list_parser.add_argument('--limit', type=int, help='Limit number of results')

    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Show diff between versions')
    diff_parser.add_argument('file', help='File to diff')
    diff_parser.add_argument('v1', help='First version')
    diff_parser.add_argument('v2', help='Second version')

    # Rollback command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback to a version')
    rollback_parser.add_argument('file', help='File to rollback')
    rollback_parser.add_argument('version', help='Version to rollback to')
    rollback_parser.add_argument('--no-backup', action='store_true',
                                help='Skip creating backup')

    # Tag command
    tag_parser = subparsers.add_parser('tag', help='Tag a version')
    tag_parser.add_argument('file', help='File to tag')
    tag_parser.add_argument('version', help='Version to tag')
    tag_parser.add_argument('tag', help='Tag name')

    # List tags command
    tags_parser = subparsers.add_parser('tags', help='List tags for a file')
    tags_parser.add_argument('file', help='File to list tags for')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = VersionManager()

    try:
        if args.command == 'save':
            version = manager.save_version(args.file, args.message, bump=args.bump)
            print(f"Saved version {version} of {args.file}")
            if args.message:
                print(f"Message: {args.message}")

        elif args.command == 'list':
            versions = manager.list_versions(args.file, limit=args.limit)
            if not versions:
                print(f"No versions found for {args.file}")
                return

            print(f"\nVersion history for {args.file}:\n")
            for v in versions:
                tags = []
                for tag_name, tag_version in manager.list_tags(args.file).items():
                    if tag_version == v['version']:
                        tags.append(tag_name)

                tag_str = f" [{', '.join(tags)}]" if tags else ""
                print(f"v{v['version']}{tag_str}")
                print(f"  Date: {v['timestamp']}")
                print(f"  Hash: {v['hash']}")
                if v['message']:
                    print(f"  Message: {v['message']}")
                print()

        elif args.command == 'diff':
            diff = manager.diff_versions(args.file, args.v1, args.v2)
            print(diff)

        elif args.command == 'rollback':
            manager.rollback(args.file, args.version, create_backup=not args.no_backup)
            print(f"Rolled back {args.file} to version {args.version}")

        elif args.command == 'tag':
            manager.tag_version(args.file, args.version, args.tag)
            print(f"Tagged version {args.version} as '{args.tag}'")

        elif args.command == 'tags':
            tags = manager.list_tags(args.file)
            if not tags:
                print(f"No tags found for {args.file}")
                return

            print(f"\nTags for {args.file}:\n")
            for tag, version in tags.items():
                print(f"  {tag}: v{version}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
