# ClaudeGuard Quick Start

Get up and running with ClaudeGuard in 2 minutes! ⚡

## Installation

### Method 1: Using the Installer (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/claudeguard.git
cd claudeguard

# Run installer
./install.sh
```

The installer will:
1. Check dependencies (Python 3.8+)
2. Ask for installation location (global/local/custom)
3. Set up configuration
4. Create the `claudeguard` command

### Method 2: Using pip (Coming Soon)

```bash
pip install claudeguard
```

## First Steps

### 1. Check Status

```bash
claudeguard status
```

You should see:
```
🤖 ClaudeGuard - Your AI Safety Net
======================================================================

📊 System Status
----------------------------------------------------------------------
Status: ✅ Enabled
Total Backups: 0
Total Operations: 0
Storage Used: 0.00 MB
```

### 2. Let Claude Work

Now just use Claude Code as normal. ClaudeGuard automatically backs up every operation!

```bash
# Example: Let Claude edit a file
$ claude "Add a function to calculate fibonacci numbers"

# ClaudeGuard automatically creates backup before the edit
```

### 3. View Backups

```bash
claudeguard list
```

Output:
```
📋 Recent Backups (showing 3 of 10)
----------------------------------------------------------------------
 1. 🟡 Edit            |  1 files | 20250930_160000
    ID: backup_20250930_160000_123456
    Git: abc123f

 2. 🟢 Write           |  1 files | 20250930_155500
    ID: backup_20250930_155500_654321
```

### 4. Rollback if Needed

```bash
# Undo most recent operation
claudeguard rollback

# Or undo specific operation
claudeguard rollback backup_20250930_160000_123456
```

## Common Commands

```bash
# Show system status
claudeguard status

# List recent backups (default: 10)
claudeguard list
claudeguard list 20        # Show 20 backups

# Rollback operations
claudeguard rollback       # Rollback latest
claudeguard rollback ID    # Rollback specific

# Verify compliance
claudeguard verify

# Clean up old backups
claudeguard cleanup        # Keep default (100)
claudeguard cleanup 50     # Keep only 50

# Cost analysis
claudeguard cost

# Help
claudeguard help
```

## Configuration

### Default Configuration

ClaudeGuard works out of the box with sensible defaults:

```yaml
backup:
  enabled: true
  max_backups: 100
  retention_days: 30
  auto_cleanup: true

risk_detection:
  enabled: true
  warn_on_high_risk: true
```

### Customization

Edit the config file:

```bash
# Global config
nano ~/.claudeguard/config.yaml

# Project-specific config
nano .claudeguard/config.yaml
```

## Real-World Example

Let's say you're refactoring code:

```bash
# 1. Start with clean slate
$ claudeguard status
Status: ✅ Enabled, 5 backups

# 2. Let Claude do major refactoring
$ claude "Refactor all database queries to use async/await"

# 3. Test the changes
$ python -m pytest
# Oops, tests fail!

# 4. Instant rollback
$ claudeguard rollback
✅ Restored 12 files from backup_20250930_160000
🎉 Rollback complete!

# 5. Try again with different approach
$ claude "Refactor database queries one file at a time, starting with models.py"
```

## Integration with Git

ClaudeGuard automatically captures Git state:

```bash
# View backups with Git info
claudeguard list --show-git

# Each backup includes:
# - Current commit hash
# - Branch name
# - Uncommitted changes snapshot
```

## Troubleshooting

### "claudeguard: command not found"

Add to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Backups Not Being Created

Check if ClaudeGuard is enabled:

```bash
claudeguard status
```

If disabled, edit config:

```yaml
backup:
  enabled: true
```

### Storage Growing Too Large

Clean up old backups:

```bash
# Keep only 50 most recent
claudeguard cleanup 50

# Or adjust config
nano ~/.claudeguard/config.yaml
# Set max_backups: 50
```

## Next Steps

- Read the [Full Documentation](README.md)
- Learn about [Advanced Features](docs/ADVANCED.md)
- Join our [Discord Community](https://discord.gg/claudeguard)
- Star the project on [GitHub](https://github.com/yourusername/claudeguard) ⭐

## FAQ

**Q: Does ClaudeGuard slow down Claude?**
A: No! Backup creation takes < 50ms, completely imperceptible.

**Q: How much storage does it use?**
A: Minimal! ~50 KB per 100 operations with auto-cleanup.

**Q: Can I use it with other AI tools?**
A: Currently Claude Code only. Support for Cursor, Copilot coming in v2.0!

**Q: Is my data safe?**
A: Yes! Everything is stored locally. No cloud, no tracking, no telemetry.

**Q: Is it really free?**
A: 100% free and open source. Forever.

---

**Need Help?**

- 📧 Email: support@claudeguard.dev
- 💬 Discord: https://discord.gg/claudeguard
- 🐛 Issues: https://github.com/yourusername/claudeguard/issues

**Happy Coding with Your AI Safety Net!** 🤖🛡️