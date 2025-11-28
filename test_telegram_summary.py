"""
Test script to preview the Telegram daily summary format
"""
from datetime import datetime

def preview_telegram_summary():
    """Preview what the Telegram message will look like"""
    
    # Sample data from today (Nov 28)
    summary_data = {
        'starting_capital': 100000,
        'ending_capital': 98578.54,
        'net_pnl': -1421.46,
        'net_pnl_pct': -1.42,
        'total_trades': 5,
        'win_rate': 40.0,
        'wins': 2,
        'losses': 3,
        'gross_pnl': 517.50,
        'total_charges': 291.05,
        'avg_score': 100,
        'avg_holding': 67,
        'avg_win': 966.89,
        'avg_loss': -569.11,
        'profit_factor': 1.78,
        'high_score_trades': 5,
        'high_score_success': 40.0,
        'csv_file': 'high_accuracy_trades_20251128.csv',
        'json_file': 'high_accuracy_updates_20251128.json'
    }
    
    starting_capital = summary_data.get('starting_capital', 0)
    ending_capital = summary_data.get('ending_capital', 0)
    net_pnl = summary_data.get('net_pnl', 0)
    net_pnl_pct = summary_data.get('net_pnl_pct', 0)
    total_trades = summary_data.get('total_trades', 0)
    win_rate = summary_data.get('win_rate', 0)
    wins = summary_data.get('wins', 0)
    losses = summary_data.get('losses', 0)
    
    gross_pnl = summary_data.get('gross_pnl', 0)
    total_charges = summary_data.get('total_charges', 0)
    avg_score = summary_data.get('avg_score', 0)
    avg_holding = summary_data.get('avg_holding', 0)
    avg_win = summary_data.get('avg_win', 0)
    avg_loss = summary_data.get('avg_loss', 0)
    profit_factor = summary_data.get('profit_factor', 0)
    high_score_trades = summary_data.get('high_score_trades', 0)
    high_score_success = summary_data.get('high_score_success', 0)
    csv_file = summary_data.get('csv_file', '')
    json_file = summary_data.get('json_file', '')
    
    emoji = "🎉" if net_pnl > 0 else "😔"
    
    message = f"""
🏆 HIGH ACCURACY TRADING RESULTS
{'=' * 50}

💰 Starting Capital: ₹{starting_capital:,.2f}
💰 Ending Capital: ₹{ending_capital:,.2f}
📊 Net P&L: ₹{net_pnl:+,.2f} ({net_pnl_pct:+.2f}%)
📋 Total Trades: {total_trades}

📈 PERFORMANCE METRICS:
🎯 Win Rate: {win_rate:.1f}% ({wins}W / {losses}L)
📊 Average Accuracy Score: {avg_score:.0f}/100
⏱️ Average Holding Time: {avg_holding:.0f} minutes

💰 Gross P&L: ₹{gross_pnl:+,.2f}
💸 Total Charges: ₹{total_charges:.2f}
🎯 Profit Factor: {profit_factor:.2f}
"""
    
    if avg_win > 0:
        message += f"📈 Average Win: ₹{avg_win:,.2f}\n"
    if avg_loss < 0:
        message += f"📉 Average Loss: ₹{avg_loss:,.2f}\n"
    
    if high_score_trades > 0:
        message += f"""
🏆 QUALITY ANALYSIS:
⭐ High Score Trades (90+): {high_score_trades}/{total_trades}
🎯 High Score Success Rate: {high_score_success:.1f}%
"""
    
    message += f"""
📁 FILES GENERATED:
📊 CSV Journal: {csv_file}
📋 JSON Updates: {json_file}

⏰ Session End: {datetime.now().strftime('%I:%M:%S %p')}
"""
    
    if win_rate >= 70:
        message += "\n💡 ALGORITHM VALIDATION:\n✅ Excellent performance - Quality over quantity achieved!"
    elif win_rate >= 60:
        message += "\n💡 ALGORITHM VALIDATION:\n✅ Good performance - Algorithm working as expected"
    elif win_rate >= 50:
        message += "\n💡 ALGORITHM VALIDATION:\n⚠️ Moderate performance - Monitor for improvements"
    else:
        message += "\n💡 ALGORITHM VALIDATION:\n⚠️ Win rate below target - Review entry criteria"
    
    print("=" * 80)
    print("📱 TELEGRAM DAILY SUMMARY PREVIEW")
    print("=" * 80)
    print(message)
    print("=" * 80)
    print("\n📎 ATTACHMENTS:")
    print(f"   📊 CSV File: {csv_file}")
    print("   (File will be sent as document attachment)")
    print("\n" + "=" * 80)
    print("✅ This message will be sent to your Telegram channel after market close")
    print("=" * 80)

if __name__ == "__main__":
    preview_telegram_summary()
