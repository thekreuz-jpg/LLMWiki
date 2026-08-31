#!/usr/bin/env python3
"""audit_public.py — fail on secrets, local paths, private keys, and plugin/cache state."""

import os
import re
import sys
from pathlib import Path


# Patterns that should never be committed
SECRET_PATTERNS = [
    r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
    r'(?i)private[_-]?key',
    r'(?i)-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?i)aws[_-]?secret[_-]?access[_-]?key',
    r'(?i)github[_-]?token',
    r'(?i)ghp_[a-zA-Z0-9]{36}',
    r'(?i)gho_[a-zA-Z0-9]{36}',
]

# Local path patterns (machine-specific)
LOCAL_PATH_PATTERNS = [
    r'[A-Z]:\\Users\\[^\\]+\\',
    r'/home/[^/]+/',
    r'/Users/[^/]+/',
    r'C:\\Users\\[^\\]+\\',
]

# Files that should never be committed
BLOCKED_FILES = [
    '.obsidian/workspace.json',
    '.obsidian/workspace-mobile.json',
    '.obsidian/cache/',
    '.obsidian/logs/',
    '.obsidian/plugins/',  # plugin code (data.json is OK)
    'Raw/Files/',  # binary source files
    '.DS_Store',
    'Thumbs.db',
    '*.log',
]


def find_vault_root():
    cwd = Path.cwd()
    for path in [cwd] + list(cwd.parents):
        if (path / ".git").exists():
            return path
    return cwd


def scan_file(file_path, vault_root):
    """Scan a file for secrets and local paths."""
    issues = []
    rel_path = str(file_path.relative_to(vault_root)).replace("\\", "/")
    
    # Check blocked file patterns
    for blocked in BLOCKED_FILES:
        if blocked in rel_path:
            issues.append(f"{rel_path}: matches blocked pattern '{blocked}'")
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Check secret patterns
        for pattern in SECRET_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                issues.append(f"{rel_path}: potential secret found (pattern: {pattern[:30]}...)")
        
        # Check local path patterns (only for non-obsidian config files)
        if not rel_path.startswith(".obsidian/"):
            for pattern in LOCAL_PATH_PATTERNS:
                matches = re.findall(pattern, content)
                if matches:
                    issues.append(f"{rel_path}: local path found (pattern: {pattern})")
    
    except Exception:
        pass  # Binary files, etc.
    
    return issues


def main():
    vault_root = find_vault_root()
    print(f"=== audit_public.py ===")
    print(f"Vault root: {vault_root}")
    
    # Get staged files
    import subprocess
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, cwd=vault_root
        )
        staged_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        # Fallback: scan all files
        staged_files = []
        for root, dirs, files in os.walk(vault_root):
            # Skip .git
            if ".git" in root:
                continue
            for f in files:
                staged_files.append(os.path.join(root, f))
    
    if not staged_files:
        print("No files to audit.")
        return 0
    
    all_issues = []
    for file_path_str in staged_files:
        if not file_path_str:
            continue
        file_path = Path(file_path_str)
        if not file_path.exists():
            continue
        if file_path.is_dir():
            continue
        issues = scan_file(file_path, vault_root)
        all_issues.extend(issues)
    
    if all_issues:
        print(f"{len(issues)} issue(s) found:")
        for issue in all_issues:
            print(f"  - {issue}")
        print("\nCommit blocked. Fix issues or use --no-verify to bypass.")
        return 1
    
    print(f"Audited {len(staged_files)} file(s). No issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
