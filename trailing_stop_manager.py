#!/usr/bin/env python3
"""
🎯 SMART TRAILING STOP MANAGER
Advanced trailing stop loss system that adapts to market conditions

Features:
1. Dynamic trailing based on profit level
2. Adaptive trailing based on market mode
3. Breakeven protection
4. Profit lock-in at key levels
"""

class TrailingStopManager:
    """
    Manages trailing stops for all positions
    Adapts trailing behavior based on:
    - Current profit level
    - Market mode (trending/ranging/volatile)
    - Time held
    - Strategy type
    """
    
    def __init__(self):
        self.position_trails = {}  # Track trailing stops per position
        
    def calculate_trailing_stop(self, position, current_price, market_mode='RANGING'):
        """
        Calculate smart trailing stop for a position
        
        Returns: {
            'trailing_stop': float,
            'should_exit': bool,
            'reason': str,
            'profit_locked': float
        }
        """
        
        entry_price = position['entry_price']
        position_id = position.get('trade_id', 'unknown')
        
        # Calculate current profit
        profit = current_price - entry_price
        profit_pct = (profit / entry_price) if entry_price > 0 else 0
        
        # Initialize trailing stop for this position if not exists
        if position_id not in self.position_trails:
            self.position_trails[position_id] = {
                'highest_price': current_price,
                'trailing_stop': entry_price * 0.75,  # Initial stop at -25%
                'profit_locked': 0
            }
        
        trail_data = self.position_trails[position_id]
        
        # Update highest price seen
        if current_price > trail_data['highest_price']:
            trail_data['highest_price'] = current_price
        
        # Calculate trailing stop based on profit level
        trailing_stop = self._calculate_adaptive_trail(
            entry_price,
            trail_data['highest_price'],
            profit_pct,
            market_mode
        )
        
        # Update trailing stop (only move up, never down)
        if trailing_stop > trail_data['trailing_stop']:
            trail_data['trailing_stop'] = trailing_stop
            trail_data['profit_locked'] = (trailing_stop - entry_price) / entry_price
        
        # Check if should exit
        should_exit = current_price <= trail_data['trailing_stop']
        
        # Determine reason
        if should_exit:
            if profit_pct > 0:
                reason = f"TRAILING_STOP (Locked profit: {trail_data['profit_locked']*100:.1f}%)"
            else:
                reason = "STOP_LOSS"
        else:
            reason = f"Trailing active (Protected: {trail_data['profit_locked']*100:.1f}%)"
        
        return {
            'trailing_stop': trail_data['trailing_stop'],
            'should_exit': should_exit,
            'reason': reason,
            'profit_locked': trail_data['profit_locked'],
            'highest_price': trail_data['highest_price']
        }
    
    def _calculate_adaptive_trail(self, entry_price, highest_price, profit_pct, market_mode):
        """
        Calculate trailing stop based on profit level and market mode
        
        Trailing Strategy:
        - 0-5% profit: No trail (use initial stop)
        - 5-10% profit: Breakeven trail (lock in 2%)
        - 10-20% profit: Conservative trail (lock in 5%)
        - 20-30% profit: Moderate trail (lock in 10%)
        - 30%+ profit: Aggressive trail (lock in 15%)
        
        Market Mode Adjustments:
        - TRENDING: Wider trails (let profits run)
        - RANGING: Tighter trails (take profits quickly)
        - VOLATILE: Medium trails (balance risk/reward)
        """
        
        # Base trailing percentages
        if profit_pct >= 0.30:  # 30%+ profit
            trail_pct = 0.15  # Lock in 15%
        elif profit_pct >= 0.20:  # 20-30% profit
            trail_pct = 0.10  # Lock in 10%
        elif profit_pct >= 0.10:  # 10-20% profit
            trail_pct = 0.05  # Lock in 5%
        elif profit_pct >= 0.05:  # 5-10% profit
            trail_pct = 0.02  # Lock in 2% (breakeven)
        else:  # <5% profit
            return entry_price * 0.75  # Initial stop at -25%
        
        # Adjust based on market mode
        if market_mode == 'TRENDING':
            # Wider trails in trending markets (let profits run)
            trail_pct *= 0.8  # 20% wider
        elif market_mode == 'RANGING':
            # Tighter trails in ranging markets (take profits)
            trail_pct *= 1.2  # 20% tighter
        elif market_mode == 'VOLATILE':
            # Medium trails in volatile markets
            trail_pct *= 1.0  # No adjustment
        
        # Calculate trailing stop from highest price
        trailing_stop = highest_price * (1 - (highest_price - entry_price) / highest_price + trail_pct)
        
        # Ensure trailing stop is always above entry (for profitable trades)
        if profit_pct > 0:
            trailing_stop = max(trailing_stop, entry_price * (1 + trail_pct))
        
        return trailing_stop
    
    def get_trail_summary(self, position_id):
        """Get trailing stop summary for a position"""
        if position_id in self.position_trails:
            trail = self.position_trails[position_id]
            return {
                'highest_price': trail['highest_price'],
                'trailing_stop': trail['trailing_stop'],
                'profit_locked': trail['profit_locked']
            }
        return None
    
    def remove_position(self, position_id):
        """Remove position from tracking after exit"""
        if position_id in self.position_trails:
            del self.position_trails[position_id]
    
    def get_all_trails(self):
        """Get all active trailing stops"""
        return self.position_trails.copy()
    
    def reset(self):
        """Reset all trailing stops (use at start of day)"""
        self.position_trails = {}


