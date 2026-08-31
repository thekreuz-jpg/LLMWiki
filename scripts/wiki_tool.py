#!/usr/bin/env python3
"""wiki_tool.py — deterministic tooling for the LLM Wiki vault."""

import argparse
import datetime
import glob
import json
import os
import re
import sys
from pathlib import Path

# Allowed tags for compiled Wiki notes
ALLOWED_TAGS = {"topic", "concept", "entity", "project", "log"}
SOURCE_TAG = "source"

# Vault structure folders
RAW_SOURCES_DIR = "Raw/Sources"
WIKI_DIRS = ["Wiki/Topics", "Wiki/Concepts", "Wiki/Entities", "Wiki/Projects", "Wiki/Logs"]
SCHEMA_DIR = "Schema"
CATALOG_PATH = "Wiki/catalog.jsonl"
INDEX_PATH = "Wiki/index.md"
MANIFEST_PATH = "Schema/source-manifest.jsonl"
LOG_PATH = "Wiki/Logs/log.md"


def find_vault_root():
    """Find the vault root by walking up from cwd."""
    cwd = Path.cwd()
    for path in [cwd] + list(cwd.parents):
        if (path / "scripts" / "wiki_tool.py").exists() or (path / ".git").exists():
            if (path / RAW_SOURCES_DIR).exists() or (path / "Raw").exists():
                return path
    return cwd


def parse_frontmatter(content):
    """Parse YAML-like frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    
    end = content.find("---", 3)
    if end == -1:
        return {}
    
    fm_text = content[3:end].strip()
    fm = {}
    
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        
        # Check if this is a key with a list value on subsequent lines
        if ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            
            # If value is empty, check if next lines are list items
            if not value and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("-"):
                    # Multi-line list
                    lst = []
                    i += 1
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith("-"):
                            item = line[1:].strip().strip('"').strip("'")
                            if item:
                                lst.append(item)
                            i += 1
                        else:
                            break
                    fm[key] = lst
                    continue
            
            # Handle inline list values
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                if not inner:
                    fm[key] = []
                else:
                    items = []
                    for item in inner.split(","):
                        item = item.strip().strip('"').strip("'")
                        if item:
                            items.append(item)
                    fm[key] = items
            # Handle quoted strings
            elif (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                fm[key] = value[1:-1]
            # Handle booleans
            elif value.lower() == "true":
                fm[key] = True
            elif value.lower() == "false":
                fm[key] = False
            # Handle numbers
            elif value.isdigit():
                fm[key] = int(value)
            else:
                fm[key] = value
        i += 1
    
    return fm


def read_note(path):
    """Read a note file and return (frontmatter_dict, body_text)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)
        return fm, content
    except Exception:
        return {}, ""


def get_title(fm, path):
    """Extract title from frontmatter or filename."""
    for key in ["Title", "title", "Name", "name"]:
        if key in fm:
            return fm[key]
    return Path(path).stem


# ─── doctor ──────────────────────────────────────────────────────────────────

