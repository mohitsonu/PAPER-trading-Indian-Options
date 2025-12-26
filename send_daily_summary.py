#!/usr/bin/env python3
"""Send today's trading summary to Telegram"""
from telegram_bot import TelegramBot
from datetime import datetime
import sys
import os

def main():
    print("📱 SENDING DAILY SUMMARY TO TELEGRAM")
    print("=" * 50)
    
    bot = TelegramBot()
    if not bot.enabled:
        print("❌ Telegram not configured!")
        print("💡 Run setup: python setup_telegram.py")
        return
    
    # Get date
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y%m%d")
    
    csv_file = f"high_accuracy_trades_{date_str}.csv"
    print(f"📅 Date: {date_str}")
    print(f"📁 Looking for: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"⚠️ File not found: {csv_file}")
    
    print("📤 Sending summary...")
    success = bot.send_daily_summary(csv_file, capital_start=100000)
    
    if success:
        print("✅ Daily summary sent successfully!")
    else:
        print("❌ Failed to send summary")

if __name__ == "__main__":
    main()
