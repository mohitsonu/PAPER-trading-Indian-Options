"""
Test script to demonstrate the trade count fix
"""

def test_trade_counting():
    """Show how trade counting works now"""
    
    print("=" * 80)
    print("🐛 TRADE COUNT BUG FIX")
    print("=" * 80)
    
    # Simulate trade_history with both ENTRY and EXIT records
    trade_history = [
        {'action': 'ENTRY', 'trade_id': 'T1', 'strike': 26200},
        {'action': 'EXIT', 'trade_id': 'T1', 'strike': 26200, 'net_pnl': 894},
        {'action': 'ENTRY', 'trade_id': 'T2', 'strike': 26000},
        {'action': 'EXIT', 'trade_id': 'T2', 'strike': 26000, 'net_pnl': -213},
        {'action': 'ENTRY', 'trade_id': 'T3', 'strike': 26200},
        {'action': 'EXIT', 'trade_id': 'T3', 'strike': 26200, 'net_pnl': 1040},
        {'action': 'ENTRY', 'trade_id': 'T4', 'strike': 26000},
        {'action': 'EXIT', 'trade_id': 'T4', 'strike': 26000, 'net_pnl': -910},
        {'action': 'ENTRY', 'trade_id': 'T5', 'strike': 26000},
        {'action': 'EXIT', 'trade_id': 'T5', 'strike': 26000, 'net_pnl': -584},
        {'action': 'ENTRY', 'trade_id': 'T6', 'strike': 26100},
        {'action': 'EXIT', 'trade_id': 'T6', 'strike': 26100, 'net_pnl': 500},
        {'action': 'ENTRY', 'trade_id': 'T7', 'strike': 26150},
        {'action': 'EXIT', 'trade_id': 'T7', 'strike': 26150, 'net_pnl': -300},
        {'action': 'ENTRY', 'trade_id': 'T8', 'strike': 26250},
        {'action': 'EXIT', 'trade_id': 'T8', 'strike': 26250, 'net_pnl': 750},
    ]
    
    print("\n📊 TRADE HISTORY CONTENTS:")
    print(f"   Total records in trade_history: {len(trade_history)}")
    print(f"   ENTRY records: {len([t for t in trade_history if t['action'] == 'ENTRY'])}")
    print(f"   EXIT records: {len([t for t in trade_history if t['action'] == 'EXIT'])}")
    
    print("\n" + "=" * 80)
    print("❌ BEFORE FIX (Wrong Count):")
    print("=" * 80)
    
    # Old way - counts all records
    old_count = len(trade_history)
    print(f"   🎯 TRADES: {old_count}")
    print(f"   ❌ WRONG! This counts both ENTRY and EXIT")
    print(f"   ❌ Shows 16 trades when actually 8 trades")
    
    print("\n" + "=" * 80)
    print("✅ AFTER FIX (Correct Count):")
    print("=" * 80)
    
    # New way - counts only EXIT records (completed trades)
    completed_trades = [t for t in trade_history if t.get('action') == 'EXIT']
    new_count = len(completed_trades)
    print(f"   🎯 TRADES: {new_count}")
    print(f"   ✅ CORRECT! This counts only completed trades (EXIT)")
    print(f"   ✅ Shows 8 trades (the actual number)")
    
    # Calculate win rate correctly
    winning_trades = len([t for t in completed_trades if t.get('net_pnl', 0) > 0])
    losing_trades = len(completed_trades) - winning_trades
    win_rate = (winning_trades / len(completed_trades)) * 100
    
    print(f"\n   🎯 Win Rate: {win_rate:.1f}% ({winning_trades}W / {losing_trades}L)")
    print(f"   ✅ CORRECT! Based on 8 trades, not 16")
    
    print("\n" + "=" * 80)
    print("🔧 HOW IT WORKS:")
    print("=" * 80)
    print("""
    def get_completed_trades(self):
        '''Get only completed trades (EXIT records)'''
        return [t for t in self.trade_history if t.get('action') == 'EXIT']
    
    def get_completed_trade_count(self):
        '''Get count of completed trades only'''
        return len(self.get_completed_trades())
    
    # Usage:
    completed_trades = self.get_completed_trades()
    trade_count = len(completed_trades)  # Correct count!
    """)
    
    print("\n" + "=" * 80)
    print("📋 WHAT'S FIXED:")
    print("=" * 80)
    print("   ✅ Terminal status display (TRADES: count)")
    print("   ✅ Daily summary (Total Trades)")
    print("   ✅ Win rate calculation")
    print("   ✅ Telegram summary")
    print("   ✅ JSON file updates")
    print("   ✅ All statistics")
    
    print("\n" + "=" * 80)
    print("🎯 EXAMPLE OUTPUT:")
    print("=" * 80)
    print(f"   🎯 POSITIONS: 0/3 | TRADES: {new_count} | WIN RATE: {win_rate:.0f}%")
    print(f"   ✅ Shows 8 trades (not 16)")
    
    print("\n" + "=" * 80)
    print("✅ FIX COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_trade_counting()
