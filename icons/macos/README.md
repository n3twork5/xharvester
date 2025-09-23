# macOS Icons - xharvester v1.0

## Files:
- `xharvester.png` - 256x256 main icon
- `xharvester_64.png` - 64x64 for menu bar/small contexts  
- `xharvester_128.png` - 128x128 for medium contexts
- `xharvester_512.png` - 512x512 for high-DPI displays

## Usage:

### For App Bundle (.app):
1. Create an iconset directory:
```bash
mkdir xharvester.iconset
```

2. Copy and rename icons to iconset:
```bash
cp xharvester_64.png xharvester.iconset/icon_32x32@2x.png
cp xharvester_128.png xharvester.iconset/icon_64x64@2x.png  
cp xharvester.png xharvester.iconset/icon_128x128@2x.png
cp xharvester_512.png xharvester.iconset/icon_256x256@2x.png
```

3. Generate .icns file:
```bash
iconutil -c icns xharvester.iconset -o xharvester.icns
```

### For PyInstaller (Python to .app):
```bash
pyinstaller --onefile --windowed --icon=icons/macos/xharvester.icns xharvester
```

### For Terminal Applications:
- Use 64x64 or 128x128 for terminal contexts
- 512x512 for Retina displays

### For Dock:
- macOS automatically scales from available sizes
- 512x512 provides best quality for large dock sizes
- Supports drag-and-drop to dock

## Required Sizes for Complete .icns:
- 16x16, 32x32, 64x64, 128x128, 256x256, 512x512
- Each with @2x retina variants
- Use `iconutil` to create proper .icns file

## App Bundle Structure:
```
xharvester.app/
├── Contents/
│   ├── Info.plist (specify icon file)
│   ├── MacOS/xharvester
│   └── Resources/xharvester.icns
```