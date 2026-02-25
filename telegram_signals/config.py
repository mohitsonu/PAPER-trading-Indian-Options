"""
⚙️ Telegram Configuration
Setup your bot token and chat ID here
"""

import os

# Get these from @BotFather on Telegram
# Can be overridden by environment variables (for GitHub Actions)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "8468449326:AAHCEko5T1squW5VFJjL4SdS0nr8h1JB-sU")

# Get this from your channel/group
# Can be overridden by environment variables (for GitHub Actions)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "@optionsalgotesting")

# Enable/Disable Telegram notifications
TELEGRAM_ENABLED = True  # Set to True after configuring

"""
📝 HOW TO SETUP:

1. CREATE BOT:
   - Open Telegram and search for @BotFather
   - Send /newbot command
   - Follow instructions to create your bot
   - Copy the bot token (looks like: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)
   - Paste it in TELEGRAM_BOT_TOKEN above

2. GET CHAT ID:
   
   Option A - For Personal Chat:
   - Search for @userinfobot on Telegram
   - Start chat and it will show your chat ID
   - Use that number as TELEGRAM_CHAT_ID
   
   Option B - For Channel:
   - Create a public channel
   - Add your bot as admin
   - Chat ID will be @your_channel_name
   
   Option C - For Group:
   - Create a group and add your bot
   - Add @userinfobot to the group
   - It will show the group chat ID (starts with -)
   - Remove @userinfobot after getting ID

3. ENABLE:
   - Set TELEGRAM_ENABLED = True
   - Run: python telegram_signals/test_telegram.py
   - You should receive a test message!

4. START TRADING:
   - Your bot will now send signals automatically
"""
