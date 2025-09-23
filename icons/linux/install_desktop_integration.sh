#!/bin/bash
# xharvester Linux Desktop Integration Installer
# Creates desktop shortcuts and system integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XHARVESTER_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
CURRENT_USER="${SUDO_USER:-$USER}"

echo "🚀 Installing xharvester Desktop Integration for Linux..."
echo "   User: $CURRENT_USER"
echo "   xharvester path: $XHARVESTER_ROOT"

# Check if running as root for system-wide installation
if [[ $EUID -eq 0 ]]; then
    echo "📋 Installing system-wide (requires root)..."
    INSTALL_MODE="system"
    ICON_DIR="/usr/local/share/icons"
    DESKTOP_DIR="/usr/local/share/applications"
    BIN_DIR="/usr/local/bin"
else
    echo "📋 Installing for current user only..."
    INSTALL_MODE="user"
    ICON_DIR="$HOME/.local/share/icons"
    DESKTOP_DIR="$HOME/.local/share/applications"
    BIN_DIR="$HOME/.local/bin"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p "$ICON_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$BIN_DIR"

# Copy icon
echo "🎨 Installing icons..."
cp "$SCRIPT_DIR/../xharvester.png" "$ICON_DIR/"
cp "$SCRIPT_DIR/../xharvester_64.png" "$ICON_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/../xharvester_128.png" "$ICON_DIR/" 2>/dev/null || true

# Create/update desktop file with correct paths
echo "🖥️  Creating desktop entry..."
sed "s|/usr/local/bin/xharvester|$XHARVESTER_ROOT/xharvester|g; s|/usr/local/share/icons/xharvester.png|$ICON_DIR/xharvester.png|g" \
    "$SCRIPT_DIR/xharvester.desktop" > "$DESKTOP_DIR/xharvester.desktop"

# Make desktop file executable
chmod +x "$DESKTOP_DIR/xharvester.desktop"

# Create symbolic link for command-line access
echo "🔗 Creating symbolic link..."
if [[ $INSTALL_MODE == "system" ]]; then
    ln -sf "$XHARVESTER_ROOT/xharvester" "$BIN_DIR/xharvester"
else
    ln -sf "$XHARVESTER_ROOT/xharvester" "$BIN_DIR/xharvester"
    # Add to PATH if not already there
    if ! echo "$PATH" | grep -q "$BIN_DIR"; then
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
        echo "⚠️  Added ~/.local/bin to PATH in .bashrc - restart terminal or run: source ~/.bashrc"
    fi
fi

# Update desktop database
echo "🔄 Updating desktop database..."
if command -v update-desktop-database >/dev/null 2>&1; then
    if [[ $INSTALL_MODE == "system" ]]; then
        update-desktop-database /usr/local/share/applications/
    else
        update-desktop-database "$HOME/.local/share/applications/"
    fi
fi

# Update icon cache
echo "🎨 Updating icon cache..."
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    if [[ $INSTALL_MODE == "system" ]]; then
        gtk-update-icon-cache -f -t /usr/local/share/icons/ 2>/dev/null || true
    else
        gtk-update-icon-cache -f -t "$HOME/.local/share/icons/" 2>/dev/null || true
    fi
fi

echo ""
echo "✅ xharvester Desktop Integration installed successfully!"
echo ""
echo "📋 Installation Summary:"
echo "   Mode: $INSTALL_MODE"
echo "   Icons: $ICON_DIR/"
echo "   Desktop: $DESKTOP_DIR/"
echo "   Binary: $BIN_DIR/"
echo ""
echo "🚀 Usage:"
echo "   • Find 'xharvester' in your application launcher"
echo "   • Right-click for 'Run as Root' option"
echo "   • Command line: xharvester (after PATH update)"
echo ""
echo "🔧 To uninstall:"
echo "   sudo rm -f $DESKTOP_DIR/xharvester.desktop"
echo "   sudo rm -f $ICON_DIR/xharvester*.png"
echo "   sudo rm -f $BIN_DIR/xharvester"
echo ""