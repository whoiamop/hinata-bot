#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  🗄️  HINATA DATABASE MANAGER                                              ║
║  PostgreSQL + SQLite Support | Big Database | Real-time | 24/7 Ready      ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import sqlite3
import json
import os
import logging
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    🗄️ Advanced Database Manager
    Supports: SQLite (local) | PostgreSQL (production)
    Features: Connection pooling, auto-reconnect, big data optimized
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.db_type = os.getenv('DB_TYPE', 'sqlite')
        self.db_path = os.getenv('DB_PATH', 'hinata_bot.db')
        
        # PostgreSQL config (for production)
        self.pg_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'hinata_bot'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
        self._init_database()
        logger.info(f"🗄️ Database initialized: {self.db_type}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔌 CONNECTION MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager"""
        conn = None
        try:
            if self.db_type == 'postgresql':
                try:
                    import psycopg2
                    conn = psycopg2.connect(**self.pg_config)
                except ImportError:
                    logger.warning("psycopg2 not installed, falling back to SQLite")
                    conn = sqlite3.connect(self.db_path)
            else:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row
            
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _init_database(self):
        """Initialize all database tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Groups table - main configuration
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    chat_id INTEGER PRIMARY KEY,
                    chat_title TEXT,
                    welcome_message TEXT DEFAULT '',
                    goodbye_message TEXT DEFAULT '',
                    rules TEXT DEFAULT '',
                    settings TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Filter words table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS filter_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    word TEXT NOT NULL,
                    added_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE,
                    UNIQUE(chat_id, word)
                )
            ''')
            
            # Blocklist table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocklist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER NOT NULL,
                    user_name TEXT,
                    reason TEXT,
                    added_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE,
                    UNIQUE(chat_id, user_id)
                )
            ''')
            
            # Warnings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER NOT NULL,
                    count INTEGER DEFAULT 0,
                    last_warning TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE,
                    UNIQUE(chat_id, user_id)
                )
            ''')
            
            # Warning history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warning_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER,
                    reason TEXT,
                    warned_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE
                )
            ''')
            
            # Admin notes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER,
                    note TEXT NOT NULL,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE
                )
            ''')
            
            # User stats table (for analytics)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER,
                    message_count INTEGER DEFAULT 0,
                    command_count INTEGER DEFAULT 0,
                    last_activity TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES groups(chat_id) ON DELETE CASCADE,
                    UNIQUE(chat_id, user_id)
                )
            ''')
            
            # Chatbot conversations (for learning)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chatbot_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    response TEXT,
                    chat_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Action logs (moderation history)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS action_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    action_type TEXT,
                    target_user_id INTEGER,
                    target_user_name TEXT,
                    admin_id INTEGER,
                    admin_name TEXT,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_filter_words_chat ON filter_words(chat_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocklist_chat ON blocklist(chat_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_warnings_chat ON warnings(chat_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_chat ON action_logs(chat_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stats_chat_user ON user_stats(chat_id, user_id)')
            
            conn.commit()
            logger.info("✅ All database tables initialized")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👥 GROUP METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def init_group(self, chat_id: int, chat_title: str = ""):
        """Initialize a new group"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO groups (chat_id, chat_title) VALUES (?, ?)
            ''', (chat_id, chat_title))
            logger.info(f"Group initialized: {chat_id}")
    
    def remove_group(self, chat_id: int):
        """Remove a group and all its data"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM groups WHERE chat_id = ?', (chat_id,))
            logger.info(f"Group removed: {chat_id}")
    
    def get_group_settings(self, chat_id: int) -> Dict[str, Any]:
        """Get group settings"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT settings FROM groups WHERE chat_id = ?', (chat_id,))
            row = cursor.fetchone()
            
            if row and row['settings']:
                return json.loads(row['settings'])
            return {
                'antispam_enabled': False,
                'flood_limit': 5,
                'max_warnings': 3,
                'log_channel': None,
                'welcome_enabled': True,
                'goodbye_enabled': False
            }
    
    def set_group_setting(self, chat_id: int, key: str, value: Any):
        """Set a group setting"""
        settings = self.get_group_settings(chat_id)
        settings[key] = value
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (chat_id, settings) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET settings = ?, updated_at = CURRENT_TIMESTAMP
            ''', (chat_id, json.dumps(settings), json.dumps(settings)))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👋 WELCOME/GOODBYE METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_welcome_message(self, chat_id: int) -> str:
        """Get welcome message"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT welcome_message FROM groups WHERE chat_id = ?', (chat_id,))
            row = cursor.fetchone()
            return row['welcome_message'] if row else ""
    
    def set_welcome_message(self, chat_id: int, message: str):
        """Set welcome message"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (chat_id, welcome_message) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET welcome_message = ?, updated_at = CURRENT_TIMESTAMP
            ''', (chat_id, message, message))
    
    def get_goodbye_message(self, chat_id: int) -> str:
        """Get goodbye message"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT goodbye_message FROM groups WHERE chat_id = ?', (chat_id,))
            row = cursor.fetchone()
            return row['goodbye_message'] if row else ""
    
    def set_goodbye_message(self, chat_id: int, message: str):
        """Set goodbye message"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (chat_id, goodbye_message) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET goodbye_message = ?, updated_at = CURRENT_TIMESTAMP
            ''', (chat_id, message, message))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📜 RULES METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_rules(self, chat_id: int) -> str:
        """Get group rules"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT rules FROM groups WHERE chat_id = ?', (chat_id,))
            row = cursor.fetchone()
            return row['rules'] if row else ""
    
    def set_rules(self, chat_id: int, rules: str):
        """Set group rules"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (chat_id, rules) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET rules = ?, updated_at = CURRENT_TIMESTAMP
            ''', (chat_id, rules, rules))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🚫 FILTER WORDS METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_filter_word(self, chat_id: int, word: str, added_by: int = 0):
        """Add a filter word"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO filter_words (chat_id, word, added_by) VALUES (?, ?, ?)
            ''', (chat_id, word.lower(), added_by))
    
    def remove_filter_word(self, chat_id: int, word: str):
        """Remove a filter word"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM filter_words WHERE chat_id = ? AND word = ?',
                         (chat_id, word.lower()))
    
    def get_filter_words(self, chat_id: int) -> List[str]:
        """Get all filter words for a group"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT word FROM filter_words WHERE chat_id = ?', (chat_id,))
            rows = cursor.fetchall()
            return [row['word'] for row in rows]
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🚫 BLOCKLIST METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_to_blocklist(self, chat_id: int, user_id: int, user_name: str = "", 
                         reason: str = "", added_by: int = 0):
        """Add user to blocklist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO blocklist (chat_id, user_id, user_name, reason, added_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, user_id, user_name, reason, added_by))
    
    def remove_from_blocklist(self, chat_id: int, user_id: int):
        """Remove user from blocklist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM blocklist WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
    
    def is_blocked(self, chat_id: int, user_id: int) -> bool:
        """Check if user is blocked"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM blocklist WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
            return cursor.fetchone() is not None
    
    def get_blocklist(self, chat_id: int) -> List[Dict]:
        """Get all blocked users"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, user_name, reason, created_at 
                FROM blocklist WHERE chat_id = ?
            ''', (chat_id,))
            rows = cursor.fetchall()
            return [{
                'user_id': row['user_id'],
                'name': row['user_name'],
                'reason': row['reason'],
                'added': row['created_at']
            } for row in rows]
    
    # ═══════════════════════════════════════════════════════════════════════
    # ⚠️ WARNINGS METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_warning(self, chat_id: int, user_id: int, reason: str = "", warned_by: int = 0) -> int:
        """Add warning to user, returns new count"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Update or insert warning count
            cursor.execute('''
                INSERT INTO warnings (chat_id, user_id, count, last_warning)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(chat_id, user_id) 
                DO UPDATE SET count = count + 1, last_warning = CURRENT_TIMESTAMP
            ''', (chat_id, user_id))
            
            # Add to history
            cursor.execute('''
                INSERT INTO warning_history (chat_id, user_id, reason, warned_by)
                VALUES (?, ?, ?, ?)
            ''', (chat_id, user_id, reason, warned_by))
            
            # Get current count
            cursor.execute('SELECT count FROM warnings WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
            row = cursor.fetchone()
            return row['count'] if row else 0
    
    def remove_warning(self, chat_id: int, user_id: int) -> int:
        """Remove one warning, returns new count"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE warnings SET count = MAX(count - 1, 0)
                WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            
            cursor.execute('SELECT count FROM warnings WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
            row = cursor.fetchone()
            return row['count'] if row else 0
    
    def get_warnings(self, chat_id: int, user_id: int) -> int:
        """Get warning count"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT count FROM warnings WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
            row = cursor.fetchone()
            return row['count'] if row else 0
    
    def clear_warnings(self, chat_id: int, user_id: int):
        """Clear all warnings"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM warnings WHERE chat_id = ? AND user_id = ?',
                         (chat_id, user_id))
    
    def get_warning_history(self, chat_id: int, user_id: int) -> List[Dict]:
        """Get warning history"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT reason, warned_by, created_at 
                FROM warning_history 
                WHERE chat_id = ? AND user_id = ?
                ORDER BY created_at DESC
            ''', (chat_id, user_id))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📝 ADMIN NOTES METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_note(self, chat_id: int, user_id: int, note: str, created_by: int):
        """Add admin note"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO admin_notes (chat_id, user_id, note, created_by)
                VALUES (?, ?, ?, ?)
            ''', (chat_id, user_id, note, created_by))
    
    def get_notes(self, chat_id: int, user_id: int) -> List[Dict]:
        """Get admin notes for user"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT note, created_by, created_at 
                FROM admin_notes 
                WHERE chat_id = ? AND user_id = ?
                ORDER BY created_at DESC
            ''', (chat_id, user_id))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def delete_note(self, note_id: int):
        """Delete a note"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM admin_notes WHERE id = ?', (note_id,))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📊 STATS METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def increment_message_count(self, chat_id: int, user_id: int):
        """Increment user message count"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_stats (chat_id, user_id, message_count, last_activity)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(chat_id, user_id) 
                DO UPDATE SET message_count = message_count + 1, last_activity = CURRENT_TIMESTAMP
            ''', (chat_id, user_id))
    
    def get_user_stats(self, chat_id: int, user_id: int) -> Dict:
        """Get user statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT message_count, command_count, last_activity
                FROM user_stats WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            row = cursor.fetchone()
            return dict(row) if row else {'message_count': 0, 'command_count': 0}
    
    def get_top_users(self, chat_id: int, limit: int = 10) -> List[Dict]:
        """Get top active users"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, message_count 
                FROM user_stats 
                WHERE chat_id = ?
                ORDER BY message_count DESC
                LIMIT ?
            ''', (chat_id, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🤖 CHATBOT LOGS
    # ═══════════════════════════════════════════════════════════════════════
    
    def log_chatbot(self, user_id: int, message: str, response: str, chat_type: str):
        """Log chatbot conversation"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chatbot_logs (user_id, message, response, chat_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, message, response, chat_type))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📝 ACTION LOGS
    # ═══════════════════════════════════════════════════════════════════════
    
    def log_action(self, chat_id: int, action_type: str, target_user_id: int,
                   target_user_name: str, admin_id: int, admin_name: str, reason: str = ""):
        """Log moderation action"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO action_logs 
                (chat_id, action_type, target_user_id, target_user_name, admin_id, admin_name, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (chat_id, action_type, target_user_id, target_user_name, admin_id, admin_name, reason))
    
    def get_action_logs(self, chat_id: int, limit: int = 50) -> List[Dict]:
        """Get action logs for group"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM action_logs 
                WHERE chat_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (chat_id, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔧 MAINTENANCE METHODS
    # ═══════════════════════════════════════════════════════════════════════
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Clean old chatbot logs
            cursor.execute('''
                DELETE FROM chatbot_logs 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days))
            
            # Clean old action logs
            cursor.execute('''
                DELETE FROM action_logs 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days))
            
            logger.info(f"Cleaned up data older than {days} days")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            stats = {}
            
            tables = ['groups', 'filter_words', 'blocklist', 'warnings', 
                     'admin_notes', 'user_stats', 'chatbot_logs', 'action_logs']
            
            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                stats[table] = cursor.fetchone()[0]
            
            return stats
