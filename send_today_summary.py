#!/usr/bin/env python3
"""Send today's Telegram summary manually"""
import pandas as pd
import os
from datetime import datetime
from telegram_signals.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
from telegram_signals.telegram_notifier import TelegramNotifier

def main():
    print("📱 SENDING TODAY'S TELEGRAM SUMMARY")
    print("=" * 50)
    
    if not TELEGRAM_ENABLED:
        print("❌ Telegram is disabled in config!")
        print("💡 Edit telegram_signals/config.py and set TELEGRAM_ENABLED = True")
        return
    
    notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Test connection
    print("🧪 Testing Telegram connection...")
    if not notifier.test_connection():
        print("❌ Connection failed! Check your bot token and chat ID")
        return
    
    # Load today's trades
    today = datetime.now().strftime("%Y%m%d")
    today_csv = f"high_accuracy_trades_{today}.csv"
    
    print(f"📅 Date: {today}")
    print(f"📁 Looking for: {today_csv}")
    
    # Get starting capital from persistence
    capital = 100000  # Default
    try:
        import json
        if os.path.exists('capital_persistence.json'):
            with open('capital_persistence.json', 'r') as f:
                data = json.load(f)
                today_date = datetime.now().strftime("%Y-%m-%d")
                if today_date in data.get('daily_sessions', {}):
                    capital = data['daily_sessions'][today_date].get('start_capital', 100000)
                    print(f"💰 Starting capital from persistence: ₹{capital:,.2f}")
    except Exception as e:
        print(f"⚠️ Could not load persistence: {e}")
    
    if os.path.exists(today_csv):
        df = pd.read_csv(today_csv)
        exits = df[df['action'] == 'EXIT']
        
        print(f"✅ Found {len(df)} total records, {len(exits)} exits")
        
        # Calculate metrics
        if not exits.empty:
            pnl_col = None
            for col in ['net_pnl_after_charges', 'pnl_after_charges', 'pnl', 'gross_pnl']:
                if col in exits.columns:
                    pnl_col = col
                    break
            
            if pnl_col:
                net_pnl = exits[pnl_col].sum()
                wins = len(exits[exits[pnl_col] > 0])
                losses = len(exits[exits[pnl_col] < 0])
                total_trades = len(exits)
                win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
                
                print(f"💰 Net P&L: ₹{net_pnl:+,.2f}")
                print(f"📊 Trades: {total_trades} ({wins}W / {losses}L)")
                print(f"📈 Win Rate: {win_rate:.1f}%")
            else:
                print("⚠️ No P&L column found")
                net_pnl = 0
                wins = 0
                losses = 0
                total_trades = 0
                win_rate = 0
        else:
            print("⚠️ No exit trades found")
            net_pnl = 0
            wins = 0
            losses = 0
            total_trades = 0
            win_rate = 0
    else:
        print(f"⚠️ File not found: {today_csv}")
        print("💡 No trades were taken today")
        net_pnl = 0
        wins = 0
        losses = 0
        total_trades = 0
        win_rate = 0
    
    ending_capital = capital + net_pnl
    net_pnl_pct = (net_pnl / capital * 100) if capital > 0 else 0
    
    summary_data = {
        'starting_capital': capital,
        'ending_capital': ending_capital,
        'net_pnl': net_pnl,
        'net_pnl_pct': net_pnl_pct,
        'total_trades': total_trades,
        'win_rate': win_rate,
        'wins': wins,
        'losses': losses,
        'csv_file': today_csv if os.path.exists(today_csv) else None
    }
    
    print("\n📤 Sending to Telegram...")
    success = notifier.send_daily_summary(summary_data)
    
    if success:
        print("✅ Daily summary sent successfully!")
        print("📱 Check your Telegram channel")
    else:
        print("❌ Failed to send summary")

if __name__ == "__main__":
    main()
