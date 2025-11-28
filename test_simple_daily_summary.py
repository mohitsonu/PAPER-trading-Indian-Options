"""
Test script to preview the NEW SIMPLE daily summary format
"""
from datetime import datetime

def preview_simple_summary():
    """Preview the new clean, simple daily summary"""
    
    print("=" * 80)
    print("📱 NEW SIMPLE DAILY SUMMARY FORMAT")
    print("=" * 80)
    
    # Example 1: Losing day (like today)
    print("\n" + "=" * 80)
    print("EXAMPLE 1: LOSING DAY (Like Nov 28)")
    print("=" * 80)
    
    summary1 = {
        'starting_capital': 100000,
        'ending_capital': 98578.54,
        'net_pnl': 226.45,  # Actual net after charges
        'net_pnl_pct': 0.23,
        'total_trades': 5,
        'win_rate': 40.0,
        'wins': 2,
        'losses': 3,
        'csv_file': 'high_accuracy_trades_20251128.csv'
    }
    
    emoji = "🎉" if summary1['net_pnl'] > 0 else "😔"
    
    message1 = f"""
{emoji} DAILY SUMMARY {emoji}

📅 Date: {datetime.now().strftime('%d-%b-%Y')}

💰 Starting Capital: ₹{summary1['starting_capital']:,.2f}
💰 Ending Capital: ₹{summary1['ending_capital']:,.2f}
📊 Net Profit (After Charges): ₹{summary1['net_pnl']:+,.2f} ({summary1['net_pnl_pct']:+.2f}%)

📋 Total Trades: {summary1['total_trades']}
🎯 Win Rate: {summary1['win_rate']:.1f}% ({summary1['wins']}W / {summary1['losses']}L)

⏰ Session End: {datetime.now().strftime('%I:%M:%S %p')}
"""
    print(message1)
    print("📎 ATTACHMENT: high_accuracy_trades_20251128.csv")
    
    # Example 2: Winning day
    print("\n" + "=" * 80)
    print("EXAMPLE 2: WINNING DAY")
    print("=" * 80)
    
    summary2 = {
        'starting_capital': 100000,
        'ending_capital': 102500,
        'net_pnl': 2500,
        'net_pnl_pct': 2.50,
        'total_trades': 6,
        'win_rate': 66.7,
        'wins': 4,
        'losses': 2,
        'csv_file': 'high_accuracy_trades_20251129.csv'
    }
    
    emoji = "🎉" if summary2['net_pnl'] > 0 else "😔"
    
    message2 = f"""
{emoji} DAILY SUMMARY {emoji}

📅 Date: {datetime.now().strftime('%d-%b-%Y')}

💰 Starting Capital: ₹{summary2['starting_capital']:,.2f}
💰 Ending Capital: ₹{summary2['ending_capital']:,.2f}
📊 Net Profit (After Charges): ₹{summary2['net_pnl']:+,.2f} ({summary2['net_pnl_pct']:+.2f}%)

📋 Total Trades: {summary2['total_trades']}
🎯 Win Rate: {summary2['win_rate']:.1f}% ({summary2['wins']}W / {summary2['losses']}L)

⏰ Session End: {datetime.now().strftime('%I:%M:%S %p')}
"""
    print(message2)
    print("📎 ATTACHMENT: high_accuracy_trades_20251129.csv")
    
    # Example 3: Big winning day
    print("\n" + "=" * 80)
    print("EXAMPLE 3: BIG WINNING DAY")
    print("=" * 80)
    
    summary3 = {
        'starting_capital': 100000,
        'ending_capital': 105000,
        'net_pnl': 5000,
        'net_pnl_pct': 5.00,
        'total_trades': 7,
        'win_rate': 85.7,
        'wins': 6,
        'losses': 1,
        'csv_file': 'high_accuracy_trades_20251130.csv'
    }
    
    emoji = "🎉" if summary3['net_pnl'] > 0 else "😔"
    
    message3 = f"""
{emoji} DAILY SUMMARY {emoji}

📅 Date: {datetime.now().strftime('%d-%b-%Y')}

💰 Starting Capital: ₹{summary3['starting_capital']:,.2f}
💰 Ending Capital: ₹{summary3['ending_capital']:,.2f}
📊 Net Profit (After Charges): ₹{summary3['net_pnl']:+,.2f} ({summary3['net_pnl_pct']:+.2f}%)

📋 Total Trades: {summary3['total_trades']}
🎯 Win Rate: {summary3['win_rate']:.1f}% ({summary3['wins']}W / {summary3['losses']}L)

⏰ Session End: {datetime.now().strftime('%I:%M:%S %p')}
"""
    print(message3)
    print("📎 ATTACHMENT: high_accuracy_trades_20251130.csv")
    
    print("\n" + "=" * 80)
    print("✅ WHAT YOU GET:")
    print("=" * 80)
    print("1. 📱 Clean, simple message")
    print("2. 💰 Net Profit (After Charges) - The real P&L")
    print("3. 🎯 Win Rate with W/L breakdown")
    print("4. 📎 CSV file attachment")
    print("5. 😔 Sad emoji for loss, 🎉 Happy emoji for profit")
    print()
    print("=" * 80)
    print("🚀 SENT AUTOMATICALLY AT 3:15 PM EVERY DAY!")
    print("=" * 80)

if __name__ == "__main__":
    preview_simple_summary()
