"""
🧪 Test Telegram Connection
Run this to verify your Telegram setup
"""

from telegram_notifier import TelegramNotifier
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED

def test_telegram():
    """Test Telegram notifications"""
    
    print("🧪 TESTING TELEGRAM CONNECTION")
    print("=" * 50)
    
    if not TELEGRAM_ENABLED:
        print("❌ Telegram is disabled in config.py")
        print("📝 Please configure and set TELEGRAM_ENABLED = True")
        return
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Bot token not configured!")
        print("📝 Please set TELEGRAM_BOT_TOKEN in config.py")
        return
    
    if TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Chat ID not configured!")
        print("📝 Please set TELEGRAM_CHAT_ID in config.py")
        return
    
    print(f"🤖 Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"💬 Chat ID: {TELEGRAM_CHAT_ID}")
    print()
    
    # Initialize notifier
    notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Test connection
    print("1️⃣ Testing connection...")
    if not notifier.test_connection():
        return
    
    print()
    print("2️⃣ Sending test message...")
    result = notifier.send_message("✅ <b>Test Successful!</b>\n\nYour Telegram bot is working correctly! 🎉")
    
    if result and result.get('ok'):
        print("✅ Test message sent successfully!")
        print("📱 Check your Telegram to see the message")
    else:
        print("❌ Failed to send test message")
        print(f"Error: {result}")
    
    print()
    print("3️⃣ Testing entry signal...")
    test_entry = {
        'symbol': 'NIFTY11NOV25C25400',
        'entry_price': 110.50,
        'quantity': 300,
        'accuracy_score': 100,
        'strategy': 'TREND_BULL_CE',
        'reason': 'Good OI, Strong bullish trend'
    }
    notifier.send_entry_signal(test_entry)
    print("✅ Entry signal sent!")
    
    print()
    print("4️⃣ Testing exit signal...")
    test_exit = {
        'symbol': 'NIFTY11NOV25C25400',
        'entry_price': 110.50,
        'exit_price': 125.30,
        'quantity': 300,
        'net_pnl': 4400,
        'exit_reason': 'TARGET_HIT',
        'holding_time_minutes': 15
    }
    notifier.send_exit_signal(test_exit)
    print("✅ Exit signal sent!")
    
    print()
    print("5️⃣ Testing daily summary...")
    test_summary = {
        'starting_capital': 100000,
        'ending_capital': 146310,
        'net_pnl': 46310,
        'net_pnl_pct': 46.31,
        'total_trades': 16,
        'win_rate': 75.0,
        'wins': 12,
        'losses': 4
    }
    notifier.send_daily_summary(test_summary)
    print("✅ Daily summary sent!")
    
    print()
    print("=" * 50)
    print("🎉 ALL TESTS COMPLETED!")
    print("📱 Check your Telegram for all test messages")
    print("✅ You're ready to receive live trading signals!")

if __name__ == "__main__":
    test_telegram()
