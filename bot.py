#!/usr/bin/env python3
"""
HINATA BOT - Created By Axl
Advanced Telegram Group Management Bot
Version: 3.0 - ULTIMATE EDITION
Real Human Brain AI + Memory System
"""

import logging
import os
import sys
import random
import re
import atexit
from datetime import datetime, timedelta
from functools import wraps

from telegram import (
    Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)
from telegram.constants import ChatType
from telegram.error import BadRequest, Forbidden, TimedOut, NetworkError

from database import DatabaseManager
from chatbot import HinataAI
from stickers import StickerManager
from games import GamesManager
from config import Config

logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

LOCK_FILE = ".bot.lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = f.read().strip()
            os.kill(int(old_pid), 0)
            print(f"Bot already running (PID: {old_pid})")
            sys.exit(1)
        except (ProcessLookupError, ValueError):
            os.remove(LOCK_FILE)
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

acquire_lock()
atexit.register(release_lock)

# Load configuration
config = Config()

# Initialize managers
db = DatabaseManager()
chatbot = HinataAI(db_manager=db)  # Pass database for memory system
sticker_mgr = StickerManager(db=db)  # Pass database for sticker collection
games = GamesManager()

# Get from config
OWNER_ID = config.OWNER_ID
HOME_GROUP_LINK = config.HOME_GROUP_LINK
SUPPORT_GROUP_LINK = config.SUPPORT_GROUP_LINK
BOT_TOKEN = os.getenv('BOT_TOKEN', config.BOT_TOKEN)

# ============ UTILITY FUNCTIONS ============

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_chat or update.effective_chat.type == ChatType.PRIVATE:
            await update.message.reply_text("ye command sirf groups mein kaam karti hai")
            return
        try:
            user = await update.effective_chat.get_member(update.effective_user.id)
            if user.status not in ['administrator', 'creator']:
                await update.message.reply_text("sirf admin use kar sakte hai ye command")
                return
        except:
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def owner_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("sirf owner use kar sakta hai ye command")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def parse_duration(time_str):
    if not time_str:
        return 0
    match = re.match(r'(\d+)([smhdw]?)', time_str.lower())
    if not match:
        return 0
    value, unit = int(match.group(1)), match.group(2)
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, '': 60}
    return value * multipliers.get(unit, 60)

