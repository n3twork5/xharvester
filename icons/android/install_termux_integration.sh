#!/data/data/com.termux/files/usr/bin/bash
# xharvester Android/Termux Integration Installer
# Creates shortcuts and command-line integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XHARVESTER_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "🚀 Installing xharvester Integration for Android/Termux..."
echo "   xharvester path: $XHARVESTER_ROOT"
echo "   Termux prefix: $PREFIX"

# Check if running in Termux
if [[ ! -d "$PREFIX" ]]; then
    echo "❌ This script is designed for Termux environment"
    echo "   Please run this in Termux app on Android"
    exit 1
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p "$PREFIX/bin"
mkdir -p "$PREFIX/share/applications"
mkdir -p "$PREFIX/share/icons"
mkdir -p "$HOME/.shortcuts"

# Copy icons
echo "🎨 Installing icons..."
cp "$SCRIPT_DIR/../xharvester.png" "$PREFIX/share/icons/" 2>/dev/null || true
cp "$SCRIPT_DIR/../xharvester_64.png" "$PREFIX/share/icons/" 2>/dev/null || true
cp "$SCRIPT_DIR/../xharvester_128.png" "$PREFIX/share/icons/" 2>/dev/null || true

# Create symbolic link for command-line access
echo "🔗 Creating command-line integration..."
ln -sf "$XHARVESTER_ROOT/xharvester" "$PREFIX/bin/xharvester"
chmod +x "$PREFIX/bin/xharvester"

# Create Termux desktop shortcut (for home screen)
echo "🖥️  Creating Termux widget shortcut..."
cat > "$HOME/.shortcuts/xharvester" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# xharvester Termux Shortcut
cd "$HOME/Desktop/xharvester" 2>/dev/null || cd "$HOME/xharvester" 2>/dev/null || cd "$(find $HOME -name xharvester -type d | head -1)"
exec ./xharvester "$@"
EOF

chmod +x "$HOME/.shortcuts/xharvester"

# Create root version shortcut (if tsu is available)
if command -v tsu >/dev/null 2>&1; then
    echo "🔐 Creating root shortcut (tsu detected)..."
    cat > "$HOME/.shortcuts/xharvester-root" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# xharvester Root Shortcut (uses tsu)
cd "$HOME/Desktop/xharvester" 2>/dev/null || cd "$HOME/xharvester" 2>/dev/null || cd "$(find $HOME -name xharvester -type d | head -1)"
exec tsu -c "./xharvester $*"
EOF
    chmod +x "$HOME/.shortcuts/xharvester-root"
fi

# Create desktop entry (for file managers that support it)
echo "📋 Creating desktop entry..."
cat > "$PREFIX/share/applications/xharvester.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=xharvester
Comment=Extended Reconnaissance & Exploitation Toolkit
Comment[en]=Cross-platform security testing framework for Android/Termux
Exec=$PREFIX/bin/xharvester
Icon=$PREFIX/share/icons/xharvester.png
Terminal=true
Categories=Development;Security;Network;System;
Keywords=security;hacking;penetration;testing;bluetooth;wifi;automobile;rf;scada;android;termux;
StartupNotify=false
Path=$XHARVESTER_ROOT
EOF

# Create launch script with proper environment
echo "🔧 Creating launch script..."
cat > "$PREFIX/bin/xharvester-launch" << EOF
#!/data/data/com.termux/files/usr/bin/bash
# xharvester Launch Script for Termux
# Sets up proper environment and launches xharvester

# Set environment variables
export TERM=xterm-256color
export COLORTERM=truecolor
export FORCE_COLOR=1

# Navigate to xharvester directory
cd "$XHARVESTER_ROOT" || {
    echo "❌ Could not find xharvester directory"
    exit 1
}

# Check if running as root is needed
if [[ "\$1" == "--root" ]] && command -v tsu >/dev/null 2>&1; then
    echo "🔐 Launching xharvester with root privileges..."
    exec tsu -c "./xharvester"
else
    echo "🚀 Launching xharvester..."
    exec ./xharvester
fi
EOF

chmod +x "$PREFIX/bin/xharvester-launch"

# Install additional dependencies if needed
echo "📦 Checking dependencies..."
MISSING_DEPS=""

# Check for Python
if ! command -v python3 >/dev/null 2>&1; then
    MISSING_DEPS="$MISSING_DEPS python"
fi

# Check for essential packages
for pkg in curl wget git; do
    if ! command -v "$pkg" >/dev/null 2>&1; then
        MISSING_DEPS="$MISSING_DEPS $pkg"
    fi
done

if [[ -n "$MISSING_DEPS" ]]; then
    echo "⚠️  Missing dependencies detected: $MISSING_DEPS"
    echo "📦 Install with: pkg install$MISSING_DEPS"
fi

# Create alias for easy access
echo "🔗 Creating shell aliases..."
ALIAS_LINE="alias xharvester='$PREFIX/bin/xharvester'"
ROOT_ALIAS_LINE="alias xharvester-root='$PREFIX/bin/xharvester-launch --root'"

# Add to both bash and zsh if they exist
for shell_rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [[ -f "$shell_rc" ]] || [[ "$shell_rc" == "$HOME/.bashrc" ]]; then
        if ! grep -q "alias xharvester=" "$shell_rc" 2>/dev/null; then
            echo "$ALIAS_LINE" >> "$shell_rc"
            if command -v tsu >/dev/null 2>&1; then
                echo "$ROOT_ALIAS_LINE" >> "$shell_rc"
            fi
        fi
    fi
done

echo ""
echo "✅ xharvester Android/Termux Integration installed successfully!"
echo ""
echo "📋 Installation Summary:"
echo "   Command-line: $PREFIX/bin/xharvester"
echo "   Shortcuts: $HOME/.shortcuts/xharvester*"
echo "   Icons: $PREFIX/share/icons/"
echo "   Desktop entry: $PREFIX/share/applications/"
echo ""
echo "🚀 Usage Methods:"
echo "   1. Command line: xharvester"
echo "   2. Termux widget: Add 'xharvester' shortcut to home screen"
if command -v tsu >/dev/null 2>&1; then
echo "   3. Root mode: xharvester-root (requires tsu)"
fi
echo "   4. Direct launch: $PREFIX/bin/xharvester-launch"
echo ""
echo "📱 Termux Widget Setup:"
echo "   1. Install 'Termux:Widget' app from F-Droid or Google Play"
echo "   2. Add Termux widget to home screen"
echo "   3. Select 'xharvester' from the shortcut list"
echo ""
if [[ -n "$MISSING_DEPS" ]]; then
echo "⚠️  Install missing dependencies:"
echo "   pkg update && pkg install$MISSING_DEPS"
echo ""
fi
echo "🔧 To uninstall:"
echo "   rm -f $PREFIX/bin/xharvester*"
echo "   rm -f $HOME/.shortcuts/xharvester*"
echo "   rm -f $PREFIX/share/applications/xharvester.desktop"
echo "   rm -f $PREFIX/share/icons/xharvester*.png"
echo ""