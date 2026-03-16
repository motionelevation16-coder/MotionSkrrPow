#!/bin/bash
# Motion Backup Script - backs up essential files to git

BACKUP_DIR="/home/ubuntu/.openclaw/workspace/backups/motion-core"
OPENCLAW_DIR="/home/ubuntu/.openclaw"
WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"

rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Copy essential files (no secrets)
echo "Backing up workspace files..."
cp "$WORKSPACE_DIR/SOUL.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/AGENTS.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/USER.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/IDENTITY.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/TOOLS.md" "$BACKUP_DIR/" 2>/dev/null
cp "$WORKSPACE_DIR/HEARTBEAT.md" "$BACKUP_DIR/" 2>/dev/null

# Memory files
mkdir -p "$BACKUP_DIR/memory"
cp "$WORKSPACE_DIR/memory/"*.md "$BACKUP_DIR/memory/" 2>/dev/null
cp "$WORKSPACE_DIR/memory/"*.json "$BACKUP_DIR/memory/" 2>/dev/null

# Projects (exclude heavy stuff)
mkdir -p "$BACKUP_DIR/projects"
rsync -av --exclude='node_modules' --exclude='venv' --exclude='.venv' --exclude='*.mp4' --exclude='*.mp3' --exclude='*.wav' --exclude='.git' --exclude='course' --exclude='__pycache__' "$WORKSPACE_DIR/projects/" "$BACKUP_DIR/projects/" 2>/dev/null

# Config (strip secrets)
cat "$OPENCLAW_DIR/openclaw.json" | sed 's/"botToken": "[^"]*"/"botToken": "REDACTED"/g' | sed 's/"apiKey": "[^"]*"/"apiKey": "REDACTED"/g' | sed 's/"token": "[^"]*"/"token": "REDACTED"/g' > "$BACKUP_DIR/openclaw.json.safe"

# Plugin list
ls -la "$OPENCLAW_DIR/extensions/" > "$BACKUP_DIR/installed-plugins.txt" 2>/dev/null

# Timestamp
echo "Last backup: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" > "$BACKUP_DIR/LAST_BACKUP.txt"

echo "Backup complete: $BACKUP_DIR"
du -sh "$BACKUP_DIR"
