#!/data/data/com.termux/files/usr/bin/bash
# xharvester Android/Termux Installation Script
# This script sets up xharvester for Android devices using Termux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Banner
echo -e "${CYAN}"
echo " _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ "
echo "( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \\"
echo " )  (  ) _ (  /(__)\\  )   / \  /  )__) \__ \  )(   )__)  )   /"
echo "(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)"
echo -e "${NC}"
echo -e "${GREEN}>>> xharvester Android/Termux Installation Script <<<${NC}"
echo -e "${YELLOW}Created by Network(GHANA)${NC}"
echo ""

# Check if running in Termux
if [[ ! -d "/data/data/com.termux" ]]; then
    echo -e "${RED}Error: This script is designed for Termux on Android!${NC}"
    echo -e "${YELLOW}For other platforms, use the regular installation method.${NC}"
    exit 1
fi

echo -e "${BLUE}[INFO]${NC} Detected Termux environment"
echo -e "${BLUE}[INFO]${NC} Android version: $(getprop ro.build.version.release)"

# Function to install packages
install_packages() {
    echo -e "${CYAN}[STEP 1/6]${NC} Updating package lists..."
    pkg update -y
    
    echo -e "${CYAN}[STEP 2/6]${NC} Installing required packages..."
    pkg install -y python git tsu curl wget zip unzip
    
    echo -e "${CYAN}[STEP 3/6]${NC} Installing Python packages..."
    pip install --upgrade pip
    pip install wheel setuptools
}

# Function to setup xharvester
setup_xharvester() {
    echo -e "${CYAN}[STEP 4/6]${NC} Setting up xharvester..."
    
    # Create xharvester directory
    XHARVESTER_DIR="$HOME/xharvester"
    
    if [[ -d "$XHARVESTER_DIR" ]]; then
        echo -e "${YELLOW}[WARNING]${NC} xharvester directory already exists"
        read -p "$(echo -e "${GREEN}Remove existing installation? (y/N): ${YELLOW}")" -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$XHARVESTER_DIR"
        else
            echo -e "${RED}Installation cancelled.${NC}"
            exit 1
        fi
    fi
    
    # Clone repository
    echo -e "${BLUE}[INFO]${NC} Cloning xharvester repository..."
    git clone https://github.com/n3tworkh4x/xharvester.git "$XHARVESTER_DIR"
    
    cd "$XHARVESTER_DIR"
    
    # Setup virtual environment
    echo -e "${BLUE}[INFO]${NC} Setting up Python virtual environment..."
    python -m venv venv
    source venv/bin/activate
    
    # Install Python requirements
    echo -e "${BLUE}[INFO]${NC} Installing Python requirements..."
    pip install -r requirements.txt
    
    # Make xharvester executable
    chmod +x xharvester
}

# Function to create launch script
create_launcher() {
    echo -e "${CYAN}[STEP 5/6]${NC} Creating launch script..."
    
    cat > "$HOME/xharvester/launch_android.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# xharvester Android/Termux Launcher

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}🚀 Starting xharvester on Android/Termux...${NC}"
echo -e "${BLUE}Platform: $(uname -o)${NC}"
echo -e "${BLUE}Python: $(python --version)${NC}"
echo ""

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check if root access is available (optional)
if command -v tsu &> /dev/null; then
    echo -e "${YELLOW}[INFO] Root access (tsu) available${NC}"
    read -p "$(echo -e "${GREEN}Run with root privileges? (y/N): ${YELLOW}")" -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Starting xharvester with root privileges...${NC}"
        tsu -c "cd '$SCRIPT_DIR' && source venv/bin/activate && python xharvester"
    else
        echo -e "${GREEN}Starting xharvester without root privileges...${NC}"
        cd "$SCRIPT_DIR" && python xharvester
    fi
else
    echo -e "${YELLOW}[INFO] Running without root privileges${NC}"
    echo -e "${BLUE}[TIP] Install 'tsu' for root access: pkg install tsu${NC}"
    cd "$SCRIPT_DIR" && python xharvester
fi
EOF
    
    chmod +x "$HOME/xharvester/launch_android.sh"
    
    # Create shortcut in bin directory
    mkdir -p "$HOME/.local/bin"
    cat > "$HOME/.local/bin/xharvester" << EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$HOME/xharvester/launch_android.sh" "\$@"
EOF
    chmod +x "$HOME/.local/bin/xharvester"
}

# Function to setup termux permissions
setup_permissions() {
    echo -e "${CYAN}[STEP 6/6]${NC} Setting up Termux permissions..."
    
    echo -e "${YELLOW}[INFO]${NC} For full functionality, xharvester may need:"
    echo -e "${BLUE}  • Storage access for file operations${NC}"
    echo -e "${BLUE}  • Network access for updates${NC}"
    echo -e "${BLUE}  • Root access for advanced features (optional)${NC}"
    
    # Request storage permission
    echo -e "${GREEN}Requesting storage permission...${NC}"
    termux-setup-storage
    
    echo -e "${GREEN}✅ Basic setup completed!${NC}"
}

# Function to show completion message
show_completion() {
    echo ""
    echo -e "${GREEN}🎉 xharvester installation completed successfully!${NC}"
    echo ""
    echo -e "${CYAN}📱 Android/Termux Specific Notes:${NC}"
    echo -e "${BLUE}  • xharvester is optimized for Android/Termux${NC}"
    echo -e "${BLUE}  • Some features may have limited functionality${NC}"
    echo -e "${BLUE}  • CAN bus features work in simulation mode${NC}"
    echo -e "${BLUE}  • No root privileges required for basic usage${NC}"
    echo ""
    echo -e "${CYAN}🚀 Usage:${NC}"
    echo -e "${GREEN}  Method 1: ${YELLOW}xharvester${NC}"
    echo -e "${GREEN}  Method 2: ${YELLOW}cd ~/xharvester && ./launch_android.sh${NC}"
    echo -e "${GREEN}  Method 3: ${YELLOW}cd ~/xharvester && python xharvester${NC}"
    echo ""
    echo -e "${CYAN}📁 Installation Directory:${NC} ${YELLOW}$HOME/xharvester${NC}"
    echo ""
    echo -e "${CYAN}🔧 Optional Enhancements:${NC}"
    echo -e "${GREEN}  • Install root access: ${YELLOW}pkg install tsu${NC}"
    echo -e "${GREEN}  • Install additional tools: ${YELLOW}pkg install nmap netcat-openbsd${NC}"
    echo ""
    echo -e "${YELLOW}Ready to hack responsibly! 🛡️${NC}"
}

# Main installation process
main() {
    echo -e "${BLUE}[INFO]${NC} Starting xharvester installation for Android/Termux..."
    echo ""
    
    install_packages
    setup_xharvester
    create_launcher
    setup_permissions
    show_completion
    
    echo ""
    echo -e "${GREEN}Installation completed! You can now run: ${YELLOW}xharvester${NC}"
}

# Run installation
main