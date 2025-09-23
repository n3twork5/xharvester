# Linux Icons - xharvester v1.0

## Files:
- `xharvester.png` - 256x256 main icon
- `xharvester_64.png` - 64x64 for system tray/small contexts
- `xharvester_128.png` - 128x128 for medium contexts

## Usage:

### For Desktop Files (.desktop):
Create `xharvester.desktop` in `~/.local/share/applications/`:
```desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=xharvester
Comment=Security Reconnaissance Suite v1.0
Exec=/path/to/xharvester
Icon=/path/to/icons/linux/xharvester.png
Terminal=true
Categories=Security;Network;
```

### For System Installation:
```bash
# Copy icons to system directories
sudo cp xharvester.png /usr/share/pixmaps/
sudo cp xharvester_*.png /usr/share/icons/hicolor/*/apps/

# Update icon cache
sudo update-icon-caches /usr/share/icons/hicolor/
```

### For KDE/Plasma:
- Icons work with Plasma desktop files
- Use 128x128 for Plasma panels
- 256x256 for desktop and application launcher

### For GNOME:
- Compatible with GNOME Shell
- Use 256x256 for Activities overview
- Smaller sizes for top bar and notifications

### For Window Managers (i3, dwm, etc.):
- Use with application launchers like dmenu, rofi
- 64x64 recommended for most WM contexts

## Standard Locations:
- **User**: `~/.local/share/icons/hicolor/256x256/apps/`
- **System**: `/usr/share/icons/hicolor/256x256/apps/`
- **Pixmaps**: `/usr/share/pixmaps/` (legacy fallback)