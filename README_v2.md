# xharvester v2.0 - Improved Edition

```
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ 
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \
 )  (  ) _ (  /(__)\\  )   / \  /  )__) \__ \  )(   )__)  )   /
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
```

⚡ **xharvester v2.0** is a completely rewritten and improved version of the specialized Python-based reconnaissance and exploitation suite designed for security assessments of radio frequency (RF), wireless (Bluetooth & WiFi), industrial control systems (SCADA), and automotive systems.

## 🚀 What's New in v2.0

### Major Improvements
- **🔧 Modular Architecture**: Complete code restructuring with proper separation of concerns
- **🛡️ Enhanced Security**: Improved input validation and security controls
- **📝 Comprehensive Logging**: Structured logging system with file rotation
- **⚙️ Configuration Management**: Centralized configuration system
- **🔄 Better Error Handling**: Graceful error handling with proper cleanup
- **🧵 Thread Safety**: Improved threading management for CAN bus operations
- **📊 Input Validation**: Robust input validation to prevent security issues

### Code Quality Improvements
- **✅ No Code Duplication**: Eliminated duplicate color definitions and functions
- **🔒 Proper Resource Cleanup**: Threading cleanup and CAN interface management
- **📚 Documentation**: Comprehensive docstrings and type hints
- **🎯 Semantic Colors**: Better color coding for different message types
- **⚡ Performance**: Optimized animations and reduced resource usage

## 📁 New Project Structure

```
xharvester/
├── config.py                 # Centralized configuration management
├── utils.py                  # Shared utilities and helper functions
├── xharvester                 # Improved main application
├── modules/
│   ├── automobile_module.py   # Enhanced automobile security testing
│   └── automobile_module_old.py  # Original version (backup)
├── logs/                      # Application logs directory
├── requirements.txt           # Dependencies
└── README_v2.md              # This file
```

## 🆕 New Features

### Configuration System (`config.py`)
- **Centralized Settings**: All application settings in one place
- **Security Controls**: Configurable security parameters
- **CAN Bus Settings**: ICSim-specific CAN IDs and configurations
- **Logging Configuration**: Structured logging setup

### Utilities Module (`utils.py`)
- **Input Validation**: Robust validation for all user inputs
- **Animation System**: Improved typewriter animations
- **Menu Rendering**: Standardized menu rendering
- **Error Handling**: Context managers for graceful error handling
- **Security Features**: Input sanitization and length limits

### Enhanced Automobile Module
- **Thread Safety**: Proper threading with locks and cleanup
- **CAN Attack Simulator**: Dedicated class for CAN bus attacks
- **Better Error Handling**: Comprehensive exception management
- **Resource Cleanup**: Automatic cleanup on exit or errors
- **Improved Logging**: Detailed logging for debugging

## 🛠️ Installation (No Changes)

### Clone the Repository
```bash
git clone https://github.com/n3tworkh4x/xharvester.git
cd xharvester
```

### Virtual Environment Setup
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

### Install Requirements
```bash
pip install -r requirements.txt
```

### External Requirements (Linux)
```bash
sudo apt update
sudo apt install libdbus-1-dev libgirepository1.0-dev libcairo2-dev libbluetooth-dev bluez
sudo apt install aircrack-ng hostapd dnsmasq iptables
```

## ⚡ Usage

### Running xharvester v2.0
```bash
sudo ./xharvester
```

## 🔧 Configuration

### Customizing Settings
Edit `config.py` to customize:
- CAN interface settings
- Animation speeds
- Security parameters
- Logging configuration
- Application metadata

### Example Configuration Changes
```python
# Change default CAN interface
DEFAULT_CAN_INTERFACE = "can0"  # Instead of "vcan0"

# Modify animation speed
ANIMATION_SPEED = 0.01  # Faster animations

# Adjust security settings
MAX_INPUT_LENGTH = 512  # Shorter input limit
```

