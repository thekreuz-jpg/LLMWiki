#!/bin/bash
# install_hooks.sh — install git hooks for the LLM Wiki vault

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Installing git hooks..."

# Create hooks directory if needed
mkdir -p "$VAULT_ROOT/.githooks"

# Install pre-commit hook
cp "$SCRIPT_DIR/../.githooks/pre-commit" "$VAULT_ROOT/.git/hooks/pre-commit"
chmod +x "$VAULT_ROOT/.git/hooks/pre-commit"

echo "Git hooks installed successfully."
echo ""
echo "The pre-commit hook will run:"
echo "  python3 scripts/wiki_tool.py build"
echo "  python3 scripts/wiki_tool.py lint"
echo "  python3 scripts/wiki_tool.py source-lint"
echo ""
echo "To bypass the hook in an emergency, use: git commit --no-verify"
