#!/usr/bin/env python3
"""
🎯 SIMPLIFIED HYBRID ALGO - Price Action + Best Indicators
Clean, simple, effective - Back to basics with smart enhancements
"""

from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import os
import pandas as pd
import json
import csv
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class SimplifiedHybridAlgo:
    def __init__(self, initial_capital=100000):
        self.api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/', 
                           websocket='wss://api.shoonya.com/NorenWSTP/')
        
        # Credentials
        self.user_id = os.getenv('SHOONYA_USER_ID')
        self.password = os.getenv('SHOONYA_PASSWORD')
        self.totp_key = os.getenv('SHOONYA_TOTP_KEY')
        self.vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
        self.api_secret = os.getenv('SHOONYA_API_SECRET')
        
        # Capital
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        
        # SIMPLIFIED PARAMETERS
        self.max_positions = 3
        self.stop_loss_pct = 0.25  # 25%
        self.target_profit_pct = 0.50  # 50%
        
        # Data Storage
        self.positions = []
        self.trade_history = []
        self.market_data = {}
        self.price_history = []
        self.last_nifty_price = 0
        
        # OHLC for indicators
        self.ohlc_5min = []
        
        # Files
        self.csv_file = f"simplified_trades_{datetime.now().strftime('%Y%m%d')}.csv"
        self.initialize_files()
    
    def initialize_files(self):
        """Initialize CSV file"""
        csv_headers = [
            'timestamp', 'trade_id', 'action', 'symbol', 'strike', 'option_type',
            'entry_price', 'exit_price', 'quantity', 'pnl', 'capital',
            'score', 'reason', 'nifty_level', 'strategy'
        ]
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)
    
    def login(self):
        """Login to Shoonya API"""
        totp = pyotp.TOTP(self.totp_key).now()
        
        try:
            result = self.api.login(
                userid=self.user_id,
                password=self.password,
                twoFA=totp,
                vendor_code=self.vendor_code,
                api_secret=self.api_secret,
                imei='abc1234'
            )
            
            if result and result.get('stat') == 'Ok':
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {result}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    # ========================================
    # SCORING SYSTEM - 100 POINTS TOTAL
    # ========================================
    
    def calculate_score(self, option_data):
        """
        Calculate simplified score (0-100)
        
        Breakdown:
        1. Price Action Trend (last 20 bars) - 25 points
        2. Candlestick Patterns - 25 points
        3. EMA Trend Confirmation - 15 points
        4. RSI Momentum (best for options) - 10 points
        5. Premium Quality (smart selection) - 15 points
        6. Liquidity - 10 points
        """
        
        score = 0
        reasons = []
        
        # ========================================
        # 1. PRICE ACTION TREND (25 points)
        # ========================================
        if len(self.price_history) >= 20:
            price_action_score, pa_reason = self.score_price_action_trend(option_data['option_type'])
            score += price_action_score
            if pa_reason:
                reasons.append(pa_reason)
        
        # ========================================
        # 2. CANDLESTICK PATTERNS (25 points)
        # ========================================
        if len(self.ohlc_5min) >= 3:
            candle_score, candle_reason = self.score_candlestick_patterns(option_data['option_type'])
            score += candle_score
            if candle_reason:
                reasons.append(candle_reason)
        
        # ========================================
        # 3. EMA TREND CONFIRMATION (15 points)
        # ========================================
        if len(self.ohlc_5min) >= 21:
            ema_score, ema_reason = self.score_ema_trend(option_data['option_type'])
            score += ema_score
            if ema_reason:
                reasons.append(ema_reason)
        
        # ========================================
        # 4. RSI MOMENTUM - BEST FOR OPTIONS (10 points)
        # ========================================
        if len(self.ohlc_5min) >= 14:
            rsi_score, rsi_reason = self.score_rsi_momentum(option_data['option_type'])
            score += rsi_score
            if rsi_reason:
                reasons.append(rsi_reason)
        
        # ========================================
        # 5. PREMIUM QUALITY - SMART SELECTION (15 points)
        # ========================================
        premium_score, premium_reason = self.score_premium_quality(
            option_data['ltp'],
            option_data['strike']
        )
        score += premium_score
        if premium_reason:
            reasons.append(premium_reason)
        
        # ========================================
        # 6. LIQUIDITY (10 points)
        # ========================================
        liquidity_score, liquidity_reason = self.score_liquidity(
            option_data['oi'],
            option_data['volume']
        )
        score += liquidity_score
        if liquidity_reason:
            reasons.append(liquidity_reason)
        
        return {
            'score': score,
            'reasons': reasons
        }
    
    # ========================================
    # 1. PRICE ACTION TREND (25 points)
    # ========================================
    
    def score_price_action_trend(self, option_type):
        """
        Score based on pure price action (last 20 bars)
        - Count up/down moves
        - Calculate momentum
        - Determine trend strength
        """
        
        recent_prices = [p['nifty'] for p in self.price_history[-20:]]
        
        # Count moves
        up_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
        down_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
        total_moves = up_moves + down_moves
        
        if total_moves == 0:
            return 0, None
        
        # Calculate momentum
        price_change = recent_prices[-1] - recent_prices[0]
        price_change_pct = (price_change / recent_prices[0] * 100) if recent_prices[0] > 0 else 0
        
        # Determine trend
        up_pct = up_moves / total_moves
        down_pct = down_moves / total_moves
        
        # Score based on alignment
        if option_type == 'CE':
            # For CE, we want bullish trend
            if up_pct >= 0.70:  # 70%+ up moves
                score = 25
                reason = f"🟢 Strong Bullish PA ({up_pct:.0%} up moves)"
            elif up_pct >= 0.60:  # 60%+ up moves
                score = 20
                reason = f"🟢 Bullish PA ({up_pct:.0%} up moves)"
            elif up_pct >= 0.55:  # 55%+ up moves
                score = 15
                reason = f"🟢 Moderate Bullish PA"
            else:
                score = 0
                reason = None  # Don't trade against trend
        else:  # PE
            # For PE, we want bearish trend
            if down_pct >= 0.70:  # 70%+ down moves
                score = 25
                reason = f"🔴 Strong Bearish PA ({down_pct:.0%} down moves)"
            elif down_pct >= 0.60:  # 60%+ down moves
                score = 20
                reason = f"🔴 Bearish PA ({down_pct:.0%} down moves)"
            elif down_pct >= 0.55:  # 55%+ down moves
                score = 15
                reason = f"🔴 Moderate Bearish PA"
            else:
                score = 0
                reason = None  # Don't trade against trend
        
        return score, reason
    
    # ========================================
    # 2. CANDLESTICK PATTERNS (25 points)
    # ========================================
    
    def score_candlestick_patterns(self, option_type):
        """
        Score based on candlestick patterns
        Focus on strongest reversal/continuation patterns
        """
        
        if len(self.ohlc_5min) < 3:
            return 0, None
        
        patterns = []
        candles = self.ohlc_5min[-3:]
        
        # Detect patterns
        patterns.extend(self.detect_engulfing(candles))
        patterns.extend(self.detect_marubozu(candles[-1]))
        patterns.extend(self.detect_hammer_hangman(candles[-1]))
        
        if not patterns:
            return 0, None
        
        # Score based on alignment with option type
        score = 0
        matching_patterns = []
        
        for pattern in patterns:
            if option_type == 'CE' and pattern['signal'] == 'BULLISH':
                score += pattern['strength']
                matching_patterns.append(pattern['name'])
            elif option_type == 'PE' and pattern['signal'] == 'BEARISH':
                score += pattern['strength']
                matching_patterns.append(pattern['name'])
        
        # Cap at 25 points
        score = min(25, score)
        
        if matching_patterns:
            reason = f"🕯️ {', '.join(matching_patterns[:2])}"
            return score, reason
        
        return 0, None
    
    def detect_engulfing(self, candles):
        """Detect bullish/bearish engulfing"""
        if len(candles) < 2:
            return []
        
        prev = candles[-2]
        curr = candles[-1]
        
        patterns = []
        
        # Bullish engulfing
        if (prev['close'] < prev['open'] and  # Previous bearish
            curr['close'] > curr['open'] and  # Current bullish
            curr['open'] < prev['close'] and  # Opens below prev close
            curr['close'] > prev['open']):    # Closes above prev open
            patterns.append({
                'name': 'Bullish Engulfing',
                'signal': 'BULLISH',
                'strength': 15
            })
        
        # Bearish engulfing
        if (prev['close'] > prev['open'] and  # Previous bullish
            curr['close'] < curr['open'] and  # Current bearish
            curr['open'] > prev['close'] and  # Opens above prev close
            curr['close'] < prev['open']):    # Closes below prev open
            patterns.append({
                'name': 'Bearish Engulfing',
                'signal': 'BEARISH',
                'strength': 15
            })
        
        return patterns
    
    def detect_marubozu(self, candle):
        """Detect marubozu (strong momentum candle)"""
        body = abs(candle['close'] - candle['open'])
        range_size = candle['high'] - candle['low']
        
        if range_size == 0:
            return []
        
        body_pct = body / range_size
        
        patterns = []
        
        if body_pct >= 0.90:  # 90%+ body
            if candle['close'] > candle['open']:
                patterns.append({
                    'name': 'Bullish Marubozu',
                    'signal': 'BULLISH',
                    'strength': 12
                })
            else:
                patterns.append({
                    'name': 'Bearish Marubozu',
                    'signal': 'BEARISH',
                    'strength': 12
                })
        
        return patterns
    
    def detect_hammer_hangman(self, candle):
        """Detect hammer (bullish) or hanging man (bearish)"""
        body = abs(candle['close'] - candle['open'])
        upper_shadow = candle['high'] - max(candle['open'], candle['close'])
        lower_shadow = min(candle['open'], candle['close']) - candle['low']
        
        patterns = []
        
        # Hammer (bullish reversal)
        if lower_shadow > body * 2 and upper_shadow < body * 0.5:
            patterns.append({
                'name': 'Hammer',
                'signal': 'BULLISH',
                'strength': 10
            })
        
        # Hanging Man (bearish reversal)
        if lower_shadow > body * 2 and upper_shadow < body * 0.5:
            patterns.append({
                'name': 'Hanging Man',
                'signal': 'BEARISH',
                'strength': 10
            })
        
        return patterns
    
    # ========================================
    # 3. EMA TREND CONFIRMATION (20 points)
    # ========================================
    
    def score_ema_trend(self, option_type):
        """
        Score based on EMA trend
        Using EMA 9 and EMA 21 (best for intraday)
        """
        
        if len(self.ohlc_5min) < 21:
            return 0, None
        
        closes = [c['close'] for c in self.ohlc_5min]
        current_price = closes[-1]
        
        # Calculate EMAs
        ema_9 = self.calculate_ema(closes, 9)
        ema_21 = self.calculate_ema(closes, 21)
        
        # Determine trend
        if current_price > ema_9 > ema_21:
            trend = 'STRONG_BULLISH'
            score_ce = 20
            score_pe = 0
            reason_ce = "📈 EMA: Strong Uptrend"
            reason_pe = None
        elif current_price > ema_9:
            trend = 'BULLISH'
            score_ce = 15
            score_pe = 0
            reason_ce = "📈 EMA: Uptrend"
            reason_pe = None
        elif current_price < ema_9 < ema_21:
            trend = 'STRONG_BEARISH'
            score_ce = 0
            score_pe = 20
            reason_ce = None
            reason_pe = "📉 EMA: Strong Downtrend"
        elif current_price < ema_9:
            trend = 'BEARISH'
            score_ce = 0
            score_pe = 15
            reason_ce = None
            reason_pe = "📉 EMA: Downtrend"
        else:
            trend = 'NEUTRAL'
            score_ce = 0
            score_pe = 0
            reason_ce = None
            reason_pe = None
        
        if option_type == 'CE':
            return score_ce, reason_ce
        else:
            return score_pe, reason_pe
    
    def calculate_ema(self, data, period):
        """Calculate EMA"""
        if len(data) < period:
            return data[-1] if data else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(data[:period]) / period
        
        for price in data[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    # ========================================
    # 4. RSI MOMENTUM - BEST FOR OPTIONS (10 points)
    # ========================================
    
    def score_rsi_momentum(self, option_type):
        """
        Score based on RSI (14 period)
        RSI is BEST for options because:
        - Shows overbought/oversold (reversal opportunities)
        - Works well in trending AND ranging markets
        - Simple and reliable
        """
        
        if len(self.ohlc_5min) < 14:
            return 0, None
        
        closes = [c['close'] for c in self.ohlc_5min]
        rsi = self.calculate_rsi(closes, 14)
        
        # Score based on RSI zones
        if option_type == 'CE':
            # For CE, we want oversold (bounce up opportunity)
            if rsi <= 30:  # Oversold
                score = 10
                reason = f"📊 RSI: Oversold ({rsi:.0f})"
            elif 30 < rsi <= 40:  # Near oversold
                score = 7
                reason = f"📊 RSI: Near Oversold ({rsi:.0f})"
            elif 40 < rsi <= 60:  # Neutral momentum
                score = 5
                reason = f"📊 RSI: Neutral ({rsi:.0f})"
            else:  # Overbought (not good for CE)
                score = 0
                reason = None
        else:  # PE
            # For PE, we want overbought (drop down opportunity)
            if rsi >= 70:  # Overbought
                score = 10
                reason = f"📊 RSI: Overbought ({rsi:.0f})"
            elif 60 <= rsi < 70:  # Near overbought
                score = 7
                reason = f"📊 RSI: Near Overbought ({rsi:.0f})"
            elif 40 <= rsi < 60:  # Neutral momentum
                score = 5
                reason = f"📊 RSI: Neutral ({rsi:.0f})"
            else:  # Oversold (not good for PE)
                score = 0
                reason = None
        
        return score, reason
    
    def calculate_rsi(self, data, period=14):
        """Calculate RSI"""
        if len(data) < period + 1:
            return 50
        
        deltas = [data[i] - data[i-1] for i in range(1, len(data))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    # ========================================
    # 4. PREMIUM QUALITY - SMART SELECTION (15 points)
    # ========================================
    
    def score_premium_quality(self, ltp, strike):
        """
        Smart premium selection based on market level
        - ATM options: ₹40-80 (high delta, good movement)
        - Near ATM: ₹20-40 (balanced risk/reward)
        - OTM: ₹10-20 (cheap, high leverage)
        """
        
        distance = abs(strike - self.last_nifty_price)
        
        # Determine optimal premium range based on distance
        if distance <= 50:  # ATM (within 50 points)
            optimal_min = 40
            optimal_max = 80
            category = "ATM"
        elif distance <= 150:  # Near ATM (50-150 points)
            optimal_min = 20
            optimal_max = 40
            category = "Near-ATM"
        elif distance <= 300:  # OTM (150-300 points)
            optimal_min = 10
            optimal_max = 20
            category = "OTM"
        else:  # Far OTM (>300 points)
            return 0, None  # Don't trade far OTM
        
        # Score based on how close to optimal range
        if optimal_min <= ltp <= optimal_max:
            score = 15
            reason = f"💰 Optimal {category} premium: ₹{ltp:.0f}"
        elif optimal_min * 0.8 <= ltp <= optimal_max * 1.2:
            score = 10
            reason = f"💰 Good {category} premium: ₹{ltp:.0f}"
        elif optimal_min * 0.6 <= ltp <= optimal_max * 1.4:
            score = 5
            reason = f"💰 Acceptable {category} premium: ₹{ltp:.0f}"
        else:
            score = 0
            reason = None  # Premium not suitable
        
        return score, reason
    
    # ========================================
    # 5. LIQUIDITY (15 points)
    # ========================================
    
    def score_liquidity(self, oi, volume):
        """
        Score based on liquidity
        - OI: Minimum 1L (100,000)
        - Volume: Minimum 500
        """
        
        score = 0
        reasons = []
        
        # OI score (7 points max)
        if oi >= 500000:  # 5L+
            oi_score = 7
            reasons.append(f"OI: {oi/100000:.1f}L")
        elif oi >= 200000:  # 2L+
            oi_score = 5
            reasons.append(f"OI: {oi/100000:.1f}L")
        elif oi >= 100000:  # 1L+
            oi_score = 3
            reasons.append(f"OI: {oi/100000:.1f}L")
        else:
            return 0, None  # Insufficient liquidity
        
        # Volume score (3 points max)
        if volume >= 5000:
            vol_score = 3
        elif volume >= 1000:
            vol_score = 2
        elif volume >= 500:
            vol_score = 1
        else:
            return 0, None  # Insufficient volume
        
        score = oi_score + vol_score
        reason = f"📊 {', '.join(reasons)}"
        
        return score, reason
    
    # ========================================
    # MARKET CONDITION FILTER
    # ========================================
    
    def check_market_condition(self):
        """
        Check if market is suitable for trading
        Returns: (allow_trading, reason)
        """
        
        if len(self.price_history) < 20:
            return False, "Insufficient data (need 20+ bars)"
        
        recent_prices = [p['nifty'] for p in self.price_history[-20:]]
        
        # Calculate volatility
        price_range = max(recent_prices) - min(recent_prices)
        avg_price = sum(recent_prices) / len(recent_prices)
        volatility_pct = (price_range / avg_price * 100) if avg_price > 0 else 0
        
        # Count moves
        up_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
        down_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
        total_moves = up_moves + down_moves
        
        if total_moves == 0:
            return False, "No price movement"
        
        # Calculate trend consistency
        consistency = max(up_moves, down_moves) / total_moves
        
        # Determine market condition
        if volatility_pct > 1.5:
            return False, f"Too volatile ({volatility_pct:.1f}%)"
        elif consistency < 0.55:
            return False, f"Choppy market (consistency: {consistency:.0%})"
        else:
            return True, f"Good market (consistency: {consistency:.0%}, volatility: {volatility_pct:.1f}%)"
    
    # ========================================
    # MAIN TRADING LOGIC
    # ========================================
    
    def find_opportunities(self):
        """Find trading opportunities with simplified scoring"""
        
        # Check market condition first
        allow_trading, condition_reason = self.check_market_condition()
        
        if not allow_trading:
            print(f"🚫 SITTING OUT: {condition_reason}")
            return []
        
        print(f"✅ MARKET CONDITION: {condition_reason}")
        
        opportunities = []
        
        for symbol, data in self.market_data.items():
            # Calculate score
            score_data = self.calculate_score(data)
            
            # Only consider scores >= 70
            if score_data['score'] >= 70:
                opportunities.append({
                    'data': data,
                    'score': score_data['score'],
                    'reasons': score_data['reasons']
                })
        
        # Sort by score
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        
        if opportunities:
            print(f"\n🎯 Found {len(opportunities)} opportunities (score >= 70):")
            for i, opp in enumerate(opportunities[:5], 1):
                print(f"   {i}. {opp['data']['symbol']} @ ₹{opp['data']['ltp']:.2f}")
                print(f"      Score: {opp['score']}/100")
                print(f"      {' | '.join(opp['reasons'])}")
        
        # Return top 3
        return opportunities[:3]
    
    def run(self):
        """Main trading loop"""
        print("🚀 Starting Simplified Hybrid Algo...")
        print("=" * 80)
        
        if not self.login():
            return
        
        print("\n📊 Algo Configuration:")
        print(f"   Scoring: Price Action (50%) + EMA (20%) + Premium (15%) + Liquidity (15%)")
        print(f"   Min Score: 70/100")
        print(f"   Market Filter: Sits out choppy/volatile markets")
        print(f"   Capital: ₹{self.current_capital:,.0f}")
        print("=" * 80)
        
        # Main loop would go here
        # For now, this is the framework
        
        print("\n✅ Algo ready to trade!")

if __name__ == "__main__":
    algo = SimplifiedHybridAlgo()
    algo.run()
