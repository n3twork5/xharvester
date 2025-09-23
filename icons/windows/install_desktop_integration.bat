@echo off
REM xharvester Windows Desktop Integration Installer
REM Creates desktop shortcuts and start menu entries

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "XHARVESTER_ROOT=%SCRIPT_DIR%..\.."

echo 🚀 Installing xharvester Desktop Integration for Windows...
echo    xharvester path: !XHARVESTER_ROOT!

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 📋 Running with Administrator privileges
    set "INSTALL_MODE=system"
) else (
    echo 📋 Running without Administrator privileges - user installation only
    set "INSTALL_MODE=user"
)

REM Set paths based on installation mode
if "!INSTALL_MODE!"=="system" (
    set "START_MENU_DIR=%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs"
    set "DESKTOP_DIR=%PUBLIC%\Desktop"
) else (
    set "START_MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
    set "DESKTOP_DIR=%USERPROFILE%\Desktop"
)

echo 📁 Creating directories...
if not exist "!START_MENU_DIR!" mkdir "!START_MENU_DIR!"

REM Create desktop shortcut
echo 🖥️  Creating desktop shortcut...
set "DESKTOP_SHORTCUT=!DESKTOP_DIR!\xharvester.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('!DESKTOP_SHORTCUT!'); $Shortcut.TargetPath = '!XHARVESTER_ROOT!\xharvester.exe'; $Shortcut.WorkingDirectory = '!XHARVESTER_ROOT!'; $Shortcut.IconLocation = '!SCRIPT_DIR!xharvester.ico'; $Shortcut.Description = 'xharvester - Extended Reconnaissance & Exploitation Toolkit'; $Shortcut.Save()"

REM Create start menu shortcut
echo 📋 Creating Start Menu shortcut...
set "STARTMENU_SHORTCUT=!START_MENU_DIR!\xharvester.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('!STARTMENU_SHORTCUT!'); $Shortcut.TargetPath = '!XHARVESTER_ROOT!\xharvester.exe'; $Shortcut.WorkingDirectory = '!XHARVESTER_ROOT!'; $Shortcut.IconLocation = '!SCRIPT_DIR!xharvester.ico'; $Shortcut.Description = 'xharvester - Extended Reconnaissance & Exploitation Toolkit'; $Shortcut.Save()"

REM Create "Run as Administrator" shortcut
echo 🔐 Creating "Run as Administrator" shortcut...
set "ADMIN_SHORTCUT=!START_MENU_DIR!\xharvester (Run as Administrator).lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('!ADMIN_SHORTCUT!'); $Shortcut.TargetPath = 'powershell.exe'; $Shortcut.Arguments = '-Command \"Start-Process \"\"!XHARVESTER_ROOT!\xharvester.exe\"\" -Verb RunAs\"'; $Shortcut.WorkingDirectory = '!XHARVESTER_ROOT!'; $Shortcut.IconLocation = '!SCRIPT_DIR!xharvester.ico'; $Shortcut.Description = 'xharvester - Run as Administrator'; $Shortcut.Save()"

REM Add to PATH (optional)
echo 🔗 Adding to system PATH...
set "XHARVESTER_IN_PATH="
for %%i in (!XHARVESTER_ROOT!) do (
    echo !PATH! | findstr /C:"%%i" >nul
    if not errorlevel 1 set "XHARVESTER_IN_PATH=1"
)

if not defined XHARVESTER_IN_PATH (
    if "!INSTALL_MODE!"=="system" (
        setx PATH "!PATH!;!XHARVESTER_ROOT!" /M >nul 2>&1
        echo ✅ Added to system PATH
    ) else (
        setx PATH "!PATH!;!XHARVESTER_ROOT!" >nul 2>&1
        echo ✅ Added to user PATH
    )
    echo ⚠️  Restart Command Prompt to use 'xharvester' command
) else (
    echo ℹ️  Already in PATH
)

echo.
echo ✅ xharvester Desktop Integration installed successfully!
echo.
echo 📋 Installation Summary:
echo    Mode: !INSTALL_MODE!
echo    Desktop Shortcut: !DESKTOP_SHORTCUT!
echo    Start Menu: !START_MENU_DIR!\xharvester*.lnk
echo.
echo 🚀 Usage:
echo    • Find 'xharvester' in Start Menu
echo    • Double-click desktop shortcut
echo    • Use "Run as Administrator" version for full features
echo    • Command line: xharvester (after restart)
echo.
echo 🔧 To uninstall:
echo    del "!DESKTOP_SHORTCUT!"
echo    del "!START_MENU_DIR!\xharvester*.lnk"
echo.

pause