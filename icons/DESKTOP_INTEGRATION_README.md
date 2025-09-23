# 🖥️ xharvester Desktop Integration

This directory contains OS-specific desktop integration files and installers for xharvester, allowing users to launch the tool from their desktop environment, start menu, or application launcher.

## 🚀 Quick Installation

### Universal Installer (Recommended)
```bash
# From xharvester root directory
./install_desktop_integration
```
This script automatically detects your OS and runs the appropriate installer.

### OS-Specific Installation

#### 🐧 Linux
```bash
# User installation (recommended)
./icons/linux/install_desktop_integration.sh

# System-wide installation (requires sudo)
sudo ./icons/linux/install_desktop_integration.sh
```

#### 🍎 macOS
```bash
# User installation (recommended)  
./icons/macos/install_desktop_integration.sh

# System-wide installation (requires sudo)
sudo ./icons/macos/install_desktop_integration.sh
```

#### 🪟 Windows
```batch
# Run as regular user or Administrator
icons\windows\install_desktop_integration.bat
```

#### 🤖 Android/Termux
```bash
# In Termux app
./icons/android/install_termux_integration.sh
```

## 📁 Directory Structure

```
icons/
├── DESKTOP_INTEGRATION_README.md (this file)
├── OS_ICON_ASSIGNMENTS.md (technical documentation)
├── xharvester.ico (Windows icon)
├── xharvester.png (primary icon - 256x256)
├── xharvester_*.png (various sizes)
├── linux/
│   ├── install_desktop_integration.sh
│   └── xharvester.desktop (template)
├── macos/
│   └── install_desktop_integration.sh
├── windows/
│   └── install_desktop_integration.bat
└── android/
    └── install_termux_integration.sh
```

## 🎯 What Gets Installed

### 🐧 Linux
- **Desktop Entry**: `~/.local/share/applications/xharvester.desktop`
- **Icons**: `~/.local/share/icons/xharvester*.png`
- **Symbolic Link**: `~/.local/bin/xharvester`
- **Features**: Application launcher integration, right-click "Run as Root"

### 🍎 macOS
- **App Bundle**: `~/Applications/xharvester.app` (or `/Applications/`)
- **Icons**: Converted to `.icns` format within app bundle
- **Symbolic Link**: `~/bin/xharvester` (or `/usr/local/bin/`)
- **Features**: Spotlight search, Dock integration, Launchpad

### 🪟 Windows
- **Desktop Shortcut**: `Desktop/xharvester.lnk`
- **Start Menu**: `Start Menu/xharvester.lnk`
- **Admin Shortcut**: `Start Menu/xharvester (Run as Administrator).lnk`
- **PATH Integration**: System/User PATH variable
- **Features**: Start Menu, desktop icon, "Run as Administrator" option

### 🤖 Android/Termux
- **Termux Shortcuts**: `~/.shortcuts/xharvester*`
- **Command Integration**: `$PREFIX/bin/xharvester`
- **Desktop Entry**: `$PREFIX/share/applications/xharvester.desktop`
- **Features**: Termux widget support, command-line access, root mode

## 🚀 Usage After Installation

### 🐧 Linux
```bash
# From application launcher
# Search for "xharvester" in Activities/Applications

# Command line (after PATH update)
xharvester

# Direct execution
~/.local/bin/xharvester
```

### 🍎 macOS
```bash
# From Applications folder
# Double-click xharvester.app

# From Spotlight
# Press ⌘+Space, type "xharvester"

# Command line
xharvester  # (after shell restart)
```

### 🪟 Windows
```batch
# From Start Menu
# Click Start → Search "xharvester"

# Desktop shortcut
# Double-click desktop icon

# Command line (after restart)
xharvester
```

### 🤖 Android/Termux
```bash
# Termux Widget (recommended)
# 1. Install Termux:Widget from F-Droid/Play Store
# 2. Add widget to home screen
# 3. Select "xharvester"

# Command line in Termux
xharvester

# Root mode (if tsu installed)
xharvester-root
```

## ⚙️ Advanced Features

### Linux: Run as Root
The desktop entry includes a right-click context menu option to "Run as Root" using `pkexec`.

### macOS: Terminal Integration
The app bundle automatically opens Terminal and launches xharvester with proper working directory.

### Windows: Administrator Mode
Separate shortcut created for "Run as Administrator" functionality.

### Android: Widget Support
Full integration with Termux:Widget for home screen shortcuts.

## 🔧 Troubleshooting

### Icon Not Appearing
```bash
# Linux: Update icon cache
gtk-update-icon-cache -f -t ~/.local/share/icons/

# Linux: Update desktop database  
update-desktop-database ~/.local/share/applications/
```

### Command Not Found
```bash
# Check if binary link exists
ls -la ~/.local/bin/xharvester  # Linux/macOS
ls -la $PREFIX/bin/xharvester   # Android

# Add to PATH manually
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission Issues
```bash
# Linux: Make sure files are executable
chmod +x ~/.local/bin/xharvester
chmod +x ~/.local/share/applications/xharvester.desktop

# macOS: Fix app bundle permissions
chmod +x ~/Applications/xharvester.app/Contents/MacOS/xharvester
```

## 🗑️ Uninstallation

Each installer provides uninstallation commands in its output. General uninstall:

### Linux
```bash
rm -f ~/.local/share/applications/xharvester.desktop
rm -f ~/.local/share/icons/xharvester*.png  
rm -f ~/.local/bin/xharvester
```

### macOS
```bash
rm -rf ~/Applications/xharvester.app
rm -f ~/bin/xharvester
```

### Windows
```batch
del "%USERPROFILE%\Desktop\xharvester.lnk"
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\xharvester*.lnk"
```

### Android/Termux
```bash
rm -f $PREFIX/bin/xharvester*
rm -f ~/.shortcuts/xharvester*
rm -f $PREFIX/share/applications/xharvester.desktop
```

## 🔒 Security Considerations

- Desktop integration installers respect user vs. system installation modes
- Root/Administrator shortcuts are clearly labeled and use appropriate privilege escalation
- All scripts include validation and error checking
- Symbolic links point to original xharvester location (not copies)

## 🐛 Known Issues

1. **Linux**: Some desktop environments may require logout/login to show new applications
2. **macOS**: First launch may show security warning - right-click → Open to bypass
3. **Windows**: Windows Defender may flag shortcuts - add exclusion if needed
4. **Android**: Requires Termux:Widget app for home screen integration

## 📧 Support

If you encounter issues with desktop integration:

1. Check the installer output for error messages
2. Verify file permissions and locations
3. Try manual installation steps from the installer scripts
4. Ensure xharvester main executable is working correctly

---

**Created by**: N3twork(GHANA)  
**Version**: 1.0  
**License**: For authorized security testing only