import json
import pandas as pd

# Load today's data
with open('high_accuracy_updates_20251128.json', 'r') as f:
    data = json.load(f)

print('=' * 80)
print('📊 NOV 28, 2025 - TRADING PERFORMANCE ANALYSIS')
print('=' * 80)

# Overall Performance
perf = data['performance']
print(f'\n🎯 OVERALL PERFORMANCE:')
print(f'   Net P&L: ₹{perf["total_net_pnl"]:.2f} ({(perf["total_net_pnl"]/100000)*100:.2f}%)')
print(f'   Win Rate: {perf["win_rate"]:.1f}% ({perf["winning_trades"]}W/{perf["losing_trades"]}L)')
print(f'   Total Trades: {perf["total_trades"]}')
print(f'   Accuracy Score: {perf["avg_accuracy_score"]:.0f}/100')
print(f'   Profit Factor: {perf["profit_factor"]:.2f}')
print(f'   Avg Holding Time: {perf["avg_holding_time_minutes"]:.1f} minutes')

# Capital tracking
print(f'\n💰 CAPITAL:')
print(f'   Starting: ₹{data["initial_capital"]:,.2f}')
print(f'   Ending: ₹{data["current_capital"]:,.2f}')
print(f'   Change: ₹{data["current_capital"] - data["initial_capital"]:,.2f}')

# Trade breakdown
print(f'\n📈 TRADE BREAKDOWN:')
for i, trade in enumerate(data['trades'], 1):
    result = '✅ WIN' if trade['net_pnl'] > 0 else '❌ LOSS'
    pnl_pct = (trade['net_pnl'] / (trade['entry_price'] * trade['quantity'])) * 100
    print(f'\n   Trade {i}: {result}')
    print(f'   Strategy: {trade["strategy"]}')
    print(f'   Strike: {trade["strike"]} {trade["option_type"]}')
    print(f'   Entry: ₹{trade["entry_price"]} → Exit: ₹{trade["exit_price"]}')
    print(f'   P&L: ₹{trade["net_pnl"]:.2f} ({pnl_pct:.1f}%) | Gross: ₹{trade["gross_pnl"]:.2f}')
    print(f'   Holding: {trade["holding_minutes"]:.1f} mins')
    print(f'   Exit: {trade["exit_reason"]}')

# Strategy performance
print(f'\n🎲 STRATEGY PERFORMANCE:')
contrarian_trades = [t for t in data['trades'] if t['strategy'] == 'CONTRARIAN']
trend_rider_trades = [t for t in data['trades'] if t['strategy'] == 'TREND_RIDER']

if contrarian_trades:
    c_wins = sum(1 for t in contrarian_trades if t['net_pnl'] > 0)
    c_pnl = sum(t['net_pnl'] for t in contrarian_trades)
    c_wr = (c_wins / len(contrarian_trades)) * 100
    print(f'   CONTRARIAN: {len(contrarian_trades)} trades, {c_wins}W/{len(contrarian_trades)-c_wins}L ({c_wr:.1f}% WR), ₹{c_pnl:.2f}')

if trend_rider_trades:
    t_wins = sum(1 for t in trend_rider_trades if t['net_pnl'] > 0)
    t_pnl = sum(t['net_pnl'] for t in trend_rider_trades)
    t_wr = (t_wins / len(trend_rider_trades)) * 100
    print(f'   TREND_RIDER: {len(trend_rider_trades)} trades, {t_wins}W/{len(trend_rider_trades)-t_wins}L ({t_wr:.1f}% WR), ₹{t_pnl:.2f}')

# Charges analysis
print(f'\n💸 COST ANALYSIS:')
print(f'   Gross P&L: ₹{perf["total_gross_pnl"]:.2f}')
print(f'   Total Charges: ₹{perf["total_charges"]:.2f}')
print(f'   Net P&L: ₹{perf["total_net_pnl"]:.2f}')
charges_impact = (perf["total_charges"]/perf["total_gross_pnl"])*100 if perf["total_gross_pnl"] > 0 else 0
print(f'   Charges Impact: {charges_impact:.1f}% of gross profit')

# Strike analysis
print(f'\n🎯 STRIKE ANALYSIS:')
strikes = {}
for trade in data['trades']:
    key = f"{trade['strike']} {trade['option_type']}"
    if key not in strikes:
        strikes[key] = {'count': 0, 'pnl': 0, 'wins': 0}
    strikes[key]['count'] += 1
    strikes[key]['pnl'] += trade['net_pnl']
    if trade['net_pnl'] > 0:
        strikes[key]['wins'] += 1

for strike, stats in strikes.items():
    wr = (stats['wins'] / stats['count']) * 100
    print(f'   {strike}: {stats["count"]} trades, {stats["wins"]}W/{stats["count"]-stats["wins"]}L ({wr:.0f}% WR), ₹{stats["pnl"]:.2f}')

# Time analysis
print(f'\n⏰ TIMING ANALYSIS:')
for trade in data['trades']:
    entry_time = trade['entry_time'].split('T')[1][:5]
    exit_time = trade['exit_time'].split('T')[1][:5]
    result = '✅' if trade['net_pnl'] > 0 else '❌'
    print(f'   {result} {entry_time}-{exit_time} ({trade["holding_minutes"]:.0f}m): {trade["strategy"]} ₹{trade["net_pnl"]:.0f}')

print('\n' + '=' * 80)
print('📝 KEY OBSERVATIONS:')
print('=' * 80)

# Observations
if perf['win_rate'] < 50:
    print('⚠️  Win rate below 50% - Need to improve trade selection')
if perf['total_net_pnl'] > 0:
    print('✅ Profitable day despite low win rate - Good risk management')
else:
    print('❌ Losing day - Review strategy and market conditions')

# Check for overtrading same strike
for strike, stats in strikes.items():
    if stats['count'] > 2:
        print(f'⚠️  Overtrading {strike}: {stats["count"]} trades (Max should be 2)')

print('\n')
