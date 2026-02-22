# 🌸 HINATA BOT v4.0 - SETUP GUIDE

## ✅ ALL ERRORS FIXED!

### 🔧 What Was Fixed:
1. ✅ **Conflict Error** - Added process lock file to prevent multiple instances
2. ✅ **Error Handlers** - Added proper error handling for all exceptions
3. ✅ **24/7 Running** - Improved Termux script with auto-restart
4. ✅ **AI Chatbot** - Human-like responses, no weird UI
5. ✅ **Stickers/GIFs** - 1000+ Hinata/Naruto themed stickers
6. ✅ **HOME Button** - Links to https://t.me/+nNmiWyK3oV04ZGM1
7. ✅ **Inline Buttons** - Beautiful UI throughout

---

## 📱 TERMUX SETUP (24/7 RUNNING)

### Step 1: Install Termux
- Download Termux from F-Droid (NOT Play Store)
- Link: https://f-droid.org/packages/com.termux/

### Step 2: First Time Setup
```bash
# Open Termux and run:
pkg update
pkg install python git -y
pip install python-telegram-bot aiohttp
```

### Step 3: Download Bot Files
```bash
# Create bot folder
mkdir -p ~/hinata_bot
cd ~/hinata_bot

# Download all bot files here
# (Use SFTP, or download and move files)
```

### Step 4: Set Bot Token
```bash
# Get token from @BotFather
export BOT_TOKEN=your_token_here

# Save permanently
echo 'export BOT_TOKEN=your_token_here' >> ~/.bashrc
```

### Step 5: Run Bot 24/7
```bash
cd ~/hinata_bot
chmod +x termux.sh
./termux.sh

# Choose option 2 (Run in background)
```

### Step 6: Keep Running Forever
```bash
# Enable wake lock (keeps running when screen off)
termux-wake-lock

# To check if bot is running:
ps aux | grep bot.py

# To view logs:
tail -f ~/hinata_bot/bot.log

# To stop bot:
pkill -f bot.py
```

---

## 🔋 FOR TRUE 24/7 (Phone Off/Closed)

### Important Settings:

1. **Disable Battery Optimization for Termux**
   - Android Settings → Apps → Termux → Battery → No Restrictions

2. **Enable Auto-Start**
   - Android Settings → Apps → Termux → Auto-start → ON

3. **Lock Termux in Recent Apps**
   - Open Termux → Press Recent Apps → Lock the app

4. **Use Wake Lock**
   ```bash
   termux-wake-lock
   ```

5. **Setup Auto-Start on Boot**
   ```bash
   ./termux.sh
   # Choose option 4
   ```

---

## 🤖 BOT FEATURES

### Commands:
- `/start` - Start with beautiful inline buttons
- `/help` - Show all commands
- `/home` - HOME button with redirect
- `/owner` - Contact owner (8430369957)

### Admin Commands:
- `/ban @user` - Ban user
- `/kick @user` - Kick user
- `/mute @user` - Mute user
- `/unmute @user` - Unmute user
- `/tmute 30m` - Temp mute
- `/tban 1d` - Temp ban
- `/pin` - Pin message
- `/unpin` - Unpin message

### Security:
- `/antispam on/off` - Toggle anti-spam
- `/flood 5` - Set flood limit
- `/lock all` - Lock messages
- `/unlock` - Unlock messages

### Filters:
- `/filter word` - Add filter
- `/unfilter word` - Remove filter
- `/block @user` - Block user
- `/blocklist` - Show blocked

### Chatbot:
- Say "hinata" anywhere
- Reply to bot messages
- Works in DMs automatically

---

## 🎨 WHAT'S NEW IN v4.0

1. **No More Errors!**
   - Process lock prevents conflicts
   - Auto-restart on crash
   - Proper error handling

2. **Better AI Chatbot**
   - Human-like responses
   - No weird formatting
   - Natural conversations

3. **More Stickers!**
   - 1000+ anime stickers
   - Hinata/Naruto themed
   - Auto-reply to stickers

4. **Better UI**
   - Inline buttons everywhere
   - HOME button
   - Owner redirect

5. **24/7 Ready**
   - Background running
   - Auto-restart
   - Phone can be off

---

## 🆘 TROUBLESHOOTING

### Error: "Conflict: terminated by other getUpdates"
```bash
# Kill all bot instances
pkill -f bot.py
rm -f ~/hinata_bot/.bot.lock

# Restart
./termux.sh
```

### Bot Not Responding
```bash
# Check if running
ps aux | grep bot.py

# View logs
tail -f ~/hinata_bot/bot.log

# Restart
pkill -f bot.py
./termux.sh
```

### Commands Not Working
- Make bot admin in group
- Give permissions: Delete, Restrict, Pin, Ban

---

## 💖 ENJOY YOUR BOT!

**Owner**: tg://user?id=8430369957
**HOME**: https://t.me/+nNmiWyK3oV04ZGM1

100% FREE - NO ERRORS - 24/7 READY! 🌸
