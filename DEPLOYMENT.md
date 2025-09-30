# ClaudeGuard Deployment Guide

Complete guide for deploying ClaudeGuard globally or in your projects.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Global Installation](#global-installation)
- [Project-Specific Installation](#project-specific-installation)
- [Verification](#verification)
- [Uninstallation](#uninstallation)

---

## Installation Methods

### 1. Using the Installation Script (Recommended)

The easiest way to install ClaudeGuard:

```bash
cd claudeguard
./install.sh
```

**Interactive prompts:**
1. Choose installation type:
   - **Global (recommended)**: Installs to `~/.claudeguard`, creates `claudeguard` command
   - **Local**: Installs to current project only (`.claudeguard/`)
   - **Custom**: Specify your own location

2. Automatic setup:
   - Creates directory structure
   - Copies core files
   - Generates configuration
   - Sets up global command (for global install)

### 2. Using pip (Coming Soon)

```bash
# From PyPI (once published)
pip install claudeguard

# From GitHub
pip install git+https://github.com/yourusername/claudeguard.git

# From local source
cd claudeguard
pip install -e .
```

### 3. Manual Installation

For advanced users who want full control:

```bash
# 1. Clone repository
git clone https://github.com/yourusername/claudeguard.git
cd claudeguard

# 2. Copy to desired location
cp -r . ~/.claudeguard

# 3. Create global command
mkdir -p ~/.local/bin
cat > ~/.local/bin/claudeguard << 'EOF'
#!/bin/bash
CLAUDEGUARD_HOME="$HOME/.claudeguard"
python3 "$CLAUDEGUARD_HOME/cli/main.py" "$@"
EOF
chmod +x ~/.local/bin/claudeguard

# 4. Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Global Installation

Best for using ClaudeGuard across multiple projects.

### Steps

1. **Run installer:**
   ```bash
   ./install.sh
   ```

2. **Choose option 1** (Global installation)

3. **Verify PATH** (if prompted):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Test installation:**
   ```bash
   claudeguard status
   ```

### Directory Structure (Global)

```
~/.claudeguard/
├── core/
│   └── guard.py
├── cli/
│   └── main.py
├── storage/
│   ├── backups/
│   └── logs/
└── config.yaml

~/.local/bin/
└── claudeguard          # Global command
```

### Usage (Global)

From any directory:

```bash
claudeguard status
claudeguard list
claudeguard rollback
```

ClaudeGuard will work on the current project directory automatically.

---

## Project-Specific Installation

Best for isolated project environments or testing.

### Steps

1. **Navigate to your project:**
   ```bash
   cd /path/to/your/project
   ```

2. **Run installer:**
   ```bash
   /path/to/claudeguard/install.sh
   ```

3. **Choose option 2** (Local installation)

4. **Use project-specific command:**
   ```bash
   python3 .claudeguard/cli/main.py status
   ```

### Directory Structure (Project-Local)

```
your-project/
├── .claudeguard/
│   ├── core/
│   ├── cli/
│   ├── storage/
│   │   ├── backups/
│   │   └── logs/
│   └── config.yaml
├── your_code.py
└── ...
```

### Usage (Project-Local)

From project root:

```bash
python3 .claudeguard/cli/main.py status
python3 .claudeguard/cli/main.py list

# Or create alias
alias cguard="python3 .claudeguard/cli/main.py"
cguard status
```

---

## Verification

### 1. Check Installation

```bash
# For global installation
claudeguard --help

# Check version (coming soon)
claudeguard version
```

### 2. Verify Components

```bash
# Check status
claudeguard status

# Expected output:
# Status: ✅ Enabled
# Total Backups: 0
# Total Operations: 0
```

### 3. Test Backup & Rollback

```bash
# Create test file
echo "test" > test.txt

# Create backup manually (using Python)
python3 -c "
import sys
sys.path.insert(0, '$HOME/.claudeguard')
from core.guard import ClaudeGuard
guard = ClaudeGuard()
backup_id = guard.create_backup('Write', {'file': 'test.txt'}, ['test.txt'])
print(f'Created backup: {backup_id}')
"

# List backups
claudeguard list

# Modify file
echo "modified" > test.txt

# Rollback
claudeguard rollback

# Check file
cat test.txt  # Should show "test"
```

---

## Configuration

### Global Config

Edit `~/.claudeguard/config.yaml`:

```yaml
backup:
  enabled: true
  max_backups: 100
  retention_days: 30
  auto_cleanup: true

risk_detection:
  enabled: true
  warn_on_high_risk: true

verification:
  auto_verify: false
  compliance_threshold: 100

storage:
  compression: false
  encryption: false
```

### Project-Specific Config

Override global settings in your project:

```bash
mkdir -p .claudeguard
cat > .claudeguard/config.yaml << 'EOF'
backup:
  max_backups: 50
  retention_days: 7

exclude:
  - node_modules/
  - .git/
  - "*.log"
EOF
```

---

## Integration with Claude Code

### Option 1: Automatic Hooks (Recommended)

Create `.claude/hooks/before_operation.sh`:

```bash
#!/bin/bash
# Automatically backup before Claude operations

OPERATION_TYPE="$1"
OPERATION_DETAILS="$2"
AFFECTED_FILES="$3"

python3 -c "
import sys, json
sys.path.insert(0, '$HOME/.claudeguard')
from core.guard import ClaudeGuard

guard = ClaudeGuard()
details = json.loads('$OPERATION_DETAILS')
files = '$AFFECTED_FILES'.split(',') if '$AFFECTED_FILES' else []

backup_id = guard.create_backup('$OPERATION_TYPE', details, files)
print(f'✅ Backup created: {backup_id}')
"
```

Make it executable:
```bash
chmod +x .claude/hooks/before_operation.sh
```

### Option 2: Manual Integration

In your workflow, call ClaudeGuard before risky operations:

```python
from claudeguard import ClaudeGuard

guard = ClaudeGuard()

# Before letting Claude edit files
backup_id = guard.create_backup(
    operation_type='Edit',
    operation_details={'file': 'important.py', 'reason': 'refactoring'},
    affected_files=['important.py']
)

# Do operations...

# Rollback if needed
if something_went_wrong:
    guard.rollback(backup_id)
```

---

## Upgrading

### From pip (Coming Soon)

```bash
pip install --upgrade claudeguard
```

### Manual Upgrade

```bash
# Backup current config
cp ~/.claudeguard/config.yaml ~/claudeguard_config_backup.yaml

# Pull latest changes
cd /path/to/claudeguard
git pull

# Reinstall
./install.sh

# Restore config if needed
cp ~/claudeguard_config_backup.yaml ~/.claudeguard/config.yaml
```

---

## Uninstallation

### For Global Installation

```bash
# Remove files
rm -rf ~/.claudeguard
rm ~/.local/bin/claudeguard

# Remove from PATH (edit ~/.bashrc or ~/.zshrc)
# Remove line: export PATH="$HOME/.local/bin:$PATH"
```

### For Local Installation

```bash
# From project root
rm -rf .claudeguard
```

### Clean All Data

```bash
# Backup data first!
cp -r ~/.claudeguard/storage/backups ~/claudeguard_backups_archive

# Remove everything
rm -rf ~/.claudeguard
```

---

## Troubleshooting

### "claudeguard: command not found"

**Solution 1:** Add to PATH
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Solution 2:** Use full path
```bash
~/.local/bin/claudeguard status
```

**Solution 3:** Create alias
```bash
echo 'alias claudeguard="python3 ~/.claudeguard/cli/main.py"' >> ~/.bashrc
source ~/.bashrc
```

### "ModuleNotFoundError: No module named 'core'"

**Cause:** Python can't find ClaudeGuard modules

**Solution:**
```bash
# Check installation
ls -la ~/.claudeguard/core/

# Fix Python path in global command
cat > ~/.local/bin/claudeguard << 'EOF'
#!/bin/bash
export PYTHONPATH="$HOME/.claudeguard:$PYTHONPATH"
python3 "$HOME/.claudeguard/cli/main.py" "$@"
EOF
```

### Permission Denied

**Solution:**
```bash
chmod +x ~/.local/bin/claudeguard
chmod +x ~/.claudeguard/cli/main.py
```

### Backups Not Working

**Check 1:** Is ClaudeGuard enabled?
```bash
claudeguard status
```

**Check 2:** Is backup directory writable?
```bash
ls -la ~/.claudeguard/storage/
```

**Check 3:** Check logs
```bash
cat ~/.claudeguard/storage/logs/operation_history.jsonl
```

---

## Platform-Specific Notes

### macOS

- Default shell: zsh
- Config file: `~/.zshrc`
- Works out of the box

### Linux

- Default shell: bash
- Config file: `~/.bashrc`
- May need to install `python3-pip`

### Windows (Git Bash)

- Use Git Bash terminal
- PATH setup may differ
- Config file: `~/.bashrc`

---

## Next Steps

After successful deployment:

1. **Test the system:** Run `claudeguard verify`
2. **Integrate with Claude:** Set up hooks or manual calls
3. **Monitor usage:** Check `claudeguard cost` periodically
4. **Join community:** Discord, GitHub discussions

---

**Questions?**

- 📧 Email: support@claudeguard.dev
- 💬 Discord: https://discord.gg/claudeguard
- 📖 Docs: https://docs.claudeguard.dev
- 🐛 Issues: https://github.com/yourusername/claudeguard/issues