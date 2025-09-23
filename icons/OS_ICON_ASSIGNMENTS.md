# xharvester v1.0 - OS Icon Assignments

## 🎯 Icon Distribution by Operating System

### 🪟 Windows (`icons/windows/`)
- **Primary**: `xharvester.ico` (Multi-resolution ICO)
- **Fallback**: `xharvester.png` (256x256 PNG)
- **Use Cases**: Executables, desktop shortcuts, installers
- **Format**: ICO preferred (native Windows format)

### 🐧 Linux (`icons/linux/`)
- **Primary**: `xharvester.png` (256x256 PNG)
- **Small**: `xharvester_64.png` (System tray, notifications)
- **Medium**: `xharvester_128.png` (Panel icons, menus)
- **Use Cases**: .desktop files, system icons, application launchers
- **Format**: PNG (freedesktop.org standard)

### 🍎 macOS (`icons/macos/`)
- **Primary**: `xharvester.png` (256x256 PNG)
- **Small**: `xharvester_64.png` (Menu bar)
- **Medium**: `xharvester_128.png` (Standard displays)
- **Large**: `xharvester_512.png` (Retina displays)
- **Use Cases**: App bundles (.app), dock icons
- **Format**: PNG → Convert to .icns for app bundles

### 🤖 Android (`icons/android/`)
- **MDPI**: `xharvester_mdpi_48.png` (48x48 - ~160dpi)
- **HDPI**: `xharvester_hdpi_72.png` (72x72 - ~240dpi)
- **XHDPI**: `xharvester_xhdpi_96.png` (96x96 - ~320dpi)
- **XXHDPI**: `xharvester_xxhdpi_144.png` (144x144 - ~480dpi)
- **XXXHDPI**: `xharvester_xxxhdpi_192.png` (192x192 - ~640dpi)
- **Use Cases**: APK development, Termux apps, launcher icons
- **Format**: PNG with density-specific sizing

## 📋 Quick Reference

| OS | Primary Format | Primary File | Sizes Available |
|---|---|---|---|
| **Windows** | ICO | `xharvester.ico` | 16,32,48,64,128px |
| **Linux** | PNG | `xharvester.png` | 64,128,256px |
| **macOS** | PNG→ICNS | `xharvester.png` | 64,128,256,512px |
| **Android** | PNG | Multiple DPI files | 48,72,96,144,192px |

## 🔧 Implementation Commands

### Windows (PyInstaller):
```bash
pyinstaller --onefile --icon=icons/windows/xharvester.ico xharvester
```

### Linux (Desktop file):
```bash
cp icons/linux/xharvester.png ~/.local/share/icons/
```

### macOS (Create .icns):
```bash
iconutil -c icns xharvester.iconset -o xharvester.icns
```

### Android (Termux):
- Use `xharvester_xhdpi_96.png` for most modern devices
- Copy to appropriate `res/drawable-*dpi/` directories

## 🎨 Icon Design Features
- **Color Scheme**: Dark theme with cyan (#00d4aa) accents
- **Typography**: "X" in cyan, "HARVESTER" in white
- **Version**: "v1.0 Cross-Platform Edition" in magenta (#ff00ff)
- **Creator**: "by n3twork" in cyan (#00d4aa)
- **Style**: Professional security tool aesthetic
- **Transparency**: Full alpha channel support on all formats

## 📁 Directory Structure (Optimized)
```
icons/
├── OS_ICON_ASSIGNMENTS.md (this file)
├── xharvester.png (master 256x256)
├── xharvester.ico (Windows multi-res)
├── windows/
│   ├── README.md
│   ├── xharvester.ico
│   └── xharvester.png
├── linux/  
│   ├── README.md
│   ├── xharvester.png
│   ├── xharvester_64.png
│   └── xharvester_128.png
├── macos/
│   ├── README.md
│   ├── xharvester.png
│   ├── xharvester_64.png
│   ├── xharvester_128.png
│   └── xharvester_512.png
└── android/
    ├── README.md
    ├── xharvester_mdpi_48.png (MDPI - 48x48)
    ├── xharvester_hdpi_72.png (HDPI - 72x72)
    ├── xharvester_xhdpi_96.png (XHDPI - 96x96)
    ├── xharvester_xxhdpi_144.png (XXHDPI - 144x144)
    └── xharvester_xxxhdpi_192.png (XXXHDPI - 192x192)
```

**Total Files**: 21 (optimized from 28) - removed duplicates and legacy icons

Each OS directory contains detailed implementation instructions in its respective README.md file.