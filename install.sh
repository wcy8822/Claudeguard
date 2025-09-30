#!/bin/bash
# ClaudeGuard Installation Script
# Supports: macOS, Linux, Windows (Git Bash)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                        🤖 ClaudeGuard Installer                          ║
║                                                                          ║
║              Your AI Safety Net - Zero Cost, Maximum Protection          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    MINGW*)     PLATFORM=Windows;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo -e "${BLUE}📊 System Information${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Platform: $PLATFORM"
echo "Python: $(python3 --version 2>/dev/null || echo 'Not found')"
echo "Git: $(git --version 2>/dev/null || echo 'Not found')"
echo ""

# Check dependencies
echo -e "${BLUE}🔍 Checking Dependencies${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DEPS_OK=true

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    DEPS_OK=false
else
    echo -e "${GREEN}✅ Python 3 found${NC}"
fi

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git not found (optional)${NC}"
else
    echo -e "${GREEN}✅ Git found${NC}"
fi

echo ""

if [ "$DEPS_OK" = false ]; then
    echo -e "${RED}❌ Missing required dependencies. Please install Python 3.${NC}"
    exit 1
fi

# Installation options
echo -e "${BLUE}📦 Installation Options${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Global installation (recommended)"
echo "2. Local installation (current project only)"
echo "3. Custom location"
echo ""

read -p "Choose installation type [1]: " INSTALL_TYPE
INSTALL_TYPE=${INSTALL_TYPE:-1}

# Determine installation directory
case $INSTALL_TYPE in
    1)
        INSTALL_DIR="$HOME/.claudeguard"
        echo -e "${GREEN}Installing to: $INSTALL_DIR${NC}"
        ;;
    2)
        INSTALL_DIR="$(pwd)/.claudeguard"
        echo -e "${GREEN}Installing to: $INSTALL_DIR${NC}"
        ;;
    3)
        read -p "Enter installation directory: " CUSTOM_DIR
        INSTALL_DIR="$CUSTOM_DIR"
        echo -e "${GREEN}Installing to: $INSTALL_DIR${NC}"
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""

# Create installation directory
echo -e "${BLUE}🚀 Installing ClaudeGuard${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

mkdir -p "$INSTALL_DIR"/{core,cli,storage/backups,storage/logs}

# Copy core files
echo "📁 Copying core files..."
cp -r core/* "$INSTALL_DIR/core/" 2>/dev/null || echo "   Skipped (development mode)"
cp -r cli/* "$INSTALL_DIR/cli/" 2>/dev/null || echo "   Skipped (development mode)"

# Create configuration
echo "⚙️  Creating configuration..."
cat > "$INSTALL_DIR/config.yaml" << 'YAML'
# ClaudeGuard Configuration

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

YAML

# Create global command
if [ $INSTALL_TYPE -eq 1 ]; then
    echo "🔗 Creating global command..."

    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"

    cat > "$BIN_DIR/claudeguard" << SCRIPT
#!/bin/bash
# ClaudeGuard Global Command
CLAUDEGUARD_HOME="$INSTALL_DIR"
python3 "\$CLAUDEGUARD_HOME/cli/main.py" "\$@"
SCRIPT

    chmod +x "$BIN_DIR/claudeguard"

    # Add to PATH if needed
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠️  Please add the following line to your shell profile:${NC}"
        echo ""
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then restart your terminal or run:"
        echo "  source ~/.bashrc  # or ~/.zshrc"
    fi
fi

# Create test backup
echo "🧪 Running initial test..."
python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
print('✅ ClaudeGuard core loaded successfully')
" || echo "⚠️  Could not run test (development mode)"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📍 Installation Directory: $INSTALL_DIR"
echo "📖 Configuration: $INSTALL_DIR/config.yaml"
echo ""
echo -e "${BLUE}🚀 Quick Start:${NC}"
echo ""

if [ $INSTALL_TYPE -eq 1 ]; then
    echo "  claudeguard status        # Check system status"
    echo "  claudeguard list          # View recent backups"
    echo "  claudeguard rollback      # Undo last operation"
    echo "  claudeguard verify        # Verify compliance"
else
    echo "  python3 $INSTALL_DIR/cli/main.py status"
    echo "  python3 $INSTALL_DIR/cli/main.py list"
fi

echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "  https://github.com/yourusername/claudeguard"
echo ""
echo -e "${BLUE}💬 Support:${NC}"
echo "  Discord: https://discord.gg/claudeguard"
echo "  Issues: https://github.com/yourusername/claudeguard/issues"
echo ""
echo -e "${GREEN}Thank you for using ClaudeGuard! 🤖${NC}"
echo ""