def format_time(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"

async def is_admin(chat, user_id):
    try:
        member = await chat.get_member(user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

async def is_owner(user_id):
    return user_id == OWNER_ID

# ============ UI BUILDERS ============

def create_ui_box(title, content, emoji="✨"):
    lines = content.split('\n')
    max_len = max(len(line) for line in lines) if lines else 30
    width = min(max_len + 4, 50)
    top = f"╔{'═' * width}╗"
    header = f"║  {emoji} {title.center(width - 6)}  ║"
    separator = f"╠{'═' * width}╣"
    bottom = f"╚{'═' * width}╝"
    content_lines = []
    for line in lines:
        padded = line.ljust(width - 2)
        content_lines.append(f"║ {padded} ║")
    return f"{top}\n{header}\n{separator}\n" + "\n".join(content_lines) + f"\n{bottom}"

def create_inline_keyboard_with_close(buttons=None):
    if buttons is None:
        buttons = []
    keyboard = buttons.copy()
    keyboard.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(keyboard)

async def delete_message_after(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(job.chat_id, job.data)
    except:
        pass

async def auto_delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE, seconds=30):
    if update.message:
        context.job_queue.run_once(
            delete_message_after,
            seconds,
            chat_id=update.effective_chat.id,
            data=update.message.message_id,
            name=f"delete_{update.message.message_id}"
        )

# ============ BASIC COMMANDS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        text = create_ui_box(
            "HINATA BOT",
            "hey main hinata hu\ngroup manage kar sakti hu\n\n/help se commands dekh lo",
            "🌸"
        )
        keyboard = create_inline_keyboard_with_close([
            [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("📚 Help", callback_data="help")]
        ])
        msg = await update.message.reply_text(text, reply_markup=keyboard)
    else:
        msg = await update.message.reply_text("hey main hinata hu group mein swagat hai 🌸")
    await auto_delete_message(update, context, 60)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = create_ui_box(
        "HINATA COMMANDS",
        "👮 Admin:\n/ban /unban /kick /mute /unmute\n/tmute /tban /pin /unpin\n\n"
        "🛡️ Security:\n/antispam /flood /lock /unlock\n/antilink\n\n"
        "🚫 Filters:\n/filter /unfilter /filters\n/block /unblock /blocklist\n\n"
        "⚠️ Warnings:\n/warn /unwarn /warnings /setwarnlimit\n\n"
        "👋 Welcome:\n/welcome /goodbye /setrules /rules\n\n"
        "🎮 Games:\n/truth /dare /roll /coin /rps\n\n"
        "🤖 Chatbot:\n'hinata' bol ya reply kar",
        "📚"
    )
    keyboard = create_inline_keyboard_with_close()
    msg = await update.message.reply_text(text, reply_markup=keyboard)
    await auto_delete_message(update, context, 120)

async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = create_inline_keyboard_with_close([
        [InlineKeyboardButton("👤 Profile", url=f"tg://user?id={OWNER_ID}")]
    ])
    text = create_ui_box("OWNER INFO", f"👑 Owner ID: {OWNER_ID}\n📱 Direct Chat: /start", "👑")
    msg = await update.message.reply_text(text, reply_markup=keyboard)
    await auto_delete_message(update, context, 30)

async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Home Group", url=HOME_GROUP_LINK)],
        [InlineKeyboardButton("💬 Support", url=SUPPORT_GROUP_LINK)],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ])
    text = create_ui_box("HOME", f"🏠 Welcome to our home\n\nJoin the group for updates!\n\n{HOME_GROUP_LINK}", "🏠")
    msg = await update.message.reply_text(text, reply_markup=keyboard)
    await auto_delete_message(update, context, 30)

# ============ ADMIN COMMANDS ============

@admin_only
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            await update.message.reply_text("reply kar ya /ban @user")
            return
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko nahi ban kar sakti")
            return
        reason = " ".join(context.args[1:]) if len(context.args) > 1 else "no reason"
        await update.effective_chat.ban_member(user_id)
        text = create_ui_box("BAN", f"✅ {user_name} ko ban kar diya\nreason: {reason}", "🚫")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("/unban user_id")
            return
        user_id = int(context.args[0]) if context.args[0].isdigit() else context.args[0]
        await update.effective_chat.unban_member(user_id)
        text = create_ui_box("UNBAN", "✅ unban ho gaya", "✅")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def kick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            await update.message.reply_text("reply kar ya /kick @user")
            return
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko nahi kick kar sakti")
            return
        reason = " ".join(context.args[1:]) if len(context.args) > 1 else "no reason"
        await update.effective_chat.ban_member(user_id)
        await update.effective_chat.unban_member(user_id)
        text = create_ui_box("KICK", f"✅ {user_name} ko kick kar diya\nreason: {reason}", "👢")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            await update.message.reply_text("reply kar ya /mute @user")
            return
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko nahi mute kar sakti")
            return
        await update.effective_chat.restrict_member(user_id, ChatPermissions(can_send_messages=False))
        text = create_ui_box("MUTE", f"✅ {user_name} ko mute kar diya", "🔇")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            await update.message.reply_text("reply kar ya /unmute @user")
            return
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await update.effective_chat.restrict_member(user_id, perms)
        text = create_ui_box("UNMUTE", f"✅ {user_name} ko unmute kar diya", "🔊")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def tmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message or not context.args:
            await update.message.reply_text("reply karke /tmute 30m")
            return
        user_id = update.message.reply_to_message.from_user.id
        user_name = update.message.reply_to_message.from_user.first_name
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko nahi mute kar sakti")
            return
        seconds = parse_duration(context.args[0])
        if seconds == 0:
            await update.message.reply_text("galat time! 30m, 1h, 1d use kar")
            return
        until_date = datetime.now() + timedelta(seconds=seconds)
        await update.effective_chat.restrict_member(user_id, ChatPermissions(can_send_messages=False), until_date=until_date)
        text = create_ui_box("TEMP MUTE", f"✅ {user_name} ko {format_time(seconds)} ke liye mute kar diya", "🔇")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def tban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message or not context.args:
            await update.message.reply_text("reply karke /tban 1d")
            return
        user_id = update.message.reply_to_message.from_user.id
        user_name = update.message.reply_to_message.from_user.first_name
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko nahi ban kar sakti")
            return
        seconds = parse_duration(context.args[0])
        if seconds == 0:
            await update.message.reply_text("galat time! 30m, 1h, 1d use kar")
            return
        until_date = datetime.now() + timedelta(seconds=seconds)
        await update.effective_chat.ban_member(user_id, until_date=until_date)
        text = create_ui_box("TEMP BAN", f"✅ {user_name} ko {format_time(seconds)} ke liye ban kar diya", "🚫")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("pin karne ke liye reply kar")
            return
        await update.message.reply_to_message.pin()
        text = create_ui_box("PIN", "✅ pin ho gaya", "📌")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 10)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unpin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.effective_chat.unpin_message()
        text = create_ui_box("UNPIN", "✅ unpin ho gaya", "📌")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 10)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