# ========================================
# STRATEGY-SPECIFIC TRAILING STOPS
# ========================================

class StrategyTrailingStops:
    """
    Different trailing stop strategies for different trading strategies
    """
    
    @staticmethod
    def scalper_trail(entry_price, current_price, profit_pct):
        """
        SCALPER: Tight trailing (quick profits)
        - 10%+ profit: Trail at 5%
        - 15%+ profit: Trail at 8%
        - 20%+ profit: Trail at 10%
        """
        if profit_pct >= 0.20:
            return entry_price * 1.10
        elif profit_pct >= 0.15:
            return entry_price * 1.08
        elif profit_pct >= 0.10:
            return entry_price * 1.05
        else:
            return entry_price * 0.90  # -10% stop
    
    @staticmethod
    def trend_rider_trail(entry_price, highest_price, profit_pct):
        """
        TREND_RIDER: Wide trailing (let profits run)
        - 20%+ profit: Trail at 10%
        - 30%+ profit: Trail at 15%
        - 40%+ profit: Trail at 20%
        """
        if profit_pct >= 0.40:
            return highest_price * 0.80  # Trail 20% from peak
        elif profit_pct >= 0.30:
            return highest_price * 0.85  # Trail 15% from peak
        elif profit_pct >= 0.20:
            return highest_price * 0.90  # Trail 10% from peak
        else:
            return entry_price * 0.75  # -25% stop
    
    @staticmethod
    def contrarian_trail(entry_price, current_price, profit_pct):
        """
        CONTRARIAN: Medium trailing (balanced)
        - 15%+ profit: Trail at 7%
        - 25%+ profit: Trail at 12%
        - 35%+ profit: Trail at 17%
        """
        if profit_pct >= 0.35:
            return entry_price * 1.17
        elif profit_pct >= 0.25:
            return entry_price * 1.12
        elif profit_pct >= 0.15:
            return entry_price * 1.07
        else:
            return entry_price * 0.75  # -25% stop
    
    @staticmethod
    def support_bounce_trail(entry_price, current_price, profit_pct):
        """
        SUPPORT_BOUNCE: Tight trailing (quick reversal risk)
        - 15%+ profit: Trail at 8%
        - 25%+ profit: Trail at 12%
        - 35%+ profit: Trail at 15%
        """
        if profit_pct >= 0.35:
            return entry_price * 1.15
        elif profit_pct >= 0.25:
            return entry_price * 1.12
        elif profit_pct >= 0.15:
            return entry_price * 1.08
        else:
            return entry_price * 0.80  # -20% stop


# ========================================
# PROFIT PROTECTION LEVELS
# ========================================

class ProfitProtection:
    """
    Automatic profit protection at key levels
    """
    
    PROTECTION_LEVELS = [
        {'profit': 0.50, 'lock': 0.25, 'name': '50% profit → Lock 25%'},
        {'profit': 0.40, 'lock': 0.20, 'name': '40% profit → Lock 20%'},
        {'profit': 0.30, 'lock': 0.15, 'name': '30% profit → Lock 15%'},
        {'profit': 0.20, 'lock': 0.10, 'name': '20% profit → Lock 10%'},
        {'profit': 0.10, 'lock': 0.05, 'name': '10% profit → Lock 5%'},
        {'profit': 0.05, 'lock': 0.02, 'name': '5% profit → Breakeven'},
    ]
    
    @staticmethod
    def get_protection_level(profit_pct):
        """
        Get appropriate profit protection level
        """
        for level in ProfitProtection.PROTECTION_LEVELS:
            if profit_pct >= level['profit']:
                return level
        
        return None
    
    @staticmethod
    def calculate_protected_stop(entry_price, profit_pct):
        """
        Calculate stop loss that protects profit
        """
        level = ProfitProtection.get_protection_level(profit_pct)
        
        if level:
            return entry_price * (1 + level['lock'])
        else:
            return entry_price * 0.75  # Default -25% stop
