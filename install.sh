#!/bin/bash
set -e

SKILL_NAME="travel-planner"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME/.gemini/config/skills/$SKILL_NAME"

echo "======================================================"
echo "🚀 Installing Antigravity Skill: $SKILL_NAME"
echo "Source: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"
echo "======================================================"

mkdir -p "$HOME/.gemini/config/skills"

if [ "$1" == "--copy" ]; then
    rm -rf "$TARGET_DIR"
    cp -R "$SCRIPT_DIR" "$TARGET_DIR"
    echo "✅ Skill copied successfully to $TARGET_DIR"
else
    rm -rf "$TARGET_DIR"
    ln -s "$SCRIPT_DIR" "$TARGET_DIR"
    echo "✅ Skill symlinked successfully to $TARGET_DIR"
fi

echo "🎉 Installation complete! The '$SKILL_NAME' skill is now active in Antigravity."