def cmd_doctor(vault_root):
    """Non-mutating health check."""
    print("=== wiki_tool.py doctor ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Vault root: {vault_root}")
    print()
    
    issues = []
    
    # Check folder structure
    print("Folder structure:")
    for folder in [RAW_SOURCES_DIR] + WIKI_DIRS + [SCHEMA_DIR, "_templates", ".agents/skills", "scripts"]:
        full_path = vault_root / folder
        exists = full_path.exists()
        status = "OK" if exists else "MISSING"
        print(f"  {folder}: {status}")
        if not exists:
            issues.append(f"Missing folder: {folder}")
    
    # Check catalog
    catalog_path = vault_root / CATALOG_PATH
    catalog_exists = catalog_path.exists()
    print(f"\nCatalog ({CATALOG_PATH}): {'EXISTS' if catalog_exists else 'NOT YET GENERATED'}")
    
    # Check manifest
    manifest_path = vault_root / MANIFEST_PATH
    manifest_exists = manifest_path.exists()
    print(f"Source manifest ({MANIFEST_PATH}): {'EXISTS' if manifest_exists else 'NOT YET GENERATED'}")
    
    # Count notes
    print("\nNote counts:")
    source_count = len(list((vault_root / RAW_SOURCES_DIR).glob("*.md"))) if (vault_root / RAW_SOURCES_DIR).exists() else 0
    print(f"  Raw sources: {source_count}")
    
    wiki_count = 0
    for wiki_dir in WIKI_DIRS:
        wiki_path = vault_root / wiki_dir
        if wiki_path.exists():
            count = len(list(wiki_path.glob("*.md")))
            wiki_count += count
            print(f"  {wiki_dir}: {count}")
    print(f"  Total Wiki notes: {wiki_count}")
    
    if issues:
        print(f"\n{len(issues)} issue(s) found:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    
    print("\nAll checks passed.")
    return 0


# ─── build ───────────────────────────────────────────────────────────────────

def cmd_build(vault_root):
    """Generate catalog, index, and per-folder indexes."""
    print("=== wiki_tool.py build ===")
    
    # Build catalog
    catalog = []
    for wiki_dir in WIKI_DIRS:
        wiki_path = vault_root / wiki_dir
        if not wiki_path.exists():
            continue
        for note_path in sorted(wiki_path.glob("*.md")):
            fm, _ = read_note(note_path)
            rel_path = str(note_path.relative_to(vault_root)).replace("\\", "/")
            tag = None
            for t in fm.get("tags", []):
                if t in ALLOWED_TAGS:
                    tag = t
                    break
            if not tag:
                tag = "unknown"
            
            entry = {
                "path": rel_path,
                "title": get_title(fm, note_path),
                "tag": tag,
                "topics": fm.get("topics", []),
                "sources": fm.get("sources", []),
                "updated": fm.get("updated", datetime.date.today().isoformat())
            }
            catalog.append(entry)
    
    # Write catalog
    catalog_path = vault_root / CATALOG_PATH
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with open(catalog_path, "w", encoding="utf-8") as f:
        for entry in catalog:
            f.write(json.dumps(entry) + "\n")
    print(f"Generated catalog: {len(catalog)} entries -> {CATALOG_PATH}")
    
    # Build master index
    index_lines = [
        "# Wiki Index",
        "",
        f"Generated: {datetime.date.today().isoformat()}",
        f"Total compiled notes: {len(catalog)}",
        "",
        "## By Tag",
    ]
    
    by_tag = {}
    for entry in catalog:
        tag = entry["tag"]
        by_tag.setdefault(tag, []).append(entry)
    
    for tag in sorted(by_tag.keys()):
        index_lines.append(f"\n### {tag}")
        for entry in sorted(by_tag[tag], key=lambda e: e["title"]):
            index_lines.append(f"- [{entry['title']}]({entry['path']})")
    
    index_lines.append("\n## By Folder\n")
    for wiki_dir in WIKI_DIRS:
        dir_entries = [e for e in catalog if e["path"].startswith(wiki_dir)]
        if dir_entries:
            index_lines.append(f"### {wiki_dir}")
            for entry in sorted(dir_entries, key=lambda e: e["title"]):
                index_lines.append(f"- [{entry['title']}]({entry['path']})")
            index_lines.append("")
    
    index_path = vault_root / INDEX_PATH
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")
    print(f"Generated master index: {INDEX_PATH}")
    
    # Build per-folder indexes
    for wiki_dir in WIKI_DIRS:
        dir_entries = [e for e in catalog if e["path"].startswith(wiki_dir)]
        if not dir_entries:
            continue
        folder_index_path = vault_root / wiki_dir / "index.md"
        lines = [
            f"# {wiki_dir.split('/')[-1]} Index",
            "",
            f"Total: {len(dir_entries)}",
            "",
        ]
        for entry in sorted(dir_entries, key=lambda e: e["title"]):
            lines.append(f"- [{entry['title']}]({entry['path']})")
        with open(folder_index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Generated folder index: {wiki_dir}/index.md")
    
    return 0


# ─── lint ────────────────────────────────────────────────────────────────────

def cmd_lint(vault_root):
    """Validate compiled Wiki note frontmatter."""
    print("=== wiki_tool.py lint ===")
    errors = []
    
    for wiki_dir in WIKI_DIRS:
        wiki_path = vault_root / wiki_dir
        if not wiki_path.exists():
            continue
        for note_path in sorted(wiki_path.glob("*.md")):
            # Skip generated index files and log.md — they are build artifacts
            if note_path.name in ("index.md", "log.md"):
                continue
            fm, _ = read_note(note_path)
            rel_path = str(note_path.relative_to(vault_root)).replace("\\", "/")
            
            # Check allowed tags
            tags = fm.get("tags", [])
            has_allowed = any(t in ALLOWED_TAGS for t in tags)
            if not has_allowed:
                errors.append(f"{rel_path}: no allowed tag (found: {tags})")
            
            # Check source_count matches sources length
            sources = fm.get("sources", [])
            source_count = fm.get("source_count", 0)
            if source_count != len(sources):
                errors.append(f"{rel_path}: source_count ({source_count}) != len(sources) ({len(sources)})")
            
            # Check source links point to existing files
            for src in sources:
                src_path = vault_root / src
                if not src_path.exists():
                    errors.append(f"{rel_path}: source link '{src}' does not exist")
    
    if errors:
        print(f"{len(errors)} lint error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("All Wiki notes pass lint checks.")
    return 0


# ─── source-scan ─────────────────────────────────────────────────────────────

def cmd_source_scan(vault_root, update=False, accept_covered=False):
    """List Raw sources and optionally update manifest."""
    print("=== wiki_tool.py source-scan ===")
    
    sources_dir = vault_root / RAW_SOURCES_DIR
    if not sources_dir.exists():
        print("No Raw/Sources directory found.")
        return 1
    
    sources = sorted(sources_dir.glob("*.md"))
    print(f"Found {len(sources)} source(s):")
    
    for src_path in sources:
        fm, _ = read_note(src_path)
        rel_path = str(src_path.relative_to(vault_root)).replace("\\", "/")
        title = get_title(fm, src_path)
        processed = fm.get("Processed", False)
        print(f"  {rel_path}: {title} (processed={processed})")
    
    if update:
        manifest = []
        for src_path in sources:
            fm, _ = read_note(src_path)
            rel_path = str(src_path.relative_to(vault_root)).replace("\\", "/")
            title = get_title(fm, src_path)
            processed = fm.get("Processed", False)
            
            covered_by = []
            if accept_covered and processed:
                # Find Wiki notes that reference this source
                for wiki_dir in WIKI_DIRS:
                    wiki_path = vault_root / wiki_dir
                    if not wiki_path.exists():
                        continue
                    for note_path in wiki_path.glob("*.md"):
                        note_fm, _ = read_note(note_path)
                        note_sources = note_fm.get("sources", [])
                        if rel_path in note_sources:
                            covered_by.append(
                                str(note_path.relative_to(vault_root)).replace("\\", "/")
                            )
            
            entry = {
                "path": rel_path,
                "title": title,
                "processed": processed,
                "covered_by": covered_by,
                "updated": datetime.date.today().isoformat()
            }
            manifest.append(entry)
        
        manifest_path = vault_root / MANIFEST_PATH
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            for entry in manifest:
                f.write(json.dumps(entry) + "\n")
        print(f"\nUpdated manifest: {len(manifest)} entries -> {MANIFEST_PATH}")
    
    return 0


# ─── source-lint ─────────────────────────────────────────────────────────────

def cmd_source_lint(vault_root):
    """Validate source frontmatter and coverage."""
    print("=== wiki_tool.py source-lint ===")
    errors = []
    
    sources_dir = vault_root / RAW_SOURCES_DIR
    if not sources_dir.exists():
        print("No Raw/Sources directory found.")
        return 1
    
    for src_path in sorted(sources_dir.glob("*.md")):
        fm, _ = read_note(src_path)
        rel_path = str(src_path.relative_to(vault_root)).replace("\\", "/")
        
        # Check required fields
        for field in ["Title", "Reference", "Created", "Processed", "tags"]:
            if field not in fm:
                errors.append(f"{rel_path}: missing required field '{field}'")
        
        # Check processed sources have coverage
        if fm.get("Processed", False):
            covered = False
            for wiki_dir in WIKI_DIRS:
                wiki_path = vault_root / wiki_dir
                if not wiki_path.exists():
                    continue
                for note_path in wiki_path.glob("*.md"):
                    note_fm, _ = read_note(note_path)
                    if rel_path in note_fm.get("sources", []):
                        covered = True
                        break
                if covered:
                    break
            if not covered:
                errors.append(f"{rel_path}: marked processed but no Wiki note references it")
    
    if errors:
        print(f"{len(errors)} source lint error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("All sources pass lint checks.")
    return 0


# ─── source-delta ────────────────────────────────────────────────────────────

def cmd_source_delta(vault_root):
    """Show Raw sources not represented in the manifest."""
    print("=== wiki_tool.py source-delta ===")
    
    manifest_path = vault_root / MANIFEST_PATH
    if not manifest_path.exists():
        print("No manifest found. Run 'source-scan --update' first.")
        return 1
    
    manifest_paths = set()
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                manifest_paths.add(entry["path"])
            except json.JSONDecodeError:
                continue
    
    sources_dir = vault_root / RAW_SOURCES_DIR
    if not sources_dir.exists():
        print("No Raw/Sources directory found.")
        return 1
    
    delta = []
    for src_path in sorted(sources_dir.glob("*.md")):
        rel_path = str(src_path.relative_to(vault_root)).replace("\\", "/")
        if rel_path not in manifest_paths:
            delta.append(rel_path)
    
    if delta:
        print(f"{len(delta)} source(s) not in manifest:")
        for path in delta:
            print(f"  - {path}")
    else:
        print("All sources are represented in the manifest.")
    
    return 0


# ─── source-coverage ─────────────────────────────────────────────────────────

def cmd_source_coverage(vault_root):
    """Show which Raw sources are covered by compiled Wiki notes."""
    print("=== wiki_tool.py source-coverage ===")
    
    sources_dir = vault_root / RAW_SOURCES_DIR
    if not sources_dir.exists():
        print("No Raw/Sources directory found.")
        return 1
    
    sources = sorted(sources_dir.glob("*.md"))
    
    for src_path in sources:
        fm, _ = read_note(src_path)
        rel_path = str(src_path.relative_to(vault_root)).replace("\\", "/")
        title = get_title(fm, src_path)
        
        covered_by = []
        for wiki_dir in WIKI_DIRS:
            wiki_path = vault_root / wiki_dir
            if not wiki_path.exists():
                continue
            for note_path in wiki_path.glob("*.md"):
                note_fm, _ = read_note(note_path)
                if rel_path in note_fm.get("sources", []):
                    covered_by.append(
                        str(note_path.relative_to(vault_root)).replace("\\", "/")
                    )
        
        status = "COVERED" if covered_by else "UNCOVERED"
        print(f"  {rel_path}: {title} [{status}]")
        for wiki_path in covered_by:
            print(f"    <- {wiki_path}")
    
    return 0


# ─── search-catalog ──────────────────────────────────────────────────────────

def cmd_search_catalog(vault_root, query):
    """Search compiled Wiki notes through the catalog."""
    print(f"=== wiki_tool.py search-catalog: '{query}' ===")
    
    catalog_path = vault_root / CATALOG_PATH
    if not catalog_path.exists():
        print("No catalog found. Run 'build' first.")
        return 1
    
    query_lower = query.lower()
    results = []
    
    with open(catalog_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                # Search in title, topics, and path
                searchable = " ".join([
                    entry.get("title", ""),
                    " ".join(entry.get("topics", [])),
                    entry.get("path", ""),
                    entry.get("tag", "")
                ]).lower()
                if query_lower in searchable:
                    results.append(entry)
            except json.JSONDecodeError:
                continue
    
    if results:
        print(f"{len(results)} result(s):")
        for entry in results:
            print(f"  [{entry['tag']}] {entry['title']} -> {entry['path']}")
    else:
        print("No results found.")
    
    return 0


# ─── log ─────────────────────────────────────────────────────────────────────

def cmd_log(vault_root, title, details):
    """Append a short entry to Wiki/Logs/log.md."""
    print("=== wiki_tool.py log ===")
    
    log_path = vault_root / LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.date.today().isoformat()
    entry = f"\n## {today}: {title}\n\n{details}\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"Logged: {title} -> {LOG_PATH}")
    return 0


# ─── main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LLM Wiki deterministic tooling")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # doctor
    subparsers.add_parser("doctor", help="Health check")
    
    # build
    subparsers.add_parser("build", help="Generate catalog and indexes")
    
    # lint
    subparsers.add_parser("lint", help="Validate Wiki note frontmatter")
    
    # source-scan
    scan_parser = subparsers.add_parser("source-scan", help="List Raw sources")
    scan_parser.add_argument("--update", action="store_true", help="Update source manifest")
    scan_parser.add_argument("--accept-covered", action="store_true", help="Accept covered sources")
    
    # source-lint
    subparsers.add_parser("source-lint", help="Validate source frontmatter")
    
    # source-delta
    subparsers.add_parser("source-delta", help="Show sources not in manifest")
    
    # source-coverage
    subparsers.add_parser("source-coverage", help="Show source coverage")
    
    # search-catalog
    search_parser = subparsers.add_parser("search-catalog", help="Search catalog")
    search_parser.add_argument("--query", required=True, help="Search query")
    
    # log
    log_parser = subparsers.add_parser("log", help="Append log entry")
    log_parser.add_argument("--title", required=True, help="Log entry title")
    log_parser.add_argument("--details", required=True, help="Log entry details")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    vault_root = find_vault_root()
    
    commands = {
        "doctor": lambda: cmd_doctor(vault_root),
        "build": lambda: cmd_build(vault_root),
        "lint": lambda: cmd_lint(vault_root),
        "source-scan": lambda: cmd_source_scan(vault_root, args.update, args.accept_covered),
        "source-lint": lambda: cmd_source_lint(vault_root),
        "source-delta": lambda: cmd_source_delta(vault_root),
        "source-coverage": lambda: cmd_source_coverage(vault_root),
        "search-catalog": lambda: cmd_search_catalog(vault_root, args.query),
        "log": lambda: cmd_log(vault_root, args.title, args.details),
    }
    
    if args.command in commands:
        return commands[args.command]()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
