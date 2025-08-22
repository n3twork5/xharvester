#!/bin/bash

# XHARVESTER Updater Script
REPO_URL="https://github.com/n3tworkh4x/xharvester.git"
DIR="xharvester"
BRANCH="main"

# Default installation directory (user home for no sudo required)
DEFAULT_INSTALL_DIR="$HOME/.local/share"
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() { echo -e "${GREEN}[+]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[-]${NC} $1"; }
print_info() { echo -e "${BLUE}[*]${NC} $1"; }

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install git first."
        echo -e "For Ubuntu/Debian: ${CYAN}sudo apt install git${NC}"
        echo -e "For CentOS/RHEL: ${CYAN}sudo yum install git${NC}"
        echo -e "For Arch: ${CYAN}sudo pacman -S git${NC}"
        exit 1
    fi
    print_status "Git is installed"
}

# Detect if we're running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root - this is not recommended for security reasons"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        INSTALL_DIR="/opt"
    fi
}

# Function to update the repository
update_repo() {
    print_info "Checking for updates..."
    
    if [ -d "$INSTALL_DIR/$DIR" ] && [ -d "$INSTALL_DIR/$DIR/.git" ]; then
        cd "$INSTALL_DIR/$DIR" || exit 1
        
        # Check if there are any local changes
        if ! git diff --quiet; then
            print_warning "Local changes detected."
            echo "Options:"
            echo "1) Stash changes and update"
            echo "2) Discard changes and update"
            echo "3) Abort update"
            read -rp "Choose option (1/2/3): " change_option
            
            case $change_option in
                1)
                    git stash
                    print_info "Changes stashed"
                    ;;
                2)
                    git reset --hard HEAD
                    git clean -fd
                    print_info "Changes discarded"
                    ;;
                3)
                    print_info "Update aborted"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option"
                    exit 1
                    ;;
            esac
        fi
        
        # Fetch updates
        git fetch origin
        
        # Check if we're on the correct branch
        CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "unknown")
        if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
            print_warning "Currently on branch '$CURRENT_BRANCH', switching to '$BRANCH'"
            git checkout "$BRANCH"
        fi
        
        # Check if we're behind origin
        if git status | grep -q "Your branch is behind"; then
            git pull origin "$BRANCH"
            print_status "Update completed successfully!"
        else
            print_status "Already up to date!"
        fi
        
    else
        print_info "Cloning repository for the first time..."
        mkdir -p "$INSTALL_DIR"
        cd "$INSTALL_DIR" || exit 1
        git clone "$REPO_URL"
        cd "$DIR" || exit 1
        print_status "Installation completed successfully!"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_info "Checking and installing dependencies..."
    
    # Check if Python3 is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed. Please install it first."
        echo -e "For Ubuntu/Debian: ${CYAN}sudo apt install python3 python3-pip${NC}"
        echo -e "For CentOS/RHEL: ${CYAN}sudo yum install python3 python3-pip${NC}"
        echo -e "For Arch: ${CYAN}sudo pacman -S python python-pip${NC}"
        exit 1
    fi
    
    # Check if pip3 is installed
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install it first."
        exit 1
    fi
    
    # Install required Python packages
    print_info "Installing Python dependencies..."
    pip3 install colorama requests --break-system-packages
    
    # Make the script executable
    chmod +x xharvester
    
    print_status "Dependency check completed!"
}

# Function to create a symlink for easy execution
create_symlink() {
    print_info "Creating symlink for easy execution..."
    
    # Try system-wide location first (if running as root)
    if [ "$EUID" -eq 0 ]; then
        ln -sf "$INSTALL_DIR/$DIR/xharvester" /usr/local/bin/xharvester 2>/dev/null && \
        print_status "System-wide symlink created in /usr/local/bin/"
    else
        # Try user-local bin directory
        if [ -d "$HOME/.local/bin" ]; then
            ln -sf "$INSTALL_DIR/$DIR/xharvester" "$HOME/.local/bin/xharvester" 2>/dev/null && \
            print_status "User symlink created in ~/.local/bin/"
        else
            mkdir -p "$HOME/.local/bin"
            ln -sf "$INSTALL_DIR/$DIR/xharvester" "$HOME/.local/bin/xharvester" 2>/dev/null && \
            print_status "Created ~/.local/bin/ and symlink"
            print_warning "Add $HOME/.local/bin to your PATH if it's not already there"
            echo "Add this to your ~/.bashrc or ~/.zshrc:"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    fi
}

# Function to create a desktop shortcut (optional)
create_shortcut() {
    if [ -d "$HOME/Desktop" ] && command -v xdg-desktop-menu &> /dev/null; then
        print_info "Creating desktop shortcut..."
        cat > "/tmp/xharvester.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=xharvester
Comment=Extended Reconnaissance Toolkit - Develop by N3twork -- Kofi Yesu
Exec=python3 $INSTALL_DIR/$DIR/xharvester
Icon=utilities-terminal
Terminal=true
Categories=information-gathering;
EOF
        
        # Try to install the desktop file
        if [ "$EUID" -eq 0 ]; then
            desktop-file-install --dir=/usr/share/applications /tmp/xharvester.desktop
        else
            mkdir -p "$HOME/.local/share/applications"
            cp "/tmp/xharvester.desktop" "$HOME/.local/share/applications/"
        fi
        rm -f "/tmp/xharvester.desktop"
        print_status "Desktop shortcut created!"
    fi
}

# Main execution function
main() {
    echo -e "${CYAN}"
    echo "┌─────────────────────────────────────────────────────┐"
    echo "│              XHARVESTER UPDATER                     │"
    echo "└─────────────────────────────────────────────────────┘"
    echo -e "${NC}"
    
    check_root
    check_git
    update_repo
    install_dependencies
    create_symlink
    
    # Ask about creating desktop shortcut
    read -rp "Do you want to create a desktop shortcut? (y/N): " create_shortcut_answer
    if [[ $create_shortcut_answer =~ ^[Yy]$ ]]; then
        create_shortcut
    fi
    
    echo -e "${GREEN}XHARVESTER has been successfully updated/installed!${NC}"
    echo -e "You can now run it by typing: ${YELLOW}python3 $INSTALL_DIR/$DIR/xharvester${NC}"
    echo -e "Or simply: ${YELLOW}xharvester${NC} (if symlink was created successfully)"
}

# Run main function
main
