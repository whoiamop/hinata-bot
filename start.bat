@echo off
chcp 65001 >nul
title Hinata Bot - Advanced Group Manager
color 0D
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🌸  ʜɪɴᴀᴛᴀ - ᴀᴅᴠᴀɴᴄᴇᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ  🌸         ║
echo ║                                                                ║
echo ║     Version: 3.0 Ultimate Edition                             ║
echo ║     Owner: tg://user?id=8430369957                            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

:: Check Python
echo [🔍] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [❌] Python is not installed!
    echo [📥] Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [✅] Python found

:: Create virtual environment if not exists
if not exist "venv" (
    echo [📦] Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo [🔄] Activating virtual environment...
call venv\Scripts\activate

:: Upgrade pip
echo [⬆️] Upgrading pip...
pip install -q --upgrade pip

:: Install requirements
echo [📥] Installing dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo [❌] Failed to install dependencies
    pause
    exit /b 1
)

echo [✅] Dependencies installed

:: Check bot token
if "%BOT_TOKEN%"=="" (
    echo.
    echo [⚠️]  WARNING: BOT_TOKEN not set!
    echo      Set it with: set BOT_TOKEN=your_token_here
    echo.
)

:: Create directories
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

:: Run bot with auto-restart
:loop
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  🚀 Starting Hinata Bot...                                    ║
echo ║  Press Ctrl+C to stop                                         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

python bot.py

if %errorlevel% == 0 (
    echo [👋] Bot stopped by user
    goto end
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║  ⚠️  Bot crashed! Restarting in 5 seconds...                  ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    timeout /t 5 /nobreak >nul
    goto loop
)

:end
echo.
echo [👋] Goodbye!
pause
