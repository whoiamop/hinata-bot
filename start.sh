#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🤖 HINATA BOT - START SCRIPT (Linux/Mac)
# 24/7 Ready | Auto-Restart | Phone Hostable
# ═══════════════════════════════════════════════════════════════════════════

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🌸  ʜɪɴᴀᴛᴀ - ᴀᴅᴠᴀɴᴄᴇᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ  🌸         ║"
echo "║                                                                ║"
echo "║     Version: 3.0 Ultimate Edition                             ║"
echo "║     Owner: tg://user?id=8430369957                            ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
echo -e "${CYAN}🔍 Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo -e "${YELLOW}📥 Install Python 3.8+ and try again${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo -e "${CYAN}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${CYAN}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${CYAN}⬆️  Upgrading pip...${NC}"
pip install -q --upgrade pip

# Install requirements
echo -e "${CYAN}📥 Installing dependencies...${NC}"
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Check bot token
if [ -z "$BOT_TOKEN" ]; then
    echo -e "${YELLOW}"
    echo "⚠️  WARNING: BOT_TOKEN not set!"
    echo "   Set it with: export BOT_TOKEN=your_token_here"
    echo ""
    echo -e "${NC}"
fi

# Create necessary directories
mkdir -p logs
mkdir -p backups

# Function to run bot with auto-restart
run_bot() {
    while true; do
        echo -e "${GREEN}"
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║  🚀 Starting Hinata Bot...                                    ║"
        echo "║  Press Ctrl+C to stop                                         ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        python3 bot.py
        
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ] || [ $EXIT_CODE -eq 130 ]; then
            echo -e "${YELLOW}👋 Bot stopped by user${NC}"
            break
        else
            echo -e "${RED}"
            echo "╔════════════════════════════════════════════════════════════════╗"
            echo "║  ⚠️  Bot crashed! Restarting in 5 seconds...                  ║"
            echo "╚════════════════════════════════════════════════════════════════╝"
            echo -e "${NC}"
            sleep 5
        fi
    done
}

# Run the bot
run_bot
