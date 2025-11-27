#!/usr/bin/env python3
"""
🎯 ADAPTIVE MARKET ENGINE
Intelligently adapts trading strategy based on market conditions

This is the "brain" that makes the algorithm smart
"""

import numpy as np
from datetime import datetime

class AdaptiveMarketEngine:
    """
    Smart engine that:
    1. Detects market condition (TRENDING/RANGING/CHOPPY/VOLATILE)
    2. Selects appropriate strategy
    3. Determines position size
    4. Sets trade limits
    5. Decides when to sit out
    """
    
    def __init__(self):
        self.current_mode = None
        self.mode_history = []
        self.trades_today = 0
        self.daily_pnl = 0
        
    def analyze_and_adapt(self, price_history, indicators_5min, indicators_15min, current_capital):
        """
        Main function: Analyzes market and returns adaptive parameters
        
        Returns: {
            'mode': 'TRENDING' | 'RANGING' | 'CHOPPY' | 'VOLATILE',
            'confidence': 0-100,
            'allow_trading': bool,
            'max_trades': int,
            'position_size': int (lots),
            'strategy': str,
            'stop_loss_pct': float,
            'target_pct': float,
            'reason': str
        }
        """
        
        if len(price_history) < 20:
            return self._insufficient_data_mode()
        
        # Step 1: Detect market condition
        market_condition = self._detect_market_condition(
            price_history, 
            indicators_5min, 
            indicators_15min
        )
        
        # Step 2: Determine if we should trade
        should_trade = self._should_trade(market_condition, current_capital)
        
        # Step 3: Select strategy and parameters
        if should_trade:
            params = self._get_mode_parameters(market_condition)
        else:
            params = self._get_sit_out_parameters(market_condition)
        
        # Store mode
        self.current_mode = params['mode']
        self.mode_history.append({
            'timestamp': datetime.now(),
            'mode': params['mode'],
            'confidence': params['confidence']
        })
        
        # Keep last 50 records
        if len(self.mode_history) > 50:
            self.mode_history = self.mode_history[-50:]
        
        return params
    
    def _detect_market_condition(self, price_history, indicators_5min, indicators_15min):
        """
        Detects current market condition using multiple factors
        """
        
        prices = [p['nifty'] for p in price_history[-20:]]
        
        # 1. Calculate ADX (trend strength)
        adx = self._calculate_adx(price_history[-20:])
        
        # 2. Calculate volatility
        volatility = np.std(prices) / np.mean(prices) * 100
        
        # 3. Calculate trend consistency
        up_moves = sum(1 for i in range(1, len(prices)) if prices[i] > prices[i-1])
        down_moves = sum(1 for i in range(1, len(prices)) if prices[i] < prices[i-1])
        total_moves = up_moves + down_moves
        trend_consistency = max(up_moves, down_moves) / total_moves if total_moves > 0 else 0
        
        # 4. Calculate price range
        price_range = (max(prices) - min(prices)) / min(prices) * 100
        
        # 5. Get indicator trends
        trend_5min = indicators_5min.get('trend', 'NEUTRAL') if indicators_5min else 'NEUTRAL'
        trend_15min = indicators_15min.get('trend', 'NEUTRAL') if indicators_15min else 'NEUTRAL'
        
        # 6. Determine market condition
        condition = self._classify_market(
            adx, volatility, trend_consistency, price_range, 
            trend_5min, trend_15min
        )
        
        return condition
    
    def _classify_market(self, adx, volatility, trend_consistency, price_range, trend_5min, trend_15min):
        """
        Classifies market into one of 4 modes
        """
        
        # VOLATILE: High volatility overrides everything
        if volatility > 1.5:
            return {
                'mode': 'VOLATILE',
                'confidence': min(100, volatility * 50),
                'adx': adx,
                'volatility': volatility,
                'trend_consistency': trend_consistency,
                'price_range': price_range
            }
        
        # TRENDING: Strong directional movement
        if adx > 25 and trend_consistency > 0.65 and price_range > 0.3:
            # Determine direction
            if trend_5min == 'BULLISH' and trend_15min == 'BULLISH':
                direction = 'UP'
            elif trend_5min == 'BEARISH' and trend_15min == 'BEARISH':
                direction = 'DOWN'
            else:
                direction = 'MIXED'
            
            return {
                'mode': 'TRENDING',
                'direction': direction,
                'confidence': min(100, adx * 3),
                'adx': adx,
                'volatility': volatility,
                'trend_consistency': trend_consistency,
                'price_range': price_range
            }
        
        # CHOPPY: Low trend strength, inconsistent
        if adx < 20 and trend_consistency < 0.55:
            return {
                'mode': 'CHOPPY',
                'confidence': 100 - (adx * 4),
                'adx': adx,
                'volatility': volatility,
                'trend_consistency': trend_consistency,
                'price_range': price_range
            }
        
        # RANGING: Default - sideways movement
        return {
            'mode': 'RANGING',
            'confidence': 70,
            'adx': adx,
            'volatility': volatility,
            'trend_consistency': trend_consistency,
            'price_range': price_range
        }
    
    def _should_trade(self, market_condition, current_capital):
        """
        Decides if we should trade based on market condition and capital
        """
        
        mode = market_condition['mode']
        confidence = market_condition['confidence']
        
        # Never trade in choppy markets
        if mode == 'CHOPPY':
            return False
        
        # Be cautious in volatile markets
        if mode == 'VOLATILE' and confidence > 80:
            return False
        
        # Check capital (stop if down >20%)
        if current_capital < 80000:  # Down 20% from 100K
            return False
        
        return True
    
    def _get_mode_parameters(self, market_condition):
        """
        Returns trading parameters for each market mode
        """
        
        mode = market_condition['mode']
        confidence = market_condition['confidence']
        
        if mode == 'TRENDING':
            return {
                'mode': 'TRENDING',
                'confidence': confidence,
                'allow_trading': True,
                'max_trades': 8,
                'position_size': 300,  # Full size in trending
                'strategy': 'TREND_FOLLOWING',
                'stop_loss_pct': 0.20,  # 20% stop
                'target_pct': 0.50,  # 50% target
                'reason': f"Strong trend (ADX: {market_condition['adx']:.1f}, Consistency: {market_condition['trend_consistency']:.1%})",
                'direction': market_condition.get('direction', 'MIXED')
            }
        
        elif mode == 'RANGING':
            return {
                'mode': 'RANGING',
                'confidence': confidence,
                'allow_trading': True,
                'max_trades': 12,
                'position_size': 225,  # 75% size in ranging
                'strategy': 'MEAN_REVERSION',
                'stop_loss_pct': 0.25,  # 25% stop
                'target_pct': 0.40,  # 40% target
                'reason': f"Range-bound market (Range: {market_condition['price_range']:.2f}%)"
            }
        
        elif mode == 'VOLATILE':
            return {
                'mode': 'VOLATILE',
                'confidence': confidence,
                'allow_trading': True,
                'max_trades': 5,
                'position_size': 150,  # 50% size in volatile
                'strategy': 'REDUCED_RISK',
                'stop_loss_pct': 0.30,  # 30% stop (wider)
                'target_pct': 0.35,  # 35% target (smaller)
                'reason': f"High volatility ({market_condition['volatility']:.2f}%) - Reduced risk"
            }
        
        else:
            return self._get_sit_out_parameters(market_condition)
    
    def _get_sit_out_parameters(self, market_condition):
        """
        Returns parameters for sitting out (no trading)
        """
        
        return {
            'mode': market_condition['mode'],
            'confidence': market_condition['confidence'],
            'allow_trading': False,
            'max_trades': 0,
            'position_size': 0,
            'strategy': 'SIT_OUT',
            'stop_loss_pct': 0,
            'target_pct': 0,
            'reason': f"Unfavorable conditions - Sitting out (ADX: {market_condition.get('adx', 0):.1f})"
        }
    
    def _insufficient_data_mode(self):
        """
        Returns safe parameters when insufficient data
        """
        
        return {
            'mode': 'INSUFFICIENT_DATA',
            'confidence': 0,
            'allow_trading': False,
            'max_trades': 0,
            'position_size': 0,
            'strategy': 'WAIT',
            'stop_loss_pct': 0,
            'target_pct': 0,
            'reason': 'Insufficient data - Building history'
        }
    
    def _calculate_adx(self, ohlc_data, period=14):
        """Calculate ADX for trend strength"""
        
        if len(ohlc_data) < period + 1:
            return 20
        
        try:
            tr_list = []
            plus_dm_list = []
            minus_dm_list = []
            
            for i in range(1, len(ohlc_data)):
                high = ohlc_data[i].get('nifty', 0)
                low = ohlc_data[i].get('nifty', 0)
                prev_high = ohlc_data[i-1].get('nifty', 0)
                prev_low = ohlc_data[i-1].get('nifty', 0)
                prev_close = ohlc_data[i-1].get('nifty', 0)
                
                tr1 = high - low
                tr2 = abs(high - prev_close)
                tr3 = abs(low - prev_close)
                tr = max(tr1, tr2, tr3)
                tr_list.append(tr)
                
                plus_dm = max(high - prev_high, 0) if (high - prev_high) > (prev_low - low) else 0
                minus_dm = max(prev_low - low, 0) if (prev_low - low) > (high - prev_high) else 0
                
                plus_dm_list.append(plus_dm)
                minus_dm_list.append(minus_dm)
            
            if len(tr_list) < period:
                return 20
            
            atr = np.mean(tr_list[-period:])
            plus_di = (np.mean(plus_dm_list[-period:]) / atr * 100) if atr > 0 else 0
            minus_di = (np.mean(minus_dm_list[-period:]) / atr * 100) if atr > 0 else 0
            
            dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
            
            return dx
            
        except Exception as e:
            return 20
    
    def update_trade_count(self):
        """Increment trade counter"""
        self.trades_today += 1
    
    def reset_daily_counters(self):
        """Reset counters at start of day"""
        self.trades_today = 0
        self.daily_pnl = 0
    
    def can_take_more_trades(self, max_trades):
        """Check if we can take more trades"""
        return self.trades_today < max_trades
    
    def get_current_mode_summary(self):
        """Get summary of current mode"""
        if not self.current_mode:
            return "No mode detected yet"
        
        return f"Current Mode: {self.current_mode} | Trades Today: {self.trades_today}"
