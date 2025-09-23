#!/bin/bash
# xharvester iOS/a-Shell Installation Script
# Compatible with a-Shell and iSH apps on iOS

set -e

echo "🍎 xharvester iOS/a-Shell Installation Script"
echo "   Compatible with a-Shell, a-Shell mini, and iSH"

# Detect iOS shell environment
if [[ -n "$SSH_CONNECTION" ]] && [[ "$(uname)" == "Darwin" ]]; then
    ENV_TYPE="ssh_ios"
    echo "   Environment: SSH connection to iOS"
elif [[ -n "$PREFIX" ]] && [[ "$PREFIX" == "/private/var/mobile"* ]]; then
    ENV_TYPE="ish"
    echo "   Environment: iSH (Alpine Linux on iOS)"
elif [[ -d "/System/Library/PrivateFrameworks/MobileDevice.framework" ]]; then
    ENV_TYPE="ashell"
    echo "   Environment: a-Shell/a-Shell mini"
else
    ENV_TYPE="unknown"
    echo "⚠️  Environment: Unknown iOS shell (attempting generic installation)"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER="${USER:-mobile}"

echo "   User: $CURRENT_USER"
echo "   xharvester path: $SCRIPT_DIR"

# iOS-specific paths
if [[ "$ENV_TYPE" == "ish" ]]; then
    # iSH uses standard Linux paths
    BIN_DIR="$HOME/.local/bin"
    SHORTCUTS_DIR="$HOME/.shortcuts"
    ICONS_DIR="$HOME/.local/share/icons"
    DESKTOP_DIR="$HOME/.local/share/applications"
else
    # a-Shell uses iOS-friendly paths
    BIN_DIR="$HOME/Documents/bin"
    SHORTCUTS_DIR="$HOME/Shortcuts"
    ICONS_DIR="$HOME/Documents/icons"
    DESKTOP_DIR="$HOME/Documents/applications"
fi

echo "📁 Creating iOS-specific directories..."
mkdir -p "$BIN_DIR"
mkdir -p "$SHORTCUTS_DIR" 
mkdir -p "$ICONS_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy icons (iOS supports PNG)
echo "🎨 Installing icons for iOS..."
if [[ -f "$SCRIPT_DIR/icons/xharvester.png" ]]; then
    cp "$SCRIPT_DIR/icons/xharvester.png" "$ICONS_DIR/"
    cp "$SCRIPT_DIR/icons/linux/xharvester_64.png" "$ICONS_DIR/" 2>/dev/null || cp "$SCRIPT_DIR/icons/xharvester.png" "$ICONS_DIR/xharvester_64.png"
    cp "$SCRIPT_DIR/icons/linux/xharvester_128.png" "$ICONS_DIR/" 2>/dev/null || true
    echo "   ✅ Icons installed to $ICONS_DIR"
else
    echo "   ⚠️  Icons not found, skipping icon installation"
fi

# Create symbolic link
echo "🔗 Creating command-line integration..."
ln -sf "$SCRIPT_DIR/xharvester" "$BIN_DIR/xharvester"
chmod +x "$BIN_DIR/xharvester"
chmod +x "$SCRIPT_DIR/xharvester"

# Create iOS Shortcuts integration
echo "📱 Creating iOS Shortcuts integration..."

# Create Shortcuts-compatible wrapper
cat > "$BIN_DIR/xharvester-ios" << EOF
#!/bin/bash
# xharvester iOS Wrapper Script
# Optimized for a-Shell and iSH environments

# Set iOS-friendly environment
export TERM=xterm-256color
export COLORTERM=truecolor
export FORCE_COLOR=1
export PYTHONPATH="\$PYTHONPATH:$SCRIPT_DIR"

# Navigate to xharvester directory
cd "$SCRIPT_DIR" || {
    echo "❌ Could not find xharvester directory"
    exit 1
}

# iOS-specific adjustments
if [[ "$ENV_TYPE" == "ish" ]]; then
    # iSH may need package updates
    echo "📱 Running on iSH (iOS Alpine Linux)"
    # Check for basic tools
    for tool in python3 curl wget; do
        if ! command -v "\$tool" >/dev/null 2>&1; then
            echo "⚠️  Missing: \$tool (install with: apk add \$tool)"
        fi
    done
elif [[ "$ENV_TYPE" == "ashell" ]]; then
    # a-Shell specific optimizations
    echo "📱 Running on a-Shell (iOS)"
    export SHELL_NAME="a-shell"
fi

# Launch xharvester
echo "🚀 Launching xharvester on iOS..."
exec python3 ./xharvester "\$@"
EOF

chmod +x "$BIN_DIR/xharvester-ios"

# Create Shortcuts app integration file
echo "⚡ Creating iOS Shortcuts app integration..."
cat > "$SHORTCUTS_DIR/xharvester.shortcut" << EOF
{
  "name": "xharvester",
  "description": "Launch xharvester security toolkit",
  "icon": {
    "type": "custom",
    "path": "$ICONS_DIR/xharvester_64.png"
  },
  "actions": [
    {
      "type": "shell",
      "command": "$BIN_DIR/xharvester-ios",
      "app": "a-shell"
    }
  ]
}
EOF

# Create desktop entry for compatible file managers
if [[ "$ENV_TYPE" == "ish" ]]; then
    echo "📋 Creating desktop entry for iSH..."
    cat > "$DESKTOP_DIR/xharvester.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=xharvester
