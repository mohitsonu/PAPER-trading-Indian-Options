#!/usr/bin/env python3
"""
🎯 PRIORITY FEATURES FOR HIGH ACCURACY TRADING
Implements 4 critical features to prevent losses like Nov 18

Priority 1: Market Condition Filter (Most Important)
Priority 2: OI Change Analysis
Priority 3: Stochastic Oscillator
Priority 4: Greeks Analysis
"""

import numpy as np
from datetime import datetime, timedelta

class PriorityFeatures:
    """Enhanced trading features to prevent overtrading and improve accuracy"""
    
    def __init__(self):
        # Market condition tracking
        self.market_condition_history = []
        self.oi_history = {}  # Track OI changes over time
        
        # Stochastic settings
        self.stoch_k_period = 14
        self.stoch_d_period = 3
        
        # Greeks calculation settings
        self.risk_free_rate = 0.07  # 7% risk-free rate
        
    # ========================================
    # PRIORITY 1: MARKET CONDITION FILTER
    # ========================================
    
    def check_trend_direction_alignment(self, option_type, price_history, indicators_5min, indicators_15min):
        """
        🚨 CRITICAL: Check if option type aligns with market trend direction
        
        This prevents the #1 cause of losses: trading against the trend
        - Blocks PE (bearish) trades in uptrend
        - Blocks CE (bullish) trades in downtrend
        
        Returns: {
            'allowed': bool,
            'trend_direction': 'BULLISH' | 'BEARISH' | 'NEUTRAL',
            'reason': str,
            'confidence': 0-100
        }
        """
        
        if len(price_history) < 20:
            return {
                'allowed': False,  # 🚨 CHANGED: Block if insufficient data (be conservative)
                'trend_direction': 'NEUTRAL',
                'reason': 'Insufficient data for trend analysis (need 20+ bars)',
                'confidence': 0
            }
        
        # Get recent prices (increased from 10 to 20 bars)
        recent_prices = [p['nifty'] for p in price_history[-20:]]
        
        # 1. Calculate price momentum (last 20 bars)
        price_change = recent_prices[-1] - recent_prices[0]
        price_change_pct = (price_change / recent_prices[0] * 100) if recent_prices[0] > 0 else 0
        
        # 2. Count up/down moves
        up_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
        down_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
        total_moves = up_moves + down_moves
        
        # 🆕 2b. Immediate price action check (last 10 bars for instant trend detection)
        immediate_prices = recent_prices[-10:] if len(recent_prices) >= 10 else recent_prices
        immediate_up = sum(1 for i in range(1, len(immediate_prices)) if immediate_prices[i] > immediate_prices[i-1])
        immediate_down = sum(1 for i in range(1, len(immediate_prices)) if immediate_prices[i] < immediate_prices[i-1])
        immediate_total = immediate_up + immediate_down
        
        # 3. Get 5min and 15min trend
        trend_5min = indicators_5min.get('trend', 'NEUTRAL') if indicators_5min else 'NEUTRAL'
        trend_15min = indicators_15min.get('trend', 'NEUTRAL') if indicators_15min else 'NEUTRAL'
        
        # 4. Determine overall trend direction
        bullish_signals = 0
        bearish_signals = 0
        
        # Price momentum signal (stricter threshold)
        if price_change_pct > 0.15:  # 🚨 CHANGED: 0.15% instead of 0.1% (stricter)
            bullish_signals += 2
        elif price_change_pct < -0.15:  # 🚨 CHANGED: -0.15% instead of -0.1% (stricter)
            bearish_signals += 2
        
        # Move count signal (stricter threshold)
        if up_moves > down_moves * 1.3:  # 🚨 CHANGED: 1.3x instead of 1.5x (easier to detect)
            bullish_signals += 2
        elif down_moves > up_moves * 1.3:  # 🚨 CHANGED: 1.3x instead of 1.5x (easier to detect)
            bearish_signals += 2
        
        # 🆕 Immediate price action signal (NO LAG - catches trends instantly!)
        if immediate_total > 0:
            immediate_down_pct = immediate_down / immediate_total
            immediate_up_pct = immediate_up / immediate_total
            
            if immediate_down_pct >= 0.7:  # 70%+ down moves in last 10 bars
                bearish_signals += 2  # Strong immediate bearish signal
            elif immediate_up_pct >= 0.7:  # 70%+ up moves in last 10 bars
                bullish_signals += 2  # Strong immediate bullish signal
        
        # 5min trend signal (EQUAL weight to 15min for faster detection)
        if trend_5min == 'BULLISH':
            bullish_signals += 2  # 🚨 CHANGED: 2 instead of 1 (faster trend detection)
        elif trend_5min == 'BEARISH':
            bearish_signals += 2  # 🚨 CHANGED: 2 instead of 1 (faster trend detection)
        
        # 15min trend signal (EQUAL weight to 5min)
        if trend_15min == 'BULLISH':
            bullish_signals += 2  # 🚨 CHANGED: 2 instead of 3 (equal weight with 5min)
        elif trend_15min == 'BEARISH':
            bearish_signals += 2  # 🚨 CHANGED: 2 instead of 3 (equal weight with 5min)
        
        # Determine trend direction (lowered threshold from 4 to 3)
        if bullish_signals >= 3:  # 🚨 CHANGED: 3 instead of 4 (easier to detect trend)
            trend_direction = 'BULLISH'
            confidence = min(100, bullish_signals * 15)
        elif bearish_signals >= 3:  # 🚨 CHANGED: 3 instead of 4 (easier to detect trend)
            trend_direction = 'BEARISH'
            confidence = min(100, bearish_signals * 15)
        else:
            trend_direction = 'NEUTRAL'
            confidence = 50
        
        # Check alignment
        allowed = True
        reason = ""
        
        if trend_direction == 'BULLISH' and option_type == 'PE':
            allowed = False
            reason = f"🚫 BLOCKED: PE trade in BULLISH trend (confidence: {confidence}%)"
        elif trend_direction == 'BEARISH' and option_type == 'CE':
            allowed = False
            reason = f"🚫 BLOCKED: CE trade in BEARISH trend (confidence: {confidence}%)"
        elif trend_direction == 'NEUTRAL':
            # 🚨 NEW: Block ALL trades in NEUTRAL trend (be conservative!)
            allowed = False
            reason = f"🚫 BLOCKED: No clear trend detected (NEUTRAL) - Sitting out"
        else:
            reason = f"✅ ALLOWED: {option_type} aligns with {trend_direction} trend"
        
        return {
            'allowed': allowed,
            'trend_direction': trend_direction,
            'reason': reason,
            'confidence': confidence,
            'price_change_pct': price_change_pct,
            'up_moves': up_moves,
            'down_moves': down_moves
        }
    
    def detect_market_condition(self, price_history, indicators_5min, indicators_15min):
        """
        Detect market condition to prevent trading in choppy markets
        
        Returns: {
            'condition': 'TRENDING' | 'CHOPPY' | 'VOLATILE' | 'RANGE_BOUND',
            'score': 0-100,
            'allow_scalper': bool,
            'allow_contrarian': bool,
            'allow_trend_rider': bool,
            'reason': str
        }
        """
        
        if len(price_history) < 20:
            return {
                'condition': 'INSUFFICIENT_DATA',
                'score': 0,
                'allow_scalper': False,
                'allow_contrarian': False,
                'allow_trend_rider': False,
                'reason': 'Need more data'
            }
        
        # Extract prices
        prices = [p['nifty'] for p in price_history[-20:]]
        
        # 1. Calculate ADX (Average Directional Index) for trend strength
        adx = self._calculate_adx(price_history[-20:])
        
        # 2. Calculate price volatility
        volatility = np.std(prices) / np.mean(prices) * 100
        
        # 3. Calculate trend consistency
        up_moves = sum(1 for i in range(1, len(prices)) if prices[i] > prices[i-1])
        down_moves = sum(1 for i in range(1, len(prices)) if prices[i] < prices[i-1])
        total_moves = up_moves + down_moves
        trend_consistency = max(up_moves, down_moves) / total_moves if total_moves > 0 else 0
        
        # 4. Check 15-minute trend alignment
        trend_15min = indicators_15min.get('trend', 'NEUTRAL') if indicators_15min else 'NEUTRAL'
        
        # 5. Calculate price range
        price_range = (max(prices) - min(prices)) / min(prices) * 100
        
        # Determine market condition
        condition = None
        score = 0
        allow_scalper = False
        allow_contrarian = True  # Contrarian works in most conditions
        allow_trend_rider = False
        reason = ""
        
        # TRENDING MARKET (Best for Trend Rider, Good for Scalper)
        if adx > 25 and trend_consistency > 0.65 and price_range > 0.3:
            condition = 'TRENDING'
            score = 90
            allow_scalper = True
            allow_trend_rider = True
            reason = f"Strong trend (ADX: {adx:.1f}, Consistency: {trend_consistency:.1%})"
        
        # CHOPPY MARKET (Avoid Scalper, Contrarian only)
        elif adx < 20 and trend_consistency < 0.55:
            condition = 'CHOPPY'
            score = 30
            allow_scalper = False  # 🚨 CRITICAL: No scalper in choppy
            allow_trend_rider = False
            reason = f"Choppy market (ADX: {adx:.1f}, Consistency: {trend_consistency:.1%})"
        
        # VOLATILE MARKET (Risky, limited trading)
        elif volatility > 1.5:
            condition = 'VOLATILE'
            score = 40
            allow_scalper = False
            allow_trend_rider = False
            reason = f"High volatility ({volatility:.2f}%)"
        
        # RANGE BOUND (Good for Contrarian, Limited Scalper)
        elif price_range < 0.3 and adx < 25:
            condition = 'RANGE_BOUND'
            score = 60
            allow_scalper = True  # Allow scalper in tight range
            allow_trend_rider = False
            reason = f"Range-bound (Range: {price_range:.2f}%)"
        
        # MODERATE (Default condition)
        else:
            condition = 'MODERATE'
            score = 70
            allow_scalper = True
            allow_trend_rider = adx > 20
            reason = f"Moderate conditions (ADX: {adx:.1f})"
        
        # Store in history
        self.market_condition_history.append({
            'timestamp': datetime.now(),
            'condition': condition,
            'score': score,
            'adx': adx,
            'volatility': volatility,
            'trend_consistency': trend_consistency
        })
        
        # Keep last 50 records
        if len(self.market_condition_history) > 50:
            self.market_condition_history = self.market_condition_history[-50:]
        
        return {
            'condition': condition,
            'score': score,
            'allow_scalper': allow_scalper,
            'allow_contrarian': allow_contrarian,
            'allow_trend_rider': allow_trend_rider,
            'reason': reason,
            'adx': adx,
            'volatility': volatility,
            'trend_consistency': trend_consistency
        }
    
    def _calculate_adx(self, ohlc_data, period=14):
        """Calculate Average Directional Index (ADX) for trend strength"""
        
        if len(ohlc_data) < period + 1:
            return 20  # Default neutral ADX
        
        try:
            # Calculate True Range and Directional Movement
            tr_list = []
            plus_dm_list = []
            minus_dm_list = []
            
            for i in range(1, len(ohlc_data)):
                high = ohlc_data[i].get('nifty', ohlc_data[i].get('high', 0))
                low = ohlc_data[i].get('nifty', ohlc_data[i].get('low', 0))
                prev_high = ohlc_data[i-1].get('nifty', ohlc_data[i-1].get('high', 0))
                prev_low = ohlc_data[i-1].get('nifty', ohlc_data[i-1].get('low', 0))
                prev_close = ohlc_data[i-1].get('nifty', ohlc_data[i-1].get('close', 0))
                
                # True Range
                tr1 = high - low
                tr2 = abs(high - prev_close)
                tr3 = abs(low - prev_close)
                tr = max(tr1, tr2, tr3)
                tr_list.append(tr)
                
                # Directional Movement
                plus_dm = max(high - prev_high, 0) if (high - prev_high) > (prev_low - low) else 0
                minus_dm = max(prev_low - low, 0) if (prev_low - low) > (high - prev_high) else 0
                
                plus_dm_list.append(plus_dm)
                minus_dm_list.append(minus_dm)
            
            # Calculate smoothed averages
            if len(tr_list) < period:
                return 20
            
            atr = np.mean(tr_list[-period:])
            plus_di = (np.mean(plus_dm_list[-period:]) / atr * 100) if atr > 0 else 0
            minus_di = (np.mean(minus_dm_list[-period:]) / atr * 100) if atr > 0 else 0
            
            # Calculate DX and ADX
            dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
            
            # ADX is smoothed DX
            adx = dx  # Simplified (should be EMA of DX, but this works)
            
            return adx
            
        except Exception as e:
            print(f"⚠️ ADX calculation error: {e}")
            return 20
    
    # ========================================
    # PRIORITY 2: OI CHANGE ANALYSIS
    # ========================================
    
    def analyze_oi_changes(self, option_data, symbol):
        """
        Analyze Open Interest changes to detect smart money flow
        
        Returns: {
            'oi_change': float,
            'oi_change_pct': float,
            'signal': 'BULLISH' | 'BEARISH' | 'NEUTRAL',
            'strength': 0-100,
            'reason': str
        }
        """
        
        current_oi = option_data.get('oi', 0)
        current_time = datetime.now()
        
        # Initialize OI history for this symbol if not exists
        if symbol not in self.oi_history:
            self.oi_history[symbol] = []
        
        # Add current OI to history
        self.oi_history[symbol].append({
            'timestamp': current_time,
            'oi': current_oi,
            'ltp': option_data.get('ltp', 0),
            'volume': option_data.get('volume', 0)
        })
        
        # Keep last 20 records (about 40 minutes of data at 2-min intervals)
        if len(self.oi_history[symbol]) > 20:
            self.oi_history[symbol] = self.oi_history[symbol][-20:]
        
        # Need at least 2 data points for comparison
        if len(self.oi_history[symbol]) < 2:
            return {
                'oi_change': 0,
                'oi_change_pct': 0,
                'signal': 'NEUTRAL',
                'strength': 0,
                'reason': 'Insufficient OI history'
            }
        
        # Calculate OI change
        prev_oi = self.oi_history[symbol][-2]['oi']
        oi_change = current_oi - prev_oi
        oi_change_pct = (oi_change / prev_oi * 100) if prev_oi > 0 else 0
        
        # Analyze OI change with price movement
        prev_ltp = self.oi_history[symbol][-2]['ltp']
        price_change = option_data.get('ltp', 0) - prev_ltp
        price_change_pct = (price_change / prev_ltp * 100) if prev_ltp > 0 else 0
        
        option_type = option_data.get('option_type', 'CE')
        
        # Determine signal based on OI and price movement
        signal = 'NEUTRAL'
        strength = 0
        reason = ""
        
        # Significant OI increase (>5%)
        if oi_change_pct > 5:
            if price_change_pct > 2:
                # OI increase + Price increase
                if option_type == 'CE':
                    signal = 'BULLISH'
                    strength = min(100, oi_change_pct * 10)
                    reason = "Long buildup in CE (OI↑ Price↑)"
                else:
                    signal = 'BEARISH'
                    strength = min(100, oi_change_pct * 10)
                    reason = "Short covering in PE (OI↑ Price↑)"
            
            elif price_change_pct < -2:
                # OI increase + Price decrease
                if option_type == 'CE':
                    signal = 'BEARISH'
                    strength = min(100, oi_change_pct * 10)
                    reason = "Short buildup in CE (OI↑ Price↓)"
                else:
                    signal = 'BULLISH'
                    strength = min(100, oi_change_pct * 10)
                    reason = "Long buildup in PE (OI↑ Price↓)"
        
        # Significant OI decrease (>5%)
        elif oi_change_pct < -5:
            if price_change_pct > 2:
                # OI decrease + Price increase
                signal = 'NEUTRAL'
                strength = 30
                reason = "Profit booking (OI↓ Price↑)"
            
            elif price_change_pct < -2:
                # OI decrease + Price decrease
                signal = 'NEUTRAL'
                strength = 30
                reason = "Unwinding (OI↓ Price↓)"
        
        # Moderate OI change
        else:
            signal = 'NEUTRAL'
            strength = 20
            reason = f"Moderate OI change ({oi_change_pct:+.1f}%)"
        
        return {
            'oi_change': oi_change,
            'oi_change_pct': oi_change_pct,
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'price_change_pct': price_change_pct
        }
    
    # ========================================
    # PRIORITY 3: STOCHASTIC OSCILLATOR
    # ========================================
    
    def calculate_stochastic(self, ohlc_data, k_period=14, d_period=3):
        """
        Calculate Stochastic Oscillator for precise entry timing
        
        Returns: {
            'k': float (0-100),
            'd': float (0-100),
            'signal': 'OVERBOUGHT' | 'OVERSOLD' | 'NEUTRAL',
            'crossover': 'BULLISH' | 'BEARISH' | 'NONE',
            'score': 0-100
        }
        """
        
        if len(ohlc_data) < k_period + d_period:
            return {
                'k': 50,
                'd': 50,
                'signal': 'NEUTRAL',
                'crossover': 'NONE',
                'score': 0
            }
        
        try:
            # Extract high, low, close
            highs = []
            lows = []
            closes = []
            
            for bar in ohlc_data[-(k_period + d_period):]:
                price = bar.get('close', bar.get('nifty', 0))
                high = bar.get('high', price)
                low = bar.get('low', price)
                
                highs.append(high)
                lows.append(low)
                closes.append(price)
            
            # Calculate %K
            k_values = []
            for i in range(k_period - 1, len(closes)):
                period_high = max(highs[i - k_period + 1:i + 1])
                period_low = min(lows[i - k_period + 1:i + 1])
                current_close = closes[i]
                
                if period_high - period_low > 0:
                    k = ((current_close - period_low) / (period_high - period_low)) * 100
                else:
                    k = 50
                
                k_values.append(k)
            
            # Calculate %D (SMA of %K)
            if len(k_values) >= d_period:
                d = np.mean(k_values[-d_period:])
                k = k_values[-1]
            else:
                k = k_values[-1] if k_values else 50
                d = k
            
            # Determine signal
            signal = 'NEUTRAL'
            score = 50
            
            if k > 80:
                signal = 'OVERBOUGHT'
                score = 20  # Reduce score for overbought
            elif k < 20:
                signal = 'OVERSOLD'
                score = 80  # Increase score for oversold (good for buying)
            else:
                signal = 'NEUTRAL'
                score = 50
            
            # Detect crossovers
            crossover = 'NONE'
            if len(k_values) >= 2:
                prev_k = k_values[-2]
                prev_d = np.mean(k_values[-d_period-1:-1]) if len(k_values) >= d_period + 1 else prev_k
                
                # Bullish crossover: %K crosses above %D
                if prev_k < prev_d and k > d:
                    crossover = 'BULLISH'
                    score += 20
                
                # Bearish crossover: %K crosses below %D
                elif prev_k > prev_d and k < d:
                    crossover = 'BEARISH'
                    score -= 20
            
            score = max(0, min(100, score))
            
            return {
                'k': k,
                'd': d,
                'signal': signal,
                'crossover': crossover,
                'score': score
            }
            
        except Exception as e:
            print(f"⚠️ Stochastic calculation error: {e}")
            return {
                'k': 50,
                'd': 50,
                'signal': 'NEUTRAL',
                'crossover': 'NONE',
                'score': 0
            }
    
    # ========================================
    # PRIORITY 4: GREEKS ANALYSIS
    # ========================================
    
    def calculate_greeks(self, option_data, spot_price, days_to_expiry, implied_volatility=0.20):
        """
        Calculate Option Greeks (Delta, Gamma, Theta, Vega)
        
        Returns: {
            'delta': float,
            'gamma': float,
            'theta': float,
            'vega': float,
            'score': 0-100,
            'recommendation': str
        }
        """
        
        try:
            strike = option_data.get('strike', 0)
            option_type = option_data.get('option_type', 'CE')
            premium = option_data.get('ltp', 0)
            
            if strike == 0 or days_to_expiry <= 0:
                return self._default_greeks()
            
            # Convert days to years
            time_to_expiry = days_to_expiry / 365.0
            
            # Calculate d1 and d2 for Black-Scholes
            d1 = (np.log(spot_price / strike) + (self.risk_free_rate + 0.5 * implied_volatility ** 2) * time_to_expiry) / (implied_volatility * np.sqrt(time_to_expiry))
            d2 = d1 - implied_volatility * np.sqrt(time_to_expiry)
            
            # Standard normal CDF
            from scipy.stats import norm
            N_d1 = norm.cdf(d1)
            N_d2 = norm.cdf(d2)
            n_d1 = norm.pdf(d1)  # PDF for gamma, vega, theta
            
            # Calculate Greeks
            if option_type == 'CE':
                delta = N_d1
                theta = (-(spot_price * n_d1 * implied_volatility) / (2 * np.sqrt(time_to_expiry)) 
                        - self.risk_free_rate * strike * np.exp(-self.risk_free_rate * time_to_expiry) * N_d2) / 365
            else:  # PE
                delta = N_d1 - 1
                theta = (-(spot_price * n_d1 * implied_volatility) / (2 * np.sqrt(time_to_expiry)) 
                        + self.risk_free_rate * strike * np.exp(-self.risk_free_rate * time_to_expiry) * (1 - N_d2)) / 365
            
            gamma = n_d1 / (spot_price * implied_volatility * np.sqrt(time_to_expiry))
            vega = spot_price * n_d1 * np.sqrt(time_to_expiry) / 100  # Divided by 100 for 1% change
            
            # Score based on Greeks
            score = self._score_greeks(delta, gamma, theta, vega, option_type, days_to_expiry)
            recommendation = self._greeks_recommendation(delta, theta, days_to_expiry)
            
            return {
                'delta': delta,
                'gamma': gamma,
                'theta': theta,
                'vega': vega,
                'score': score,
                'recommendation': recommendation,
                'days_to_expiry': days_to_expiry
            }
            
        except Exception as e:
            print(f"⚠️ Greeks calculation error: {e}")
            return self._default_greeks()
    
    def _default_greeks(self):
        """Return default Greeks when calculation fails"""
        return {
            'delta': 0.5,
            'gamma': 0.01,
            'theta': -10,
            'vega': 50,
            'score': 50,
            'recommendation': 'Unable to calculate Greeks',
            'days_to_expiry': 0
        }
    
    def _score_greeks(self, delta, gamma, theta, vega, option_type, days_to_expiry):
        """Score option based on Greeks"""
        
        score = 50  # Base score
        
        # Delta scoring (prefer 0.3-0.7 delta)
        abs_delta = abs(delta)
        if 0.3 <= abs_delta <= 0.7:
            score += 20
        elif 0.2 <= abs_delta < 0.3 or 0.7 < abs_delta <= 0.8:
            score += 10
        else:
            score += 0
        
        # Theta scoring (avoid high theta decay)
        if days_to_expiry > 7:
            if theta > -20:
                score += 15
            elif theta > -40:
                score += 10
            else:
                score += 0
        else:
            # Last week - theta decay is severe
            if theta > -50:
                score += 5
            else:
                score -= 10
        
        # Gamma scoring (prefer moderate gamma)
        if 0.005 <= gamma <= 0.02:
            score += 10
        elif gamma > 0.02:
            score += 5  # High gamma = high risk/reward
        
        # Vega scoring (prefer high vega for volatility plays)
        if vega > 40:
            score += 5
        
        return max(0, min(100, score))
    
    def _greeks_recommendation(self, delta, theta, days_to_expiry):
        """Generate recommendation based on Greeks"""
        
        abs_delta = abs(delta)
        
        if days_to_expiry <= 3:
            return f"⚠️ High theta decay (₹{abs(theta):.1f}/day) - Avoid unless quick trade"
        
        if abs_delta < 0.2:
            return f"⚠️ Low delta ({abs_delta:.2f}) - Far OTM, low probability"
        
        if abs_delta > 0.8:
            return f"⚠️ High delta ({abs_delta:.2f}) - Deep ITM, expensive"
        
        if 0.3 <= abs_delta <= 0.7:
            return f"✅ Good delta ({abs_delta:.2f}) - Balanced risk/reward"
        
        return f"Moderate delta ({abs_delta:.2f})"


# ========================================
# INTEGRATION HELPER FUNCTIONS
# ========================================

def integrate_priority_features(algo_instance):
    """
    Integrate priority features into existing algorithm
    
    Usage:
        from priority_features import integrate_priority_features
        integrate_priority_features(algo)
    """
    
    # Add priority features instance
    algo_instance.priority_features = PriorityFeatures()
    
    print("✅ Priority Features Integrated:")
    print("   1. Market Condition Filter")
    print("   2. OI Change Analysis")
    print("   3. Stochastic Oscillator")
    print("   4. Greeks Analysis")
    
    return algo_instance
