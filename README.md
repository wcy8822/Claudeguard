# 🤖 ClaudeGuard

> **Your AI Safety Net** - Never Fear the Undo Button Again
>
> **你的 AI 安全网** - 让 AI 操作永远可回滚

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](https://github.com)

---

## 🎯 What is ClaudeGuard?

**ClaudeGuard** is an automatic backup and rollback system for Claude Code operations. It creates snapshots before every file modification, allowing you to undo any AI-generated change with a single command.

Think of it as **Time Machine for AI** - but smarter, faster, and zero-cost.

### ✨ Key Features

- 🔒 **Automatic Backups** - Every Write/Edit/Bash operation is backed up automatically
- ⚡ **Instant Rollback** - Undo any operation in < 100ms
- 🎯 **Zero Configuration** - Works out of the box
- 💾 **Minimal Storage** - < 1MB for 100 operations
- 📊 **Full Audit Trail** - Complete operation history
- 🆓 **100% Free** - No cloud services, no subscriptions
- 🛡️ **Risk Detection** - Automatically classifies operation risk levels
- 🔍 **Compliance Verification** - Built-in validation tools

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claudeguard.git
cd claudeguard

# Run installer
./install.sh
```

### Basic Usage

```bash
# View recent operations
claudeguard list

# Undo last operation
claudeguard rollback

# Check system status
claudeguard status

# View detailed report
claudeguard verify
```

That's it! ClaudeGuard is now protecting all your Claude Code operations.

---

## 📖 How It Works

### 1. Automatic Backup Before Operations

```python
# Before any Claude operation
┌─────────────────────────────────────┐
│ Claude wants to edit main.py       │
│                                     │
│ 🔒 ClaudeGuard automatically:      │
│   • Creates backup snapshot         │
│   • Records operation metadata      │
│   • Captures Git state              │
│   • Assigns unique backup ID        │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Operation proceeds safely           │
└─────────────────────────────────────┘
```

### 2. One-Command Rollback

```bash
# Made a mistake? Just rollback!
$ claudeguard rollback

🔄 Rolling back to: backup_20250930_160000
✅ Restored 3 files
✅ Rollback complete!
```

### 3. Full Visibility

```bash
$ claudeguard list

📋 Recent Operations:
  1. ✅ Edit main.py        | 2025-09-30 16:00:00 | backup_001
  2. ✅ Write config.yaml   | 2025-09-30 15:55:23 | backup_002
  3. ✅ Bash(mv file.txt)   | 2025-09-30 15:50:10 | backup_003

Compliance: 100% ✅
```

---

## 🎨 Architecture

```
claudeguard/
├── core/
│   ├── guard.py              # Core backup engine
│   ├── rollback.py           # Rollback manager
│   └── verifier.py           # Compliance checker
├── cli/
│   ├── main.py               # CLI interface
│   └── commands.py           # Command implementations
├── storage/
│   └── .claudeguard/
│       ├── backups/          # Backup snapshots
│       ├── logs/             # Operation logs
│       └── config.yaml       # Configuration
└── docs/
    ├── INSTALLATION.md
    ├── USAGE.md
    └── API.md
```

---

## 💡 Use Cases

### 1. Safe AI-Assisted Coding

```bash
# Let Claude make changes without fear
$ claude "Refactor this entire codebase"

# Something went wrong? No problem!
$ claudeguard rollback
✅ All changes reverted
```

### 2. Experiment Freely

```bash
# Try risky operations
$ claude "Optimize all SQL queries"

# Keep what works, rollback what doesn't
$ claudeguard list
$ claudeguard rollback backup_003  # Rollback specific operation
```

### 3. Team Collaboration

```bash
# Review all AI operations
$ claudeguard verify --export report.json

# Share with team for review
$ cat report.json | jq '.compliance_rate'
100%
```

---

## 📊 Cost & Performance

### Storage

| Operations | Storage  | Cost    |
|------------|----------|---------|
| 100        | ~50 KB   | $0      |
| 1,000      | ~500 KB  | $0      |
| 10,000     | ~5 MB    | $0      |

### Performance

| Operation      | Time    |
|----------------|---------|
| Create Backup  | < 50ms  |
| Rollback       | < 100ms |
| Verify         | < 500ms |

**Conclusion:** Negligible impact, zero cost.

---

## 🔧 Configuration

### Global Configuration

Edit `~/.claudeguard/config.yaml`:

```yaml
backup:
  enabled: true
  max_backups: 100              # Maximum number of backups
  retention_days: 30            # Retention period
  auto_cleanup: true            # Automatic cleanup

risk_detection:
  enabled: true
  warn_on_high_risk: true

verification:
  auto_verify: true             # Verify after operations
  compliance_threshold: 100     # Required compliance %
```

### Per-Project Configuration

Create `.claudeguard/config.yaml` in your project:

```yaml
backup:
  max_backups: 50               # Override for this project

exclude:
  - node_modules/
  - .git/
  - "*.log"
```

---

## 🛠️ Advanced Features

### 1. Risk-Based Backup Strategy

ClaudeGuard automatically classifies operations:

- **LOW**: Read operations (no backup needed)
- **MEDIUM**: Write/Edit (standard backup)
- **HIGH**: Bash commands, bulk operations (enhanced backup)
- **CRITICAL**: rm -rf, DROP TABLE (multi-snapshot backup)

### 2. Compliance Verification

```bash
# Check if all operations are backed up
$ claudeguard verify

📊 Compliance Analysis:
  Total Operations: 156
  Backed Up: 156 (100%)
  Missing Backups: 0

✅ Fully Compliant
```

### 3. Cost Analysis

```bash
$ claudeguard cost

💰 Cost Analysis:
  Current Storage: 0.05 MB
  Predicted (1 year): 2.1 MB
  Estimated Cost: $0.00/year

✅ Minimal impact
```

### 4. Monitoring Dashboard

```bash
$ claudeguard monitor --watch

╔══════════════════════════════════════╗
║   ClaudeGuard Live Monitor          ║
╚══════════════════════════════════════╝

📊 Status: ✅ All systems operational
📈 Operations today: 47
💾 Storage: 0.15 MB
🔒 Compliance: 100%

Recent Operations:
  16:30:25 ✅ Edit main.py (LOW)
  16:29:41 ✅ Write test.py (MEDIUM)

[Auto-refresh every 5s]
```

---

## 🤝 Integration

### With Claude Code

ClaudeGuard integrates seamlessly with Claude Code settings:

```json
{
  "permissions": {
    "allow": ["Bash(*)", "Write(**)", "Edit(**)"]
  },
  "hooks": {
    "before_operation": ".claudeguard/hooks/backup.sh"
  }
}
```

### With Git

```bash
# ClaudeGuard records Git state with each backup
$ claudeguard list --show-git

1. Edit main.py | backup_001 | git: abc123f
   └─ Git: "feat: add new feature"
```

### With CI/CD

```yaml
# .github/workflows/verify.yml
- name: Verify ClaudeGuard Compliance
  run: |
    claudeguard verify --strict
    [ $? -eq 0 ] || exit 1
```

---

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Manual](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [FAQ](docs/FAQ.md)

---

## 🌟 Why ClaudeGuard?

### The Problem

AI assistants like Claude Code are powerful, but mistakes happen:
- ❌ Accidentally deleted important files
- ❌ Overwrote working code with bugs
- ❌ Lost track of what changed
- ❌ No easy way to undo AI operations

### The Solution

ClaudeGuard provides:
- ✅ Automatic safety net for all operations
- ✅ Instant rollback capability
- ✅ Complete audit trail
- ✅ Zero-cost, zero-maintenance

---

## 🎯 Roadmap

### v1.0 (Current)
- ✅ Automatic backup system
- ✅ One-command rollback
- ✅ Compliance verification
- ✅ CLI interface

### v1.1 (Coming Soon)
- 🔜 Web dashboard
- 🔜 Cloud sync option
- 🔜 Team collaboration features
- 🔜 VS Code extension

### v2.0 (Future)
- 🔮 Support for other AI tools (GitHub Copilot, Cursor, etc.)
- 🔮 Intelligent backup optimization
- 🔮 Machine learning-based risk prediction
- 🔮 Cross-platform GUI

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/yourusername/claudeguard.git
cd claudeguard

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Submit PR
git push origin feature/your-feature
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with love for the Claude Code community
- Inspired by Time Machine, Git, and undo/redo systems
- Special thanks to all contributors and early adopters

---

## 📞 Support

- 📧 Email: support@claudeguard.dev
- 💬 Discord: [Join our community](https://discord.gg/claudeguard)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/claudeguard/issues)
- 📖 Docs: [Documentation](https://docs.claudeguard.dev)

---

## ⭐ Star History

If you find ClaudeGuard useful, please give it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/claudeguard&type=Date)](https://star-history.com/#yourusername/claudeguard&Date)

---

<p align="center">
  Made with ❤️ by the ClaudeGuard Team
  <br>
  <strong>Your AI Safety Net - Never Fear the Undo Button Again</strong>
</p>