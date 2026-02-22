#!/bin/bash
# HINATA BOT - Termux Runner Script
# Created By Axl

echo "================================"
echo "  🌸 HINATA BOT - Termux 🌸"
echo "  Created By Axl"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in Termux
if [ -z "$TERMUX_VERSION" ] && [ -z "$TERMUX_API_VERSION" ]; then
    echo -e "${YELLOW}Warning: Not running in Termux environment${NC}"
fi

# Update packages
echo -e "${YELLOW}[1/5] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install required packages
echo -e "${YELLOW}[2/5] Installing required packages...${NC}"
pkg install -y python python-pip git

# Install Python dependencies
echo -e "${YELLOW}[3/5] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install python-telegram-bot aiohttp

# Check if bot files exist
if [ ! -f "bot.py" ]; then
    echo -e "${RED}Error: bot.py not found!${NC}"
    echo "Please make sure all bot files are in the current directory."
    exit 1
fi

# Check for BOT_TOKEN
if [ -z "$BOT_TOKEN" ]; then
    echo -e "${YELLOW}[4/5] BOT_TOKEN not set!${NC}"
    echo "Please enter your Bot Token from @BotFather:"
    read -r token
    export BOT_TOKEN="$token"
    echo "export BOT_TOKEN=\"$token\"" >> ~/.bashrc
fi

# Run bot
echo -e "${GREEN}[5/5] Starting Hinata Bot...${NC}"
echo ""
echo "================================"
echo "  Bot is running!"
echo "  Press Ctrl+C to stop"
echo "================================"
echo ""

# Run the bot
python3 bot.py
