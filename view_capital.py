#!/usr/bin/env python3
"""
💰 CAPITAL STATUS VIEWER
View current capital and P&L from persistence file
"""

import json
import os
from datetime import datetime

def view_capital_status():
    """View current capital status"""
    
    capital_file = "capital_persistence.json"
    
    print("💰 CAPITAL STATUS")
    print("=" * 50)
    
    if not os.path.exists(capital_file):
        print("❌ No capital persistence file found")
        print("   This means no trading session has been completed yet")
        print("   Initial capital will be ₹100,000 for first session")
        return
    
    try:
        with open(capital_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        current_capital = data.get('current_capital', 0)
        initial_capital = data.get('initial_capital', 100000)
        total_pnl = data.get('total_pnl', 0)
        pnl_percentage = data.get('pnl_percentage', 0)
        last_updated = data.get('last_updated', 'Unknown')
        session_date = data.get('session_date', 'Unknown')
        trades_completed = data.get('trades_completed', 0)
        
        print(f"📊 Current Capital: ₹{current_capital:,.2f}")
        print(f"🎯 Initial Capital: ₹{initial_capital:,.2f}")
        print(f"📈 Total P&L: ₹{total_pnl:+,.2f} ({pnl_percentage:+.2f}%)")
        print(f"📅 Last Session: {session_date}")
        print(f"🕒 Last Updated: {last_updated}")
        print(f"📊 Trades Completed: {trades_completed}")
        
        # Show daily P&L tracking
        daily_sessions = data.get('daily_sessions', {})
        if daily_sessions:
            print(f"\n📅 DAILY P&L HISTORY:")
            print("-" * 50)
            for date, session in sorted(daily_sessions.items(), reverse=True):
                daily_pnl = session.get('daily_pnl', 0)
                trades = session.get('trades_count', 0)
                start_cap = session.get('start_capital', 0)
                end_cap = session.get('end_capital', 0)
                
                status = "✅" if daily_pnl > 0 else "❌" if daily_pnl < 0 else "➖"
                print(f"{status} {date}: ₹{daily_pnl:+,.2f} | {trades} trades | ₹{start_cap:,.0f} → ₹{end_cap:,.0f}")
        
        print("\n" + "=" * 50)
        
        if total_pnl > 0:
            print(f"✅ OVERALL PROFIT: Your capital has grown by ₹{total_pnl:,.2f}")
        elif total_pnl < 0:
            print(f"❌ OVERALL LOSS: Your capital has decreased by ₹{abs(total_pnl):,.2f}")
        else:
            print("➖ BREAKEVEN: No profit or loss")
        
        print(f"\n🔄 Next session will start with: ₹{current_capital:,.2f}")
        
    except Exception as e:
        print(f"❌ Error reading capital file: {e}")

if __name__ == "__main__":
    view_capital_status()