# Windows Icons - xharvester v1.0

## Files:
- `xharvester.ico` - Multi-resolution ICO file (preferred for Windows)
- `xharvester.png` - 256x256 PNG fallback

## Usage:

### For Executable Files (.exe):
```bash
# Using Resource Hacker or similar tool
# Embed xharvester.ico into your compiled executable
```

### For Desktop Shortcuts:
1. Right-click on desktop → New → Shortcut
2. Browse to xharvester executable
3. Right-click shortcut → Properties → Change Icon
4. Browse to `xharvester.ico`

### For PyInstaller (Python to EXE):
```bash
pyinstaller --onefile --icon=icons/windows/xharvester.ico xharvester
```

### For Windows Installer:
- Use `xharvester.ico` for installer icon
- Contains multiple resolutions: 16x16, 32x32, 48x48, 64x64, 128x128

## Format Details:
- **ICO Format**: Native Windows icon format
- **Multi-resolution**: Automatically scales for different contexts
- **Transparency**: Full alpha channel support