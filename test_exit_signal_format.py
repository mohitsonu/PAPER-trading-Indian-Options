"""
Test script to preview the new exit signal format with P&L
"""
from datetime import datetime

def preview_exit_signals():
    """Preview what the exit signals will look like"""
    
    print("=" * 80)
    print("📱 TELEGRAM EXIT SIGNAL - NEW FORMAT PREVIEW")
    print("=" * 80)
    
    # Example 1: Winning trade (from today)
    print("\n" + "=" * 80)
    print("EXAMPLE 1: WINNING TRADE")
    print("=" * 80)
    
    trade1 = {
        'symbol': 'NIFTY02DEC25P26200',
        'strike': 26200,
        'option_type': 'PE',
        'entry_price': 69.60,
        'exit_price': 73.85,
        'quantity': 225,
        'net_pnl': 894.16,
        'gross_pnl': 956.25,
        'exit_reason': 'TRAILING_STOP (Locked profit: 6.6%)',
        'holding_time_minutes': 44
    }
    
    net_pnl = trade1['net_pnl']
    pnl_pct = ((trade1['exit_price'] - trade1['entry_price']) / trade1['entry_price']) * 100
    emoji = "🟢" if net_pnl > 0 else "🔴"
    status = "PROFIT" if net_pnl > 0 else "LOSS"
    
    message1 = f"""
{emoji} EXIT SIGNAL - {status} {emoji}

📊 Symbol: {trade1['symbol']}
🎯 Strike: {trade1['strike']} {trade1['option_type']}
💵 Entry: ₹{trade1['entry_price']:.2f}
💵 Exit: ₹{trade1['exit_price']:.2f}
📦 Quantity: {trade1['quantity']}
💰 Trade P&L: ₹{net_pnl:+,.2f} ({pnl_pct:+.1f}%)
⏱️ Holding Time: {trade1['holding_time_minutes']:.0f} minutes
📋 Exit Reason: {trade1['exit_reason']}

⏰ Time: {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}
"""
    print(message1)
    
    # Example 2: Losing trade (from today)
    print("\n" + "=" * 80)
    print("EXAMPLE 2: LOSING TRADE")
    print("=" * 80)
    
    trade2 = {
        'symbol': 'NIFTY02DEC25P26000',
        'strike': 26000,
        'option_type': 'PE',
        'entry_price': 24.85,
        'exit_price': 21.05,
        'quantity': 225,
        'net_pnl': -910.30,
        'gross_pnl': -855.00,
        'exit_reason': 'STOP_LOSS',
        'holding_time_minutes': 18
    }
    
    net_pnl = trade2['net_pnl']
    pnl_pct = ((trade2['exit_price'] - trade2['entry_price']) / trade2['entry_price']) * 100
    emoji = "🟢" if net_pnl > 0 else "🔴"
    status = "PROFIT" if net_pnl > 0 else "LOSS"
    
    message2 = f"""
{emoji} EXIT SIGNAL - {status} {emoji}

📊 Symbol: {trade2['symbol']}
🎯 Strike: {trade2['strike']} {trade2['option_type']}
💵 Entry: ₹{trade2['entry_price']:.2f}
💵 Exit: ₹{trade2['exit_price']:.2f}
📦 Quantity: {trade2['quantity']}
💰 Trade P&L: ₹{net_pnl:+,.2f} ({pnl_pct:+.1f}%)
⏱️ Holding Time: {trade2['holding_time_minutes']:.0f} minutes
📋 Exit Reason: {trade2['exit_reason']}

⏰ Time: {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}
"""
    print(message2)
    
    # Example 3: Big win
    print("\n" + "=" * 80)
    print("EXAMPLE 3: BIG WIN")
    print("=" * 80)
    
    trade3 = {
        'symbol': 'NIFTY02DEC25P26200',
        'strike': 26200,
        'option_type': 'PE',
        'entry_price': 75.05,
        'exit_price': 79.95,
        'quantity': 225,
        'net_pnl': 1039.62,
        'gross_pnl': 1102.50,
        'exit_reason': 'TRAILING_STOP (Locked profit: 6.8%)',
        'holding_time_minutes': 87
    }
    
    net_pnl = trade3['net_pnl']
    pnl_pct = ((trade3['exit_price'] - trade3['entry_price']) / trade3['entry_price']) * 100
    emoji = "🟢" if net_pnl > 0 else "🔴"
    status = "PROFIT" if net_pnl > 0 else "LOSS"
    
    message3 = f"""
{emoji} EXIT SIGNAL - {status} {emoji}

📊 Symbol: {trade3['symbol']}
🎯 Strike: {trade3['strike']} {trade3['option_type']}
💵 Entry: ₹{trade3['entry_price']:.2f}
💵 Exit: ₹{trade3['exit_price']:.2f}
📦 Quantity: {trade3['quantity']}
💰 Trade P&L: ₹{net_pnl:+,.2f} ({pnl_pct:+.1f}%)
⏱️ Holding Time: {trade3['holding_time_minutes']:.0f} minutes
📋 Exit Reason: {trade3['exit_reason']}

⏰ Time: {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}
"""
    print(message3)
    
    print("\n" + "=" * 80)
    print("✅ NEW FEATURES:")
    print("=" * 80)
    print("1. 💰 Trade P&L: Shows net profit/loss in rupees")
    print("2. 📊 P&L %: Shows percentage gain/loss")
    print("3. ✅ Format: ₹+894.16 (+6.1%) for wins")
    print("4. ❌ Format: ₹-910.30 (-15.3%) for losses")
    print("5. 🎨 Color: Green emoji for profit, Red for loss")
    print("\n" + "=" * 80)
    print("🚀 This will be sent to your Telegram on every exit!")
    print("=" * 80)

if __name__ == "__main__":
    preview_exit_signals()
