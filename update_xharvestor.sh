#!/bin/bash

# XHARVESTOR Updater Script
REPO_URL="https://github.com/n3tworkh4x/xharvestor.git"
DIR="xharvestor"
BRANCH="main"
INSTALL_DIR="/opt"  # Change this to your preferred installation directory

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Git is not installed. Please install git first.${NC}"
        echo -e "For Ubuntu/Debian: sudo apt install git"
        echo -e "For CentOS/RHEL: sudo yum install git"
        exit 1
    fi
}

# Function to update the repository
update_repo() {
    echo -e "${BLUE}🚀 Checking for updates...${NC}"
    
    if [ -d "$INSTALL_DIR/$DIR" ] && [ -d "$INSTALL_DIR/$DIR/.git" ]; then
        cd "$INSTALL_DIR/$DIR" || exit 1
        
        # Check if there are any local changes
        if ! git diff --quiet; then
            echo -e "${YELLOW}Warning: Local changes detected. Stashing changes before update.${NC}"
            git stash
        fi
        
        # Fetch updates
        git fetch origin
        
        # Check if we're on the correct branch
        CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
        if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
            echo -e "${YELLOW}Currently on branch '$CURRENT_BRANCH', switching to '$BRANCH'${NC}"
            git checkout "$BRANCH"
        fi
        
        # Reset to the latest version
        git reset --hard "origin/$BRANCH"
        
        # Clean untracked files
        git clean -fd
        
        echo -e "${GREEN}Update completed successfully!${NC}"
        
        # Check if we stashed any changes
        if git stash list | grep -q "stash@{0}"; then
            echo -e "${YELLOW}Note: Your local changes were stashed. Use 'git stash pop' to restore them if needed.${NC}"
        fi
    else
        echo -e "${BLUE}Cloning repository for the first time...${NC}"
        sudo mkdir -p "$INSTALL_DIR"
        sudo chown "$USER:$USER" "$INSTALL_DIR"
        cd "$INSTALL_DIR" || exit 1
        git clone "$REPO_URL"
        cd "$DIR" || exit 1
        echo -e "${GREEN}Installation completed successfully!${NC}"
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}🚀 Checking and installing dependencies...${NC}"
    
    # Check if Python3 is installed
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python3 is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Check if pip3 is installed
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}pip3 is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Install colorama if not present
    if ! python3 -c "import colorama" 2>/dev/null; then
        echo -e "${YELLOW}Installing colorama...${NC}"
        pip3 install colorama
    fi
    
    # Make the script executable
    chmod +x xharvestor
    
    echo -e "${GREEN}Dependency check completed!${NC}"
}

# Function to create a desktop shortcut (optional)
create_shortcut() {
    if [ -d "$HOME/Desktop" ]; then
        echo -e "${BLUE}🚀 Creating desktop shortcut...${NC}"
        cat > "$HOME/Desktop/XHARVESTOR.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=XHARVESTOR
Comment=Extended Reconnaissance Toolkit
Exec=python3 $INSTALL_DIR/$DIR/xharvestor.py
Icon=utilities-terminal
Terminal=true
Categories=Security;
EOF
        chmod +x "$HOME/Desktop/XHARVESTOR.desktop"
        echo -e "${GREEN}Desktop shortcut created!${NC}"
    fi
}

# Function to create a symlink in /usr/local/bin for easy execution
create_symlink() {
    echo -e "${BLUE}Creating symlink for easy execution...${NC}"
    sudo ln -sf "$INSTALL_DIR/$DIR/xharvestor" /usr/local/bin/xharvestor 2>/dev/null || true
    echo -e "${GREEN}You can now run XHARVESTOR by typing 'xharvestor' in the terminal!${NC}"
}

# Main execution
check_git
update_repo
install_dependencies
create_symlink

# Ask about creating desktop shortcut
read -rp "Do you want to create a desktop shortcut? (y/N): " create_shortcut_answer
if [[ $create_shortcut_answer =~ ^[Yy]$ ]]; then
    create_shortcut
fi

echo -e "${GREEN}XHARVESTOR has been successfully updated/installed!${NC}"
echo -e "You can now run it by typing: ${YELLOW}python3 $INSTALL_DIR/$DIR/xharvestor${NC}"
echo -e "Or simply: ${YELLOW}xharvestor${NC} (if symlink was created successfully)"