# ============ SECURITY COMMANDS ============

@admin_only
async def antispam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        settings = db.get_group_settings(chat_id)
        status = "on" if settings.get('antispam_enabled') else "off"
        text = create_ui_box("ANTISPAM", f"status: {status}\n\n/antispam on ya off", "🛡️")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
        return
    arg = context.args[0].lower()
    if arg in ['on', 'yes']:
        db.set_group_setting(chat_id, 'antispam_enabled', True)
        text = create_ui_box("ANTISPAM", "✅ antispam on ho gaya", "🛡️")
    elif arg in ['off', 'no']:
        db.set_group_setting(chat_id, 'antispam_enabled', False)
        text = create_ui_box("ANTISPAM", "✅ antispam off ho gaya", "🛡️")
    else:
        text = create_ui_box("ANTISPAM", "/antispam on ya off", "🛡️")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def flood_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        settings = db.get_group_settings(chat_id)
        limit = settings.get('flood_limit', 5)
        text = create_ui_box("FLOOD CONTROL", f"limit: {limit} msgs\n\n/flood 5 ya /flood off", "🌊")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
        return
    arg = context.args[0].lower()
    if arg in ['off', 'disable']:
        db.set_group_setting(chat_id, 'flood_limit', 0)
        text = create_ui_box("FLOOD CONTROL", "✅ flood control off", "🌊")
    elif arg.isdigit():
        db.set_group_setting(chat_id, 'flood_limit', int(arg))
        text = create_ui_box("FLOOD CONTROL", f"✅ flood limit {arg} set", "🌊")
    else:
        text = create_ui_box("FLOOD CONTROL", "/flood 5 ya /flood off", "🌊")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def antilink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        settings = db.get_group_settings(chat_id)
        status = "on" if settings.get('antilink_enabled') else "off"
        text = create_ui_box("ANTILINK", f"status: {status}\n\n/antilink on ya off\n\nNOTE: sirf owner link bhej sakta hai", "🔗")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
        return
    arg = context.args[0].lower()
    if arg in ['on', 'yes']:
        db.set_group_setting(chat_id, 'antilink_enabled', True)
        text = create_ui_box("ANTILINK", "✅ antilink on ho gaya\n\nab sirf owner link bhej sakta hai", "🔗")
    elif arg in ['off', 'no']:
        db.set_group_setting(chat_id, 'antilink_enabled', False)
        text = create_ui_box("ANTILINK", "✅ antilink off ho gaya", "🔗")
    else:
        text = create_ui_box("ANTILINK", "/antilink on ya off", "🔗")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced /lock command with inline options"""
    if not context.args:
        # Show inline keyboard with lock options
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔒 All", callback_data="lock_all"),
             InlineKeyboardButton("📝 Text", callback_data="lock_text")],
            [InlineKeyboardButton("🎬 Media", callback_data="lock_media"),
             InlineKeyboardButton("🔤 Stickers", callback_data="lock_stickers")],
            [InlineKeyboardButton("📊 Polls", callback_data="lock_polls"),
             InlineKeyboardButton("🔗 Links", callback_data="lock_links")],
            [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
        ])
        text = create_ui_box("LOCK OPTIONS", "Select what to lock:\n\n✅ = Not Locked\n🔒 = Locked", "🔒")
        msg = await update.message.reply_text(text, reply_markup=keyboard)
        return
    
    lock_type = context.args[0].lower()
    await _apply_lock(lock_type, update, context)

async def _apply_lock(lock_type: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply lock to chat"""
    perms = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )
    if lock_type == 'all':
        perms = ChatPermissions()
    elif lock_type == 'text':
        perms.can_send_messages = False
    elif lock_type == 'media':
        perms.can_send_media_messages = False
    elif lock_type == 'stickers':
        perms.can_send_other_messages = False
    elif lock_type == 'polls':
        perms.can_send_polls = False
    elif lock_type == 'links':
        perms.can_add_web_page_previews = False
    else:
        await update.message.reply_text("❌ galat option")
        return
    try:
        await update.effective_chat.set_permissions(perms)
        text = create_ui_box("LOCK", f"✅ {lock_type} lock ho gaya", "🔒")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await update.effective_chat.set_permissions(perms)
        text = create_ui_box("UNLOCK", "✅ sab kuch unlock ho gaya", "🔓")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

# ============ FILTER COMMANDS ============

@admin_only
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/filter word")
        return
    db.add_filter_word(update.effective_chat.id, context.args[0].lower())
    text = create_ui_box("FILTER", f"✅ filter add ho gaya: {context.args[0]}", "🚫")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def remove_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/unfilter word")
        return
    db.remove_filter_word(update.effective_chat.id, context.args[0].lower())
    text = create_ui_box("FILTER", f"✅ filter remove ho gaya: {context.args[0]}", "✅")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filters_list = db.get_filter_words(update.effective_chat.id)
    if not filters_list:
        text = create_ui_box("FILTERS", "koi filter nahi hai", "🚫")
    else:
        content = "\n".join(f"• {w}" for w in filters_list)
        text = create_ui_box("FILTERED WORDS", content, "🚫")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 60)

@admin_only
async def block_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            await update.message.reply_text("reply kar ya /block @user")
            return
        db.add_to_blocklist(update.effective_chat.id, user_id, user_name)
        text = create_ui_box("BLOCK", f"✅ {user_name} ko block kar diya", "🚫")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unblock_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/unblock user_id")
        return
    try:
        user_id = int(context.args[0]) if context.args[0].isdigit() else context.args[0]
        db.remove_from_blocklist(update.effective_chat.id, user_id)
        text = create_ui_box("UNBLOCK", "✅ unblock ho gaya", "✅")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

async def blocklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    blocked = db.get_blocklist(update.effective_chat.id)
    if not blocked:
        text = create_ui_box("BLOCKLIST", "koi blocked nahi", "🚫")
    else:
        content = "\n".join(f"• {user['user_id']} = {user['name']}" for user in blocked)
        text = create_ui_box("BLOCKED USERS", content, "🚫")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 60)

# ============ WARNING COMMANDS ============

@admin_only
async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("reply karke warn de")
            return
        user_id = update.message.reply_to_message.from_user.id
        user_name = update.message.reply_to_message.from_user.first_name
        if await is_admin(update.effective_chat, user_id):
            await update.message.reply_text("admin ko warn nahi de sakti")
            return
        reason = " ".join(context.args) if context.args else "no reason"
        warning_count = db.add_warning(update.effective_chat.id, user_id, reason)
        settings = db.get_group_settings(update.effective_chat.id)
        max_warnings = settings.get('max_warnings', 3)
        if warning_count >= max_warnings:
            await update.effective_chat.ban_member(user_id)
            db.clear_warnings(update.effective_chat.id, user_id)
            text = create_ui_box("BAN", f"🚫 {user_name} ko ban kar diya (max warnings)", "🚫")
        else:
            text = create_ui_box("WARNING", f"⚠️ warning {warning_count}/{max_warnings}\nuser: {user_name}\nreason: {reason}", "⚠️")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 60)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text("reply kar")
            return
        user_id = update.message.reply_to_message.from_user.id
        user_name = update.message.reply_to_message.from_user.first_name
        warning_count = db.remove_warning(update.effective_chat.id, user_id)
        text = create_ui_box("UNWARN", f"✅ warning hat gayi {user_name} ke paas ab {warning_count} hai", "✅")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

