# Android Icons - xharvester v1.0

## Files:
### Standard Launcher Icons:
- `xharvester_mdpi_48.png` - 48x48 (MDPI - ~160dpi)
- `xharvester_hdpi_72.png` - 72x72 (HDPI - ~240dpi) 
- `xharvester_xhdpi_96.png` - 96x96 (XHDPI - ~320dpi)
- `xharvester_xxhdpi_144.png` - 144x144 (XXHDPI - ~480dpi)
- `xharvester_xxxhdpi_192.png` - 192x192 (XXXHDPI - ~640dpi)

### Alternative Sizes:
- `xharvester_mdpi.png` - 64x64 (alternative MDPI)
- `xharvester_hdpi.png` - 128x128 (alternative HDPI)
- `xharvester_xhdpi.png` - 256x256 (alternative XHDPI) 
- `xharvester_xxhdpi.png` - 512x512 (alternative XXHDPI)

## Usage:

### For Android APK Development:
Place icons in `res/drawable-*dpi/` directories:
```
res/
├── drawable-mdpi/ic_launcher.png (48x48)
├── drawable-hdpi/ic_launcher.png (72x72)
├── drawable-xhdpi/ic_launcher.png (96x96)
├── drawable-xxhdpi/ic_launcher.png (144x144)
└── drawable-xxxhdpi/ic_launcher.png (192x192)
```

### For Termux/Terminal Apps:
- Use 96x96 (xhdpi) for most modern devices
- 144x144 (xxhdpi) for high-density displays
- PNG format with transparency support

### For Android Studio:
1. Right-click `res` → New → Image Asset
2. Choose "Launcher Icons (Adaptive and Legacy)"
3. Import the appropriate sized PNG
4. Generate adaptive icon variants

### For React Native:
```javascript
// Place in android/app/src/main/res/drawable-*dpi/
// Reference in AndroidManifest.xml:
android:icon="@drawable/ic_launcher"
```

### For Cordova/PhoneGap:
Add to `config.xml`:
```xml
<platform name="android">
    <icon src="icons/android/xharvester_mdpi_48.png" density="mdpi" />
    <icon src="icons/android/xharvester_hdpi_72.png" density="hdpi" />
    <icon src="icons/android/xharvester_xhdpi_96.png" density="xhdpi" />
    <icon src="icons/android/xharvester_xxhdpi_144.png" density="xxhdpi" />
    <icon src="icons/android/xharvester_xxxhdpi_192.png" density="xxxhdpi" />
</platform>
```

## Density Guidelines:
- **MDPI**: ~160 DPI (1x baseline)
- **HDPI**: ~240 DPI (1.5x)  
- **XHDPI**: ~320 DPI (2x)
- **XXHDPI**: ~480 DPI (3x)
- **XXXHDPI**: ~640 DPI (4x)

## Format Requirements:
- **Format**: PNG with alpha transparency
- **Color**: Full color support (24-bit + alpha)
- **Compression**: Optimized for mobile bandwidth