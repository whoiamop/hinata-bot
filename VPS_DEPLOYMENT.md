# 🌸 HINATA BOT - VPS Deployment Guide

## Created By Axl

---

## 📋 Prerequisites

- A VPS (Virtual Private Server) with:
  - Ubuntu 20.04/22.04 or Debian 10/11
  - Minimum 1GB RAM
  - Minimum 10GB storage
- Root or sudo access
- Your Bot Token from @BotFather

---

## 🚀 Step-by-Step Deployment

### Step 1: Connect to Your VPS

```bash
ssh root@your_vps_ip
```

### Step 2: Update System

```bash
apt update && apt upgrade -y
```

### Step 3: Install Required Packages

```bash
apt install -y python3 python3-pip python3-venv git screen
```

### Step 4: Create Bot Directory

```bash
mkdir -p /opt/hinata_bot
cd /opt/hinata_bot
```

### Step 5: Upload Bot Files

Upload all bot files to `/opt/hinata_bot/` using SCP or SFTP:

```bash
# From your local machine
scp -r /path/to/hinata_bot/* root@your_vps_ip:/opt/hinata_bot/
```

### Step 6: Create Virtual Environment

```bash
cd /opt/hinata_bot
python3 -m venv venv
source venv/bin/activate
```

### Step 7: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 8: Set Environment Variables

```bash
export BOT_TOKEN="your_bot_token_here"
```

To make it permanent:

```bash
echo 'export BOT_TOKEN="your_bot_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 9: Test Bot

```bash
cd /opt/hinata_bot
source venv/bin/activate
python3 bot.py
```

If everything works, stop it with `Ctrl+C`

---

## 🔄 Running Bot 24/7

### Method 1: Using Screen (Recommended for Beginners)

```bash
# Create a new screen session
screen -S hinata_bot

# Navigate to bot directory
cd /opt/hinata_bot
source venv/bin/activate

# Run the bot
python3 bot.py

# Detach from screen (bot keeps running)
# Press: Ctrl+A, then D

# To reattach later
screen -r hinata_bot

# To stop the bot
screen -r hinata_bot
# Press: Ctrl+C
```

### Method 2: Using Systemd Service (Recommended for Production)

Create a service file:

```bash
nano /etc/systemd/system/hinata_bot.service
```

Add this content:

```ini
[Unit]
Description=Hinata Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hinata_bot
Environment=BOT_TOKEN=your_bot_token_here
ExecStart=/opt/hinata_bot/venv/bin/python3 /opt/hinata_bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
systemctl daemon-reload

# Enable service (start on boot)
systemctl enable hinata_bot

# Start the service
systemctl start hinata_bot

# Check status
systemctl status hinata_bot

# View logs
journalctl -u hinata_bot -f

# Stop the service
systemctl stop hinata_bot

# Restart the service
systemctl restart hinata_bot
```

---

## 📊 Monitoring

### Check if Bot is Running

```bash
# Using systemd
systemctl status hinata_bot

# Using screen
screen -ls

# Check processes
ps aux | grep bot.py
```

### View Logs

```bash
# Using systemd
journalctl -u hinata_bot -f

# Using screen
screen -r hinata_bot

# View bot logs
tail -f /opt/hinata_bot/bot.log
```

---

## 🔄 Updating the Bot

```bash
# Stop the bot
systemctl stop hinata_bot

# Navigate to bot directory
cd /opt/hinata_bot

# Backup database
cp hinata_bot.db hinata_bot.db.backup

# Upload new files
scp -r /path/to/new/files/* root@your_vps_ip:/opt/hinata_bot/

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Start the bot
systemctl start hinata_bot
```

---

## 🔒 Security Tips

1. **Use a firewall:**
```bash
ufw allow ssh
ufw enable
```

2. **Create a non-root user for the bot:**
```bash
useradd -m -s /bin/bash hinata
chown -R hinata:hinata /opt/hinata_bot
```

3. **Update the service file to use non-root user:**
```ini
User=hinata
Group=hinata
```

---

## 🛠️ Troubleshooting

### Bot Not Starting

```bash
# Check Python version
python3 --version

# Check if virtual environment is activated
which python3

# Check logs
journalctl -u hinata_bot -n 50
```

### Permission Denied

```bash
# Fix permissions
chmod -R 755 /opt/hinata_bot
chown -R root:root /opt/hinata_bot
```

### Module Not Found

```bash
# Reinstall dependencies
cd /opt/hinata_bot
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Database Issues

```bash
# Check database file
ls -la /opt/hinata_bot/*.db

# Backup and recreate if corrupted
cp hinata_bot.db hinata_bot.db.corrupted
rm hinata_bot.db
```

---

## 📱 Useful Commands

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check network connections
netstat -tulpn

# Restart VPS
reboot
```

---

## 🌐 Popular VPS Providers

- **DigitalOcean** - $5/month
- **Linode** - $5/month
- **Vultr** - $5/month
- **AWS Lightsail** - $5/month
- **Google Cloud** - Free tier available
- **Oracle Cloud** - Always free tier

---

## 📞 Support

If you face any issues:
- Check logs: `journalctl -u hinata_bot -f`
- Contact Owner: @Axl
- Group: https://t.me/+nNmiWyK3oV04ZGM1

---

**Hinata Bot - Created By Axl** 🌸