async def check_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            user_name = update.message.reply_to_message.from_user.first_name
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user_id = member.user.id
            user_name = member.user.first_name
        else:
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name
        warning_count = db.get_warnings(update.effective_chat.id, user_id)
        settings = db.get_group_settings(update.effective_chat.id)
        max_warnings = settings.get('max_warnings', 3)
        text = create_ui_box("WARNINGS", f"⚠️ {user_name} ke paas {warning_count}/{max_warnings} warning hai", "⚠️")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

@admin_only
async def set_warn_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("/setwarnlimit number")
        return
    db.set_group_setting(update.effective_chat.id, 'max_warnings', int(context.args[0]))
    text = create_ui_box("WARN LIMIT", f"✅ max warnings {context.args[0]} set", "⚠️")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

# ============ WELCOME COMMANDS ============

@admin_only
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/welcome hello {first_name}")
        return
    db.set_welcome_message(update.effective_chat.id, " ".join(context.args))
    text = create_ui_box("WELCOME", "✅ welcome message set ho gaya", "👋")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def set_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/goodbye message")
        return
    db.set_goodbye_message(update.effective_chat.id, " ".join(context.args))
    text = create_ui_box("GOODBYE", "✅ goodbye message set ho gaya", "👋")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

@admin_only
async def set_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("/setrules rules text")
        return
    db.set_rules(update.effective_chat.id, " ".join(context.args))
    text = create_ui_box("RULES", "✅ rules set ho gaye", "📜")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules = db.get_rules(update.effective_chat.id)
    if not rules:
        text = create_ui_box("RULES", "koi rules nahi hai", "📜")
    else:
        text = create_ui_box("GROUP RULES", rules, "📜")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 120)

# ============ GAMES COMMANDS ============

async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = games.get_truth()
    text = create_ui_box("TRUTH", question, "🎮")
    keyboard = create_inline_keyboard_with_close()
    msg = await update.message.reply_text(text, reply_markup=keyboard)
    await auto_delete_message(update, context, 120)

async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dare = games.get_dare()
    text = create_ui_box("DARE", dare, "🎮")
    keyboard = create_inline_keyboard_with_close()
    msg = await update.message.reply_text(text, reply_markup=keyboard)
    await auto_delete_message(update, context, 120)

async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = games.roll_dice()
    text = create_ui_box("ROLL", f"🎲 You rolled: {result}", "🎲")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = games.flip_coin()
    text = create_ui_box("COIN FLIP", f"🪙 Result: {result}", "🪙")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

async def rps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        text = create_ui_box("ROCK PAPER SCISSORS", "/rps rock ya /rps paper ya /rps scissors", "✊")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 30)
        return
    user_choice = context.args[0].lower()
    if user_choice not in ['rock', 'paper', 'scissors']:
        await update.message.reply_text("rock, paper, ya scissors choose kar")
        return
    result, bot_choice = games.play_rps(user_choice)
    text = create_ui_box("RPS", f"You: {user_choice}\nHinata: {bot_choice}\n\n{result}", "✊")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 30)

