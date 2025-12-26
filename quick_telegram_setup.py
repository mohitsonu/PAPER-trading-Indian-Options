#!/usr/bin/env python3
"""Quick Telegram Setup"""
import json

print("🔧 TELEGRAM QUICK SETUP")
print("=" * 50)
print("\nIf you already have bot token and chat ID, enter them now.")
print("Otherwise, follow these steps:")
print("1. Message @BotFather on Telegram")
print("2. Send: /newbot")
print("3. Copy your bot token")
print("4. Message your bot once")
print("5. Visit: https://api.telegram.org/bot<TOKEN>/getUpdates")
print("6. Find your chat ID\n")

bot_token = input("🤖 Bot Token: ").strip()
chat_id = input("💬 Chat ID: ").strip()

if bot_token and chat_id:
    config = {
        "bot_token": bot_token,
        "chat_id": chat_id
    }
    
    with open('telegram_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved!")
    print("Now run: python send_daily_summary.py")
else:
    print("\n❌ Both token and chat ID are required!")
