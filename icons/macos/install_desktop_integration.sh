#!/bin/bash
# xharvester macOS Desktop Integration Installer
# Creates app bundle and dock integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XHARVESTER_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
CURRENT_USER="${SUDO_USER:-$USER}"

echo "🚀 Installing xharvester Desktop Integration for macOS..."
echo "   User: $CURRENT_USER"
echo "   xharvester path: $XHARVESTER_ROOT"

# Check if running with sudo for system-wide installation
if [[ $EUID -eq 0 ]]; then
    echo "📋 Installing system-wide (requires sudo)..."
    INSTALL_MODE="system"
    APP_DIR="/Applications"
    BIN_DIR="/usr/local/bin"
else
    echo "📋 Installing for current user only..."
    INSTALL_MODE="user"
    APP_DIR="$HOME/Applications"
    BIN_DIR="$HOME/bin"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p "$APP_DIR"
mkdir -p "$BIN_DIR"

# Create app bundle structure
APP_BUNDLE="$APP_DIR/xharvester.app"
echo "📦 Creating app bundle: $APP_BUNDLE"
rm -rf "$APP_BUNDLE"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Create Info.plist
echo "📄 Creating Info.plist..."
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>xharvester</string>
    <key>CFBundleIconFile</key>
    <string>xharvester</string>
    <key>CFBundleIdentifier</key>
    <string>com.n3twork.xharvester</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>xharvester</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>LSRequiresCarbon</key>
    <false/>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.developer-tools</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>All Files</string>
            <key>CFBundleTypeOSTypes</key>
            <array>
                <string>****</string>
            </array>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
            <key>LSTypeIsPackage</key>
            <false/>
        </dict>
    </array>
</dict>
</plist>
EOF

# Create executable launcher script
echo "🔗 Creating launcher script..."
cat > "$APP_BUNDLE/Contents/MacOS/xharvester" << EOF
#!/bin/bash
# xharvester macOS Launcher
# Opens Terminal and runs xharvester

XHARVESTER_PATH="$XHARVESTER_ROOT/xharvester"

# Check if running with admin privileges needed
if [[ "\$1" == "--admin" ]]; then
    # Use AppleScript to request admin privileges
    osascript -e "do shell script \"'\$XHARVESTER_PATH'\" with administrator privileges"
else
    # Open Terminal and run xharvester
    osascript <<EOD
        tell application "Terminal"
            activate
            do script "cd '$XHARVESTER_ROOT' && sudo ./xharvester"
        end tell
EOD
fi
EOF

chmod +x "$APP_BUNDLE/Contents/MacOS/xharvester"

# Convert PNG to icns (if iconutil is available)
echo "🎨 Creating app icon..."
if command -v iconutil >/dev/null 2>&1; then
    # Create iconset directory
    ICONSET_DIR="$APP_BUNDLE/Contents/Resources/xharvester.iconset"
    mkdir -p "$ICONSET_DIR"
    
    # Copy and resize icons for iconset
    if [[ -f "$SCRIPT_DIR/../xharvester.png" ]]; then
        cp "$SCRIPT_DIR/../xharvester.png" "$ICONSET_DIR/icon_256x256.png"
        
        # Try to create other sizes using sips
        if command -v sips >/dev/null 2>&1; then
            sips -z 16 16 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null 2>&1
            sips -z 32 32 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null 2>&1
            sips -z 32 32 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null 2>&1
            sips -z 64 64 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null 2>&1
            sips -z 128 128 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null 2>&1
            sips -z 256 256 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null 2>&1
            sips -z 512 512 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null 2>&1
            sips -z 512 512 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null 2>&1
            sips -z 1024 1024 "$ICONSET_DIR/icon_256x256.png" --out "$ICONSET_DIR/icon_512x512@2x.png" >/dev/null 2>&1
        fi
        
        # Convert iconset to icns
        iconutil -c icns "$ICONSET_DIR" -o "$APP_BUNDLE/Contents/Resources/xharvester.icns"
        rm -rf "$ICONSET_DIR"
    fi
else
    # Fallback: just copy PNG
    cp "$SCRIPT_DIR/../xharvester.png" "$APP_BUNDLE/Contents/Resources/xharvester.png" 2>/dev/null || true
fi

# Create symbolic link for command-line access
echo "🔗 Creating symbolic link..."
ln -sf "$XHARVESTER_ROOT/xharvester" "$BIN_DIR/xharvester"

# Add to PATH if not already there
if [[ $INSTALL_MODE == "user" ]]; then
    if ! echo "$PATH" | grep -q "$BIN_DIR"; then
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bash_profile"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.zshrc" 2>/dev/null || true
        echo "⚠️  Added $BIN_DIR to PATH in shell profiles - restart terminal"
    fi
fi

# Register app with Launch Services (to appear in Spotlight, etc.)
echo "🔄 Registering with Launch Services..."
if command -v lsregister >/dev/null 2>&1; then
    /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$APP_BUNDLE"
fi

echo ""
echo "✅ xharvester Desktop Integration installed successfully!"
echo ""
echo "📋 Installation Summary:"
echo "   Mode: $INSTALL_MODE"
echo "   App Bundle: $APP_BUNDLE"
echo "   Binary Link: $BIN_DIR/xharvester"
echo ""
echo "🚀 Usage:"
echo "   • Find 'xharvester' in Applications folder"
echo "   • Find 'xharvester' in Spotlight search (⌘+Space)"
echo "   • Command line: xharvester (after restart)"
echo "   • Dock: Drag app from Applications to Dock"
echo ""
echo "🔧 To uninstall:"
echo "   rm -rf '$APP_BUNDLE'"
echo "   rm -f '$BIN_DIR/xharvester'"
echo ""