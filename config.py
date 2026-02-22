#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  ⚙️ HINATA BOT CONFIGURATION                                              ║
║  24/7 Ready | Phone Hostable | Free Forever                               ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os

class Config:
    """
    ⚙️ Hinata Bot Configuration
    All settings are customizable!
    """
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔑 BOT TOKEN (REQUIRED)
    # ═══════════════════════════════════════════════════════════════════════
    
    # Get from @BotFather
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👑 OWNER SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Owner Telegram ID - For redirect and admin commands
    OWNER_ID = 8430369957
    OWNER_NAME = "Developer"
    OWNER_USERNAME = ""  # Optional: @username
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🤖 BOT INFO
    # ═══════════════════════════════════════════════════════════════════════
    
    BOT_NAME = "Hinata"
    BOT_VERSION = "3.0 Ultimate Edition"
    BOT_DESCRIPTION = "Advanced Group Management Bot with AI Chatbot"
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🗄️ DATABASE SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Database Type: 'sqlite' or 'postgresql'
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    
    # SQLite Settings (Default - works everywhere)
    SQLITE_PATH = os.getenv('DB_PATH', 'hinata_bot.db')
    
    # PostgreSQL Settings (For production/24/7 hosting)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'hinata_bot')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🛡️ SECURITY SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Anti-Spam Settings
    ANTISPAM_ENABLED = True
    ANTISPAM_LINK_LIMIT = 2  # Max links per message
    ANTISPAM_MENTION_LIMIT = 5  # Max mentions per message
    
    # Flood Control
    FLOOD_ENABLED = True
    FLOOD_LIMIT = 5  # Messages per 10 seconds
    FLOOD_MUTE_DURATION = 300  # 5 minutes
    
    # Warning System
    MAX_WARNINGS = 3  # Ban after X warnings
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🤖 CHATBOT SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Chatbot Trigger Words
    CHATBOT_TRIGGERS = ['hinata', 'hinata-chan', 'ヒナタ']
    
    # Chatbot Response Settings
    CHATBOT_REPLY_RATE = 0.3  # 30% chance to send GIF with response
    CHATBOT_TYPING_DELAY = 0.5  # Seconds
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎨 STICKER SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Auto-Sticker Response Rate
    STICKER_REPLY_RATE = 0.4  # 40% chance to reply to stickers
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📊 LOGGING SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Log Level: DEBUG, INFO, WARNING, ERROR
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Log to File
    LOG_TO_FILE = True
    LOG_FILE = 'hinata_bot.log'
    
    # ═══════════════════════════════════════════════════════════════════════
    # ⚡ PERFORMANCE SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Message Handler Groups (Lower = Higher Priority)
    CHATBOT_GROUP = 1
    FILTER_GROUP = 2
    
    # Rate Limiting
    RATE_LIMIT_CALLS = 5
    RATE_LIMIT_PERIOD = 60  # Seconds
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🌐 WEBHOOK SETTINGS (For 24/7 hosting)
    # ═══════════════════════════════════════════════════════════════════════
    
    # Use Webhook instead of Polling (for production)
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'False').lower() == 'true'
    
    # Webhook URL (Required if USE_WEBHOOK = True)
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    
    # Webhook Port
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 8443))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📱 PHONE HOSTING SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # For Termux/Android hosting
    TERMUX_MODE = os.getenv('TERMUX_MODE', 'False').lower() == 'true'
    
    # Auto-restart on crash
    AUTO_RESTART = True
    
    # Restart delay (seconds)
    RESTART_DELAY = 5
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎨 UI SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Use Decorative UI
    FANCY_UI = True
    
    # Box Style: 'single', 'double', 'rounded'
    BOX_STYLE = 'single'
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔧 MAINTENANCE SETTINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Auto-cleanup old data
    AUTO_CLEANUP = True
    CLEANUP_DAYS = 30
    
    # Cleanup interval (hours)
    CLEANUP_INTERVAL = 24
