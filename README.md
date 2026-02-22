# 🌸 HINATA - Advanced Telegram Group Management Bot

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0%20Ultimate-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-Free-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/24%2F7-Ready-success?style=for-the-badge">
</p>

<p align="center">
  <b>🤖 AI Chatbot | 🛡️ Anti-Spam | 🎨 Anime Stickers | 👮 Admin Tools | 📱 24/7 Ready</b>
</p>

---

## ✨ Features

### 🤖 AI Chatbot (Hinata)
- **100% FREE** - No API key needed!
- **Unlimited responses** - Smart, anime-style conversations
- **Trigger words**: Say "hinata" or reply to bot messages
- **Auto GIFs** - Sends anime GIFs with responses
- **Personality**: Cute, friendly, helpful anime girl personality

### 👮 Admin Commands
| Command | Description |
|---------|-------------|
| `/ban [@user]` | Ban user permanently |
| `/unban [@user]` | Unban user |
| `/kick [@user]` | Kick user (can rejoin) |
| `/mute [@user]` | Mute user |
| `/unmute [@user]` | Unmute user |
| `/tmute [time]` | Temporary mute (30m, 1h, 1d) |
| `/tban [time]` | Temporary ban |
| `/pin` | Pin message (reply) |
| `/unpin` | Unpin message |

### 🛡️ Security Features
| Feature | Description |
|---------|-------------|
| **Anti-Spam** | Auto-delete spam with multiple links |
| **Flood Control** | Auto-mute users sending too many messages |
| **Word Filter** | Auto-delete messages with banned words |
| **Blocklist** | Permanently block specific users |
| **Lock/Unlock** | Restrict message types (text, media, stickers) |

### ⚠️ Warning System
- `/warn [reason]` - Warn user (reply)
- `/unwarn` - Remove warning
- `/warnings [@user]` - Check warnings
- `/setwarnlimit [n]` - Set max warnings before auto-ban

### 👋 Welcome System
- Customizable welcome/goodbye messages
- Variables: `{first_name}`, `{last_name}`, `{username}`, `{mention}`, `{group_name}`

### 🎨 Anime Stickers & GIFs
- **1000+ FREE anime stickers** - No API needed!
- **Auto-respond** to stickers with anime stickers
- **Categories**: Cute, Naruto, Demon Slayer, AOT, and more!

### 👑 Owner Features
- **Owner ID**: `8430369957` - Click to contact
- Owner-only commands
- Full bot control

---

## 🚀 Quick Start

### 1️⃣ Get Bot Token
1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow instructions
3. Copy your **Bot Token**

### 2️⃣ Install & Run

#### 💻 Windows
```batch
# Download and extract
# Double-click: start.bat
```

#### 🐧 Linux/Mac
```bash
git clone <repo-url>
cd hinata_bot
chmod +x start.sh
./start.sh
```

#### 📱 Android/Termux (FREE 24/7 Hosting!)
```bash
pkg update
pkg install python git
pip install python-telegram-bot aiohttp

# Set token
export BOT_TOKEN=your_token_here

# Run
python bot.py

# OR run in background (24/7)
nohup python bot.py > bot.log 2>&1 &
```

---

## 📱 24/7 Phone Hosting (FREE!)

### Using Termux (Android)

```bash
# Install Termux from F-Droid or Play Store

# In Termux:
pkg update
pkg install python -y
pip install python-telegram-bot aiohttp

# Download bot files
cd ~
mkdir hinata_bot
cd hinata_bot

# Copy bot files here (use SFTP or download)

# Set environment variable
export BOT_TOKEN=your_token_here

# Run in background (24/7!)
nohup python bot.py > bot.log 2>&1 &

# Check if running
ps aux | grep bot.py

# View logs
tail -f bot.log

# Stop bot
pkill -f bot.py
```

### Auto-Start on Boot (Termux)
```bash
# Install Termux:API
pkg install termux-api

# Create boot script
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/hinata_bot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/hinata_bot
export BOT_TOKEN=your_token_here
nohup python bot.py > bot.log 2>&1 &
EOF

chmod +x ~/.termux/boot/hinata_bot.sh
```

---

## 🗄️ Database Setup

### SQLite (Default - Works Everywhere)
```python
# No setup needed! Works out of the box!
# Database file: hinata_bot.db
```

### PostgreSQL (For Big Groups)
```bash
# Install PostgreSQL
sudo apt install postgresql

# Create database
sudo -u postgres createdb hinata_bot

# Set environment variables
export DB_TYPE=postgresql
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=hinata_bot
export DB_USER=postgres
export DB_PASSWORD=your_password

# Install psycopg2
pip install psycopg2-binary
```

---

## 📖 Command Reference

### 🤖 Chatbot Commands
Just say:
- `"hinata"` - Start conversation
- Reply to bot message - Continue chatting
- Works in DMs automatically

