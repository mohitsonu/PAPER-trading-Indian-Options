#!/usr/bin/env python3
"""
Send Telegram summary manually for today's trades
"""

import os
import pandas as pd
from datetime import datetime
from telegram_signals.telegram_notifier import TelegramNotifier
from telegram_signals.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED

def send_summary_now():
    print("=" * 70)
    print("📱 MANUAL TELEGRAM SUMMARY SENDER")
    print("=" * 70)
    
    if not TELEGRAM_ENABLED:
        print("❌ Telegram is disabled in config!")
        return
    
    # Get today's CSV file
    today_csv = f"high_accuracy_trades_{datetime.now().strftime('%Y%m%d')}.csv"
    
    if not os.path.exists(today_csv):
        print(f"❌ No trades file found: {today_csv}")
        return
    
    print(f"\n✅ Found trades file: {today_csv}")
    
    # Load trades
    df = pd.read_csv(today_csv)
    exits = df[df['action'] == 'EXIT']
    
    if exits.empty:
        print("⚠️ No completed trades found (no EXIT records)")
        print("   Trades might still be open or no trades taken today")
        return
    
    print(f"✅ Found {len(exits)} completed trades")
    
    # Calculate metrics
    pnl_col = None
    for col in ['net_pnl_after_charges', 'pnl_after_charges', 'pnl', 'gross_pnl']:
        if col in exits.columns:
            pnl_col = col
            break
    
    if not pnl_col:
        print("❌ No P&L column found in CSV")
        return
    
    net_pnl = exits[pnl_col].sum()
    wins = len(exits[exits[pnl_col] > 0])
    losses = len(exits[exits[pnl_col] < 0])
    total_trades = len(exits)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    # Get capital from first row
    starting_capital = 100000  # Default
    if 'capital' in df.columns and not df.empty:
        first_capital = df.iloc[0]['capital']
        if pd.notna(first_capital):
            starting_capital = float(first_capital)
    
    ending_capital = starting_capital + net_pnl
    net_pnl_pct = (net_pnl / starting_capital * 100) if starting_capital > 0 else 0
    
    print(f"\n📊 Summary:")
    print(f"   Starting Capital: ₹{starting_capital:,.2f}")
    print(f"   Ending Capital: ₹{ending_capital:,.2f}")
    print(f"   Net P&L: ₹{net_pnl:+,.2f} ({net_pnl_pct:+.2f}%)")
    print(f"   Total Trades: {total_trades}")
    print(f"   Win Rate: {win_rate:.1f}% ({wins}W / {losses}L)")
    
    # Send to Telegram
    print(f"\n📱 Sending to Telegram...")
    
    try:
        notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
        summary_data = {
            'starting_capital': starting_capital,
            'ending_capital': ending_capital,
            'net_pnl': net_pnl,
            'net_pnl_pct': net_pnl_pct,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'wins': wins,
            'losses': losses,
            'csv_file': today_csv
        }
        
        notifier.send_daily_summary(summary_data)
        print("✅ Telegram summary sent successfully!")
        print("   Check your Telegram channel for the message and CSV file")
        
    except Exception as e:
        print(f"❌ Failed to send Telegram summary: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    send_summary_now()