# ============ INFO COMMANDS ============

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
        elif context.args:
            member = await update.effective_chat.get_member(context.args[0])
            user = member.user
        else:
            user = update.effective_user
        member = await update.effective_chat.get_member(user.id)
        warnings = db.get_warnings(update.effective_chat.id, user.id)
        content = f"name: {user.first_name}\nid: {user.id}"
        if user.username:
            content += f"\nusername: @{user.username}"
        content += f"\nstatus: {member.status}\nwarnings: {warnings}"
        text = create_ui_box("USER INFO", content, "👤")
        msg = await update.message.reply_text(text)
        await auto_delete_message(update, context, 60)
    except Exception as e:
        await update.message.reply_text(f"❌ error: {str(e)}")

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = db.get_group_settings(update.effective_chat.id)
    content = (
        f"antispam: {'on' if settings.get('antispam_enabled') else 'off'}\n"
        f"flood limit: {settings.get('flood_limit', 5)}\n"
        f"antilink: {'on' if settings.get('antilink_enabled') else 'off'}\n"
        f"max warnings: {settings.get('max_warnings', 3)}"
    )
    text = create_ui_box("GROUP SETTINGS", content, "⚙️")
    msg = await update.message.reply_text(text)
    await auto_delete_message(update, context, 60)

# ============ MESSAGE HANDLERS ============

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            db.init_group(chat.id)
            text = create_ui_box(
                "HINATA BOT",
                "mujhe admin banao:\n- delete messages\n- restrict members\n- pin messages\n- ban users\n\n/help se commands dekh lo",
                "🌸"
            )
            await update.message.reply_text(text)
            continue
        if db.is_blocked(chat.id, member.id):
            await chat.ban_member(member.id)
            text = create_ui_box("BLOCKED", f"🚫 blocked user {member.first_name} ko kick kar diya", "🚫")
            await update.message.reply_text(text)
            continue
        welcome_msg = db.get_welcome_message(chat.id)
        if welcome_msg:
            try:
                welcome_text = welcome_msg.format(
                    first_name=member.first_name or "",
                    last_name=member.last_name or "",
                    username=f"@{member.username}" if member.username else member.first_name,
                    mention=member.mention_html(),
                    group_name=chat.title
                )
                await update.message.reply_text(welcome_text)
            except:
                pass

async def handle_left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    member = update.message.left_chat_member
    if member.id == context.bot.id:
        db.remove_group(chat.id)
        return
    goodbye_msg = db.get_goodbye_message(chat.id)
    if goodbye_msg:
        try:
            goodbye_text = goodbye_msg.format(
                first_name=member.first_name or "",
                last_name=member.last_name or "",
                username=f"@{member.username}" if member.username else member.first_name,
                group_name=chat.title
            )
            await update.message.reply_text(goodbye_text)
        except:
            pass