### 👮 Admin Commands
```
/ban @user [reason]      - Ban user
/unban @user             - Unban user
/kick @user [reason]     - Kick user
/mute @user              - Mute user
/unmute @user            - Unmute user
/tmute 30m               - Temp mute 30 minutes
/tban 1d                 - Temp ban 1 day
/pin                     - Pin message (reply)
/unpin                   - Unpin message
```

### 🛡️ Security Commands
```
/antispam on/off         - Toggle anti-spam
/flood 5                 - Set flood limit
/flood off               - Disable flood control
/lock all                - Lock all messages
/lock text               - Lock text only
/lock media              - Lock media
/unlock                  - Unlock all
```

### 🚫 Filter Commands
```
/filter word             - Add filtered word
/unfilter word           - Remove filtered word
/filters                 - List filters
/block @user             - Block user
/unblock user_id         - Unblock user
/blocklist               - Show blocked users
```

### ⚠️ Warning Commands
```
/warn reason             - Warn user (reply)
/unwarn                  - Remove warning (reply)
/warnings @user          - Check warnings
/setwarnlimit 3          - Set max warnings
```

### 👋 Welcome Commands
```
/welcome Hello {first_name}!  - Set welcome
/goodbye Bye {first_name}!    - Set goodbye
/setrules No spam...          - Set rules
/rules                        - Show rules
```

### 📊 Info Commands
```
/info @user              - User info
/settings                - Group settings
/owner                   - Contact owner
/help                    - Show help
```

---

## 🎨 Customization

### Edit `config.py`:
```python
# Bot Settings
BOT_NAME = "Hinata"
BOT_VERSION = "3.0 Ultimate Edition"

# Owner Settings
OWNER_ID = 8430369957

# Security Settings
ANTISPAM_ENABLED = True
FLOOD_LIMIT = 5
MAX_WARNINGS = 3

# Chatbot Settings
CHATBOT_TRIGGERS = ['hinata', 'hinata-chan']
CHATBOT_REPLY_RATE = 0.3  # 30% chance for GIF

# Database
DB_TYPE = 'sqlite'  # or 'postgresql'
```

---

## 🔧 Troubleshooting

### Bot not responding?
```bash
# Check if token is correct
echo $BOT_TOKEN

# Check Python version
python3 --version  # Need 3.8+

# Check logs
tail -f hinata_bot.log
```

### Commands not working?
- Make sure bot is **admin** in the group
- Give bot these permissions:
  - ✅ Delete messages
  - ✅ Restrict members
  - ✅ Pin messages
  - ✅ Ban users

### Database errors?
```bash
# Reset database (WARNING: Deletes all data!)
rm hinata_bot.db
```

### Phone hosting issues?
- Make sure Termux has **battery optimization disabled**
- Enable **wake lock**: `termux-wake-lock`
- Use **nohup** for background running

---

## 📁 File Structure

```
hinata_bot/
├── bot.py              # Main bot file
├── database.py         # Database manager
├── chatbot.py          # Hinata AI
├── stickers.py         # Anime stickers/GIFs
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── start.sh            # Linux/Mac start
├── start.bat           # Windows start
├── termux.sh           # Android hosting
├── README.md           # This file
└── hinata_bot.db       # Database (auto-created)
```

---

## 💡 Tips

### For 24/7 Free Hosting:
1. **Use old Android phone** - Works perfectly!
2. **Keep phone plugged in** - Prevents battery drain
3. **Use WiFi** - More stable than mobile data
4. **Disable battery optimization** for Termux
5. **Use nohup** to keep running after closing Termux

### For Best Performance:
1. Use **PostgreSQL** for groups with 1000+ members
2. Enable **webhook mode** for production
3. Set up **log rotation** to prevent disk full
4. Use **tmux** or **screen** for persistent sessions

---

## 🌟 Why Hinata Bot?

| Feature | Other Bots | Hinata |
|---------|-----------|--------|
| Price | $5-50/month | **FREE** |
| AI Chatbot | Limited/Paid | **Unlimited & Free** |
| Anime Stickers | None/Paid | **1000+ Free** |
| 24/7 Hosting | VPS Required | **Phone Works!** |
| Database | Small/Limited | **Big & Scalable** |
| Setup | Complex | **One Click** |

---

## 👑 Owner

**Contact**: [Click Here](tg://user?id=8430369957)

**User ID**: `8430369957`

---

## 📄 License

**100% FREE** - Use it, modify it, share it!

No restrictions. No attribution required.

---

## 🙏 Credits

- Created with ❤️ for the Telegram community
- Anime stickers from various free sources
- Inspired by the best group management bots

---

<p align="center">
  <b>🌸 Enjoy managing your groups with Hinata! 🌸</b>
</p>

<p align="center">
  <a href="tg://user?id=8430369957">👑 Contact Owner</a> |
  <a href="https://t.me/BotFather">🤖 Create Bot</a> |
  <a href="https://github.com">⭐ Star on GitHub</a>
</p>