Comment=Extended Reconnaissance & Exploitation Toolkit for iOS
Comment[en]=Cross-platform security testing framework on iOS/iSH
Exec=$BIN_DIR/xharvester
Icon=$ICONS_DIR/xharvester.png
Terminal=true
Categories=Development;Security;Network;System;
Keywords=security;hacking;penetration;testing;bluetooth;wifi;automobile;rf;scada;ios;
StartupNotify=false
Path=$SCRIPT_DIR
EOF
fi

# Add to PATH
echo "🔧 Setting up PATH integration..."
SHELL_RC=""
if [[ -f "$HOME/.bashrc" ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ -f "$HOME/.profile" ]]; then
    SHELL_RC="$HOME/.profile"
else
    SHELL_RC="$HOME/.bashrc"
    touch "$SHELL_RC"
fi

# Add PATH entry if not already present
if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "   ✅ Added $BIN_DIR to PATH in $SHELL_RC"
fi

# Create iOS-specific aliases
cat >> "$SHELL_RC" << EOF

# xharvester iOS aliases
alias xharvester='$BIN_DIR/xharvester'
alias xharvester-ios='$BIN_DIR/xharvester-ios'
alias xh='$BIN_DIR/xharvester'
EOF

# Install iOS-specific dependencies
echo "📦 Checking iOS dependencies..."
MISSING_DEPS=""

if [[ "$ENV_TYPE" == "ish" ]]; then
    # iSH uses Alpine packages
    echo "   Checking Alpine packages..."
    for pkg in python3 py3-pip curl wget git; do
        if ! apk list --installed "$pkg" >/dev/null 2>&1; then
            MISSING_DEPS="$MISSING_DEPS $pkg"
        fi
    done
    
    if [[ -n "$MISSING_DEPS" ]]; then
        echo "⚠️  Missing Alpine packages: $MISSING_DEPS"
        echo "📦 Install with: apk add$MISSING_DEPS"
    fi
    
elif [[ "$ENV_TYPE" == "ashell" ]]; then
    # a-Shell has built-in Python
    echo "   a-Shell environment detected (Python built-in)"
    
    # Check for a-Shell packages
    if ! command -v pip3 >/dev/null 2>&1; then
        echo "⚠️  pip3 not found - may need to install via a-Shell package manager"
    fi
fi

# Create iOS-specific launch instructions
cat > "$HOME/xharvester_ios_launch.txt" << EOF
🍎 xharvester iOS Launch Instructions

📱 METHOD 1: Command Line (Recommended)
   Type in a-Shell/iSH: xharvester

📱 METHOD 2: iOS Optimized Launcher
   Type in a-Shell/iSH: xharvester-ios

📱 METHOD 3: iOS Shortcuts App
   1. Open iOS Shortcuts app
   2. Import: $SHORTCUTS_DIR/xharvester.shortcut
   3. Run shortcut from home screen widget

📱 METHOD 4: Direct Execution
   $BIN_DIR/xharvester

🔧 TROUBLESHOOTING:
   • Restart a-Shell/iSH to update PATH
   • Check permissions: chmod +x $BIN_DIR/xharvester
   • For iSH: apk update && apk add python3 py3-pip
   • For a-Shell: Use built-in Python environment

📂 INSTALLED FILES:
   • Binary: $BIN_DIR/xharvester
   • iOS Wrapper: $BIN_DIR/xharvester-ios
   • Shortcuts: $SHORTCUTS_DIR/xharvester.shortcut
   • Icons: $ICONS_DIR/xharvester*.png
   • Launch Guide: $HOME/xharvester_ios_launch.txt
EOF

echo ""
echo "xharvester iOS Integration installed successfully!"
echo ""
echo "📋 Installation Summary:"
echo "   Environment: $ENV_TYPE"
echo "   Binary: $BIN_DIR/xharvester"
echo "   iOS Wrapper: $BIN_DIR/xharvester-ios" 
echo "   Shortcuts: $SHORTCUTS_DIR/"
echo "   Icons: $ICONS_DIR/"
echo ""
echo "🚀 Usage on iOS:"
if [[ "$ENV_TYPE" == "ish" ]]; then
echo "   • iSH Terminal: xharvester"
echo "   • iOS Shortcuts: Import and run shortcut"
echo "   • File Manager: Launch from desktop entry"
elif [[ "$ENV_TYPE" == "ashell" ]]; then
echo "   • a-Shell: xharvester"
echo "   • a-Shell optimized: xharvester-ios"
echo "   • iOS Shortcuts: Import shortcut for home screen"
else
echo "   • Terminal: xharvester"
echo "   • iOS-optimized: xharvester-ios"
fi
echo ""
echo "📱 iOS-Specific Features:"
echo "   • Shortcuts app integration"
echo "   • Touch-friendly interface"
echo "   • iOS filesystem compatibility"
echo "   • Optimized for mobile screens"
echo ""
if [[ -n "$MISSING_DEPS" ]]; then
echo "⚠️  Install missing dependencies first:"
if [[ "$ENV_TYPE" == "ish" ]]; then
echo "   apk update && apk add$MISSING_DEPS"
elif [[ "$ENV_TYPE" == "ashell" ]]; then
echo "   Use a-Shell package manager for additional tools"
fi
echo ""
fi
echo "📖 Full launch instructions: $HOME/xharvester_ios_launch.txt"
echo ""
echo "🔄 Restart a-Shell/iSH to activate PATH changes"
echo ""
echo "🔧 To uninstall:"
echo "   rm -f $BIN_DIR/xharvester*"
echo "   rm -f $SHORTCUTS_DIR/xharvester*"
echo "   rm -f $ICONS_DIR/xharvester*.png"
if [[ "$ENV_TYPE" == "ish" ]]; then
echo "   rm -f $DESKTOP_DIR/xharvester.desktop"
fi
echo ""