async def hinata_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    if not message.text:
        return
    is_for_hinata = False
    if message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id:
        is_for_hinata = True
    if any(trigger in message.text.lower() for trigger in config.CHATBOT_TRIGGERS):
        is_for_hinata = True
    if chat.type == ChatType.PRIVATE:
        is_for_hinata = True
    if not is_for_hinata:
        return
    clean_text = re.sub(r'\bhinata\b|\bhana\b|\bbot\b', '', message.text, flags=re.IGNORECASE).strip()
    
    # Pass user_id for memory system
    response = await chatbot.generate_response(clean_text, user_id=user.id, user_name=user.first_name)
    
    # Save user profile
    try:
        db.save_user_profile(user.id, user.first_name, user.username or "", "hinglish")
    except:
        pass
    
    try:
        await message.reply_text(response)
        # Log conversation
        db.increment_message_count(chat.id, user.id)
    except:
        pass

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming stickers - collect and respond"""
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    
    # Collect the sticker (auto-learning)
    if message and message.sticker and user:
        try:
            sticker = message.sticker
            # Save to database for later use
            sticker_mgr.save_sticker(
                file_id=sticker.file_id,
                file_unique_id=sticker.file_unique_id,
                sticker_type="animated" if sticker.is_animated else "regular",
                set_name=sticker.set_name or "collected",
                user_id=user.id,
                chat_id=chat.id
            )
        except Exception as e:
            pass
    
    # Respond back with GIF or sticker (40% chance)
    if random.random() < 0.4:
        try:
            # Get response media (GIF or sticker)
            response_media = sticker_mgr.respond_to_sticker()
            
            # Check if it's a GIF URL or sticker ID
            if response_media.startswith('http'):
                # It's a GIF URL - send as animation
                await context.bot.send_animation(chat.id, response_media)
            else:
                # It's a sticker ID - send as sticker
                await context.bot.send_sticker(chat.id, response_media)
        except Exception as e:
            pass

async def check_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    if not chat or not user or not message:
        return
    if await is_admin(chat, user.id):
        return
        
    settings = db.get_group_settings(chat.id)
    text = message.text or message.caption or ""
    
    # Check antilink - enhanced security with multiple patterns
    if settings.get('antilink_enabled', False) and text:
        # Comprehensive link detection patterns
        link_patterns = [
            r'https?://[^\s]+',  # HTTP/HTTPS links
            r'(?<![\@\.])[t]\.me/[^\s]+',  # Telegram links (fixed)
            r'telegram\.me/[^\s]+',  # Telegram alternative
            r'www\.[^\s]+',  # WWW links
            r'bit\.ly/[^\s]+',  # Bitly links
            r'ow\.ly/[^\s]+',  # Owly links
            r'tinyurl\.com/[^\s]+',  # TinyURL links
            r'youtu\.be/[^\s]+',  # YouTube short links
            r'facebookhttps?://[^\s|]+',  # Facebook links
            r'(?<![\w/.-])(?:(?:\w+\.)+(?:com|org|net|co|in|io|gov|edu|uk))\b',  # Domain detection
        ]
        
        has_link = any(re.search(p, text, re.IGNORECASE) for p in link_patterns)
        
        # Check for mentions which might be promotion
        mention_count = len(re.findall(r'@[\w]+', text))
        has_spam_mentions = mention_count > 3
        
        if (has_link or has_spam_mentions) and not await is_owner(user.id):
            try:
                await message.delete()
                reason = "link detected" if has_link else f"spam mentions ({mention_count})"
                warning_msg = await update.message.reply_text(
                    create_ui_box("ANTILINK ALERT", f"🚫 {user.first_name}\n{reason}\n\nadmin link bhej sakta", "🔗")
                )
                
                # Log action
                db.log_action(chat.id, "ANTILINK", user.id, user.first_name or "Unknown", 
                            context.bot.id, "HINATA", reason)
                
                context.job_queue.run_once(
                    delete_message_after,
                    1,
                    chat_id=chat.id,
                    data=warning_msg.message_id
                )
            except Exception as e:
                pass
            return
    
    # Check blocklist
    if db.is_blocked(chat.id, user.id):
        try:
            await message.delete()
        except:
            pass
        return
    
    # Check filter words
    filters_list = db.get_filter_words(chat.id)
    if filters_list and text:
        text_lower = text.lower()
        for word in filters_list:
            if word in text_lower:
                try:
                    await message.delete()
                    warning_msg = await update.message.reply_text(
                        create_ui_box("FILTER", f"🚫 filtered word {user.first_name} ka message delete kar diya", "🚫")
                    )
                    context.job_queue.run_once(
                        delete_message_after,
                        1,
                        chat_id=chat.id,
                        data=warning_msg.message_id
                    )
                except:
                    pass
                return
    
    # Check antispam
    if settings.get('antispam_enabled', False) and text:
        link_patterns = [r'https?://[^\s]+', r't\.me/[^\s]+', r'telegram\.me/[^\s]+']
        link_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in link_patterns)
        if link_count >= 2:
            try:
                await message.delete()
                warning_msg = await update.message.reply_text(
                    create_ui_box("ANTISPAM", f"🚫 spam detect hua {user.first_name} link mat bhejo", "🛡️")
                )
                context.job_queue.run_once(
                    delete_message_after,
                    1,
                    chat_id=chat.id,
                    data=warning_msg.message_id
                )
            except:
                pass
            return
    
    # Check flood
    flood_limit = settings.get('flood_limit', 5)
    if flood_limit > 0:
        key = f"flood_{chat.id}_{user.id}"
        if key not in context.chat_data:
            context.chat_data[key] = []
        now = datetime.now()
        context.chat_data[key].append(now)
        context.chat_data[key] = [t for t in context.chat_data[key] if (now - t).total_seconds() < 10]
        if len(context.chat_data[key]) > flood_limit:
            try:
                await message.delete()
                until_date = datetime.now() + timedelta(minutes=5)
                await chat.restrict_member(user.id, ChatPermissions(can_send_messages=False), until_date=until_date)
                warning_msg = await update.message.reply_text(
                    create_ui_box("FLOOD", f"🌊 flood detect hua {user.first_name} 5 min mute", "🌊")
                )
                context.job_queue.run_once(
                    delete_message_after,
                    1,
                    chat_id=chat.id,
                    data=warning_msg.message_id
                )
                del context.chat_data[key]
            except:
                pass
            return

# ============ CALLBACK HANDLER ============

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'close_msg':
        try:
            await query.message.delete()
        except:
            pass
        return
    
    # Handle lock commands
    if query.data.startswith('lock_'):
        lock_type = query.data.replace('lock_', '')
        # Create a fake update to reuse the _apply_lock function
        await _apply_lock(lock_type, query, context)
        try:
            await query.message.delete()
        except:
            pass
        return
    
    if query.data == 'help':
        text = create_ui_box(
            "HINATA COMMANDS",
            "👮 Admin:\n/ban /unban /kick /mute /unmute\n/tmute /tban /pin /unpin\n\n"
            "🛡️ Security:\n/antispam /flood /lock /unlock\n/antilink\n\n"
            "🚫 Filters:\n/filter /unfilter /filters\n/block /unblock /blocklist\n\n"
            "⚠️ Warnings:\n/warn /unwarn /warnings /setwarnlimit\n\n"
            "👋 Welcome:\n/welcome /goodbye /setrules /rules\n\n"
            "🎮 Games:\n/truth /dare /roll /coin /rps\n\n"
            "🤖 Chatbot:\n'hinata' bol ya reply kar",
            "📚"
        )
        keyboard = create_inline_keyboard_with_close()
        await query.edit_message_text(text, reply_markup=keyboard)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception: {context.error}")

# ============ MAIN ============

def main():
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("set BOT_TOKEN environment variable!")
        print("export BOT_TOKEN=your_token_here")
        return
    print("""
    ==============================
      HINATA BOT - Created By Axl
      Version 2.0 - Zero Errors
      Starting...
    ==============================
    """)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_error_handler(error_handler)
    
    # Basic commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("owner", owner_command))
    application.add_handler(CommandHandler("home", home_command))
    
    # Admin commands
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("kick", kick_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("tmute", tmute_command))
    application.add_handler(CommandHandler("tban", tban_command))
    application.add_handler(CommandHandler("pin", pin_command))
    application.add_handler(CommandHandler("unpin", unpin_command))
    
    # Security commands
    application.add_handler(CommandHandler("antispam", antispam_command))
    application.add_handler(CommandHandler("flood", flood_command))
    application.add_handler(CommandHandler("antilink", antilink_command))
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("unlock", unlock_command))
    
    # Filter commands
    application.add_handler(CommandHandler("filter", add_filter))
    application.add_handler(CommandHandler("unfilter", remove_filter))
    application.add_handler(CommandHandler("filters", list_filters))
    application.add_handler(CommandHandler("block", block_user))
    application.add_handler(CommandHandler("unblock", unblock_user))
    application.add_handler(CommandHandler("blocklist", blocklist_command))
    
    # Warning commands
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("unwarn", unwarn_command))
    application.add_handler(CommandHandler("warnings", check_warnings))
    application.add_handler(CommandHandler("setwarnlimit", set_warn_limit))
    
    # Welcome commands
    application.add_handler(CommandHandler("welcome", set_welcome))
    application.add_handler(CommandHandler("goodbye", set_goodbye))
    application.add_handler(CommandHandler("setrules", set_rules))
    application.add_handler(CommandHandler("rules", show_rules))
    
    # Games commands
    application.add_handler(CommandHandler("truth", truth_command))
    application.add_handler(CommandHandler("dare", dare_command))
    application.add_handler(CommandHandler("roll", roll_command))
    application.add_handler(CommandHandler("coin", coin_command))
    application.add_handler(CommandHandler("rps", rps_command))
    
    # Info commands
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_left_member))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hinata_chatbot), group=1)
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check_filters), group=2)
    
    logger.info("bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
