"""
📤 Send Test Messages - Replay Today's Trades
This will send all of today's trades to your Telegram as a demo
"""

from telegram_notifier import TelegramNotifier
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
import time

def send_todays_trades():
    """Send today's actual trades as test messages"""
    
    print("📤 SENDING TODAY'S TRADES TO TELEGRAM")
    print("=" * 50)
    
    if not TELEGRAM_ENABLED:
        print("❌ Telegram is disabled in config.py")
        print("📝 Please configure and set TELEGRAM_ENABLED = True")
        return
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Please configure bot token and chat ID in config.py")
        return
    
    # Initialize notifier
    notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Test connection
    if not notifier.test_connection():
        print("❌ Connection failed!")
        return
    
    print("✅ Connected! Sending today's trades...\n")
    
    # Session Start
    print("1️⃣ Sending session start...")
    notifier.send_session_start(100000)
    time.sleep(1)
    
    # Trade 1: Entry + Exit
    print("2️⃣ Trade 1: NIFTY 25400 CE Entry...")
    trade1_entry = {
        'symbol': 'NIFTY11NOV25C25400',
        'strike': 25400,
        'option_type': 'CE',
        'entry_price': 110.30,
        'quantity': 300,
        'strategy': 'CONTRARIAN',
        'reason': 'Good OI: 14,030,400, Good premium: ₹110.30'
    }
    notifier.send_entry_signal(trade1_entry)
    time.sleep(2)
    
    print("   Exit...")
    trade1_exit = {
        'symbol': 'NIFTY11NOV25C25400',
        'strike': 25400,
        'option_type': 'CE',
        'entry_price': 110.30,
        'exit_price': 129.40,
        'quantity': 300,
        'net_pnl': 5690,
        'exit_reason': 'IMMEDIATE_PROFIT_BOOK',
        'holding_time_minutes': 8
    }
    notifier.send_exit_signal(trade1_exit)
    time.sleep(2)
    
    # Trade 2: Entry + Exit
    print("3️⃣ Trade 2: NIFTY 25400 CE Entry...")
    trade2_entry = {
        'symbol': 'NIFTY11NOV25C25400',
        'strike': 25400,
        'option_type': 'CE',
        'entry_price': 117.30,
        'quantity': 300,
        'strategy': 'CONTRARIAN',
        'reason': 'Good OI: 12,660,825, Good premium: ₹117.30'
    }
    notifier.send_entry_signal(trade2_entry)
    time.sleep(2)
    
    print("   Exit...")
    trade2_exit = {
        'symbol': 'NIFTY11NOV25C25400',
        'strike': 25400,
        'option_type': 'CE',
        'entry_price': 117.30,
        'exit_price': 148.80,
        'quantity': 300,
        'net_pnl': 9410,
        'exit_reason': 'IMMEDIATE_PROFIT_BOOK',
        'holding_time_minutes': 5
    }
    notifier.send_exit_signal(trade2_exit)
    time.sleep(2)
    
    # Trade 3: Entry + Exit (Big Winner)
    print("4️⃣ Trade 3: NIFTY 25450 CE Entry...")
    trade3_entry = {
        'symbol': 'NIFTY11NOV25C25450',
        'strike': 25450,
        'option_type': 'CE',
        'entry_price': 116.10,
        'quantity': 300,
        'strategy': 'TREND_BULL_CE',
        'reason': 'Good OI: 5,464,200, Good premium: ₹116.10'
    }
    notifier.send_entry_signal(trade3_entry)
    time.sleep(2)
    
    print("   Exit...")
    trade3_exit = {
        'symbol': 'NIFTY11NOV25C25450',
        'strike': 25450,
        'option_type': 'CE',
        'entry_price': 116.10,
        'exit_price': 160.00,
        'quantity': 300,
        'net_pnl': 13130,
        'exit_reason': 'TIME_EXIT',
        'holding_time_minutes': 120
    }
    notifier.send_exit_signal(trade3_exit)
    time.sleep(2)
    
    # Trade 4: Entry + Exit (PE Trade)
    print("5️⃣ Trade 4: NIFTY 25350 PE Entry...")
    trade4_entry = {
        'symbol': 'NIFTY11NOV25P25350',
        'strike': 25350,
        'option_type': 'PE',
        'entry_price': 25.40,
        'quantity': 300,
        'strategy': 'CONTRARIAN',
        'reason': 'Good OI: 11,687,400, Good premium: ₹25.40'
    }
    notifier.send_entry_signal(trade4_entry)
    time.sleep(2)
    
    print("   Exit...")
    trade4_exit = {
        'symbol': 'NIFTY11NOV25P25350',
        'strike': 25350,
        'option_type': 'PE',
        'entry_price': 25.40,
        'exit_price': 39.60,
        'quantity': 300,
        'net_pnl': 4220,
        'exit_reason': 'TARGET_HIT',
        'holding_time_minutes': 25
    }
    notifier.send_exit_signal(trade4_exit)
    time.sleep(2)
    
    # Trade 5: Entry + Exit (Loss Example)
    print("6️⃣ Trade 5: NIFTY 25250 PE Entry...")
    trade5_entry = {
        'symbol': 'NIFTY11NOV25P25250',
        'strike': 25250,
        'option_type': 'PE',
        'entry_price': 23.00,
        'quantity': 300,
        'strategy': 'TREND_BEAR_PE',
        'reason': 'Good OI: 9,007,725, Good premium: ₹23.00'
    }
    notifier.send_entry_signal(trade5_entry)
    time.sleep(2)
    
    print("   Exit (Loss)...")
    trade5_exit = {
        'symbol': 'NIFTY11NOV25P25250',
        'strike': 25250,
        'option_type': 'PE',
        'entry_price': 23.00,
        'exit_price': 16.35,
        'quantity': 300,
        'net_pnl': -2035,
        'exit_reason': 'STOP_LOSS',
        'holding_time_minutes': 17
    }
    notifier.send_exit_signal(trade5_exit)
    time.sleep(2)
    
    # Trade 6: Quick Profit
    print("7️⃣ Trade 6: NIFTY 25300 PE Entry...")
    trade6_entry = {
        'symbol': 'NIFTY11NOV25P25300',
        'strike': 25300,
        'option_type': 'PE',
        'entry_price': 22.50,
        'quantity': 300,
        'strategy': 'CONTRARIAN',
        'reason': 'Good OI: 16,245,900, Good premium: ₹22.50'
    }
    notifier.send_entry_signal(trade6_entry)
    time.sleep(2)
    
    print("   Exit...")
    trade6_exit = {
        'symbol': 'NIFTY11NOV25P25300',
        'strike': 25300,
        'option_type': 'PE',
        'entry_price': 22.50,
        'exit_price': 25.90,
        'quantity': 300,
        'net_pnl': 980,
        'exit_reason': 'IMMEDIATE_PROFIT_BOOK',
        'holding_time_minutes': 10
    }
    notifier.send_exit_signal(trade6_exit)
    time.sleep(2)
    
    # Daily Summary
    print("8️⃣ Sending daily summary...")
    summary = {
        'starting_capital': 100000,
        'ending_capital': 146310,
        'net_pnl': 46310,
        'net_pnl_pct': 46.31,
        'total_trades': 16,
        'win_rate': 75.0,
        'wins': 12,
        'losses': 4
    }
    notifier.send_daily_summary(summary)
    
    print("\n" + "=" * 50)
    print("✅ ALL TEST MESSAGES SENT!")
    print("📱 Check your Telegram to see the messages")
    print("🎉 This is how your friends will see live signals!")

if __name__ == "__main__":
    send_todays_trades()