## 🚨 Security Improvements

### Input Validation
- **Length Limits**: All inputs have configurable length limits
- **Type Validation**: Proper integer and hex validation
- **Range Checking**: Values are checked against allowed ranges
- **Sanitization**: Removal of potentially dangerous characters

### Thread Safety
- **Resource Locking**: Proper threading locks for shared resources
- **Cleanup Management**: Automatic cleanup of threads and resources
- **Timeout Handling**: Thread timeouts to prevent hanging

### Error Handling
- **Graceful Degradation**: Application continues even with non-critical errors
- **Proper Logging**: All errors are logged with stack traces
- **User Feedback**: Clear error messages for users

## 📊 Logging System

### Log Files
- **Application Log**: `logs/xharvester.log`
- **Module Logs**: `logs/automobile_module.log`
- **Rotation**: Automatic log rotation (10MB max, 5 backups)

### Log Levels
- **INFO**: General application flow
- **WARNING**: Potential issues
- **ERROR**: Actual errors with stack traces

## 🔍 Debugging

### Enable Debug Mode
```python
# In config.py
LOG_LEVEL = "DEBUG"  # Instead of "INFO"
```

### Check Logs
```bash
# View latest logs
tail -f logs/xharvester.log
tail -f logs/automobile_module.log
```

## 🧪 Testing

### Test Configuration Loading
```bash
python3 -c "from config import Config; print(f'Config loaded: {Config.APP_NAME} v{Config.VERSION}')"
```

### Test Utilities
```bash
python3 -c "from utils import Animation, Colors; Animation.typewriter_text(f'{Colors.SUCCESS}Test successful!{Colors.RESET}')"
```

## 🆚 Comparison: v1.0 vs v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Code Structure | Monolithic | Modular |
| Error Handling | Basic try/except | Comprehensive with context managers |
| Threading | Basic | Thread-safe with proper cleanup |
| Configuration | Hardcoded | Centralized config system |
| Input Validation | Minimal | Comprehensive validation |
| Logging | Print statements | Structured logging with rotation |
| Code Duplication | Significant | Eliminated |
| Documentation | Basic | Comprehensive with type hints |
| Security | Basic | Enhanced with input sanitization |

## 🐛 Known Issues Fixed

- ✅ **Duplicate imports** - Resolved in all modules
- ✅ **Code duplication** - Eliminated color codes duplication
- ✅ **Threading cleanup** - Proper resource management
- ✅ **Generic exception handling** - More specific error handling
- ✅ **Input validation** - Comprehensive validation system
- ✅ **CAN interface hardcoding** - Configurable interface names

## 🔄 Migration from v1.0

If you have the old version:

1. **Backup your data**: The new version is backward compatible
2. **Update dependencies**: No new dependencies required
3. **Configuration**: Your old settings will work, but consider using the new config system
4. **Logs**: New structured logging will be created automatically

## 🤝 Contributing

With the new modular structure, contributing is easier:

1. **Configuration changes**: Edit `config.py`
2. **New utilities**: Add to `utils.py`
3. **New modules**: Create in `modules/` directory
4. **Follow the pattern**: Use the automobile module as a template

## 📞 Support

- **GitHub**: [@n3tworkh4x](https://github.com/n3tworkh4x)
- **Ko-fi**: [Support Development](https://ko-fi.com/n3twork)
- **Issues**: Use the GitHub issue tracker for bugs

## 📄 License & Disclaimer

**⚠️ IMPORTANT DISCLAIMER**: This tool is intended for authorized security testing and educational purposes only. Interfering with wireless signals, industrial processes, or vehicle systems without explicit permission is illegal, extremely dangerous, and can lead to physical harm, catastrophic failure, and severe legal consequences. Always operate within a controlled, legal environment.

---

**xharvester v2.0** - *"Coding Is My Weapon, Hacking Is My Art"*

Created by **Network(GHANA)** 🇬🇭