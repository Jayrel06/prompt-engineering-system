#!/usr/bin/env python3
"""Import-friendly wrapper for context-loader.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).with_name("context-loader.py")
_SPEC = importlib.util.spec_from_file_location("_context_loader_cli", _MODULE_PATH)

if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load {_MODULE_PATH}")

_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

_ORIGINAL_LOAD_FILE = _MODULE.load_file
_ORIGINAL_FIND_FRAMEWORK = _MODULE.find_framework
_ORIGINAL_ASSEMBLE_CONTEXT = _MODULE.assemble_context

CONTEXT_RULES = _MODULE.CONTEXT_RULES
CONTEXT_DIR = _MODULE.CONTEXT_DIR
FRAMEWORKS_DIR = _MODULE.FRAMEWORKS_DIR
TEMPLATES_DIR = _MODULE.TEMPLATES_DIR
PROJECT_ROOT = _MODULE.PROJECT_ROOT
main = _MODULE.main


def load_file(filepath):
    return _ORIGINAL_LOAD_FILE(filepath)


def _sync_module_globals():
    _MODULE.CONTEXT_RULES = CONTEXT_RULES
    _MODULE.CONTEXT_DIR = CONTEXT_DIR
    _MODULE.FRAMEWORKS_DIR = FRAMEWORKS_DIR
    _MODULE.TEMPLATES_DIR = TEMPLATES_DIR
    _MODULE.PROJECT_ROOT = PROJECT_ROOT
    _MODULE.load_file = load_file
    _MODULE.find_framework = find_framework


def find_framework(name):
    _sync_module_globals()
    for category in ["planning", "analysis", "decision", "technical", "communication", "creation"]:
        path = FRAMEWORKS_DIR / category / f"{name}.md"
        if path.exists() is True:
            return path
    return None


def assemble_context(*args, **kwargs):
    _sync_module_globals()
    return _ORIGINAL_ASSEMBLE_CONTEXT(*args, **kwargs)


if __name__ == "__main__":
    main()
