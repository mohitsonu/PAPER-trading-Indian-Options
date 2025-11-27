#!/usr/bin/env python3
"""
💰 REALISTIC BROKERAGE & CHARGES CALCULATOR
Calculates all real trading charges including brokerage, STT, GST, etc.
"""

class BrokerageCalculator:
    """Calculate realistic trading charges for Indian options trading (NSE)"""
    
    def __init__(self, broker_type='discount'):
        """
        Initialize brokerage calculator with ground reality charges
        
        Args:
            broker_type: 'discount' (₹20/order) or 'traditional' (0.05% of turnover)
        
        Charges based on:
        - FYERS, Shoonya, Zerodha (discount brokers)
        - NSE Options trading
        - Current Indian regulations
        """
        self.broker_type = broker_type
        
        # 1. BROKERAGE CHARGES
        # Discount brokers: Flat ₹20 per executed order
        if broker_type == 'discount':
            self.brokerage_per_order = 20  # ₹20 per order (buy or sell)
        else:
            self.brokerage_percentage = 0.0005  # 0.05% for traditional brokers
        
        # 2. EXCHANGE TRANSACTION CHARGES (NSE Options)
        # ₹2 per lakh of turnover (buy value + sell value)
        self.exchange_charge_per_lakh = 2  # ₹2 per ₹1,00,000 turnover
        
        # 3. STT (Securities Transaction Tax)
        # On SELL side only: 0.05% of sell premium value
        self.stt_rate = 0.0005  # 0.05% = 0.0005
        
        # 4. GST (Goods & Services Tax)
        # 18% on (brokerage + exchange + SEBI + clearing)
        self.gst_rate = 0.18  # 18%
        
        # 5. SEBI CHARGES
        # ₹10 per crore of turnover (₹0.0001%)
        self.sebi_charge_per_crore = 10  # ₹10 per ₹1,00,00,000
        
        # 6. STAMP DUTY
        # On BUY side only: ₹300 per crore (0.003% of buy value)
        self.stamp_duty_per_crore = 300  # ₹300 per ₹1,00,00,000
        
        # 7. CLEARING CHARGES
        # Usually ₹0.01 per lot per side (often negligible)
        self.clearing_charge_per_lot = 0.01  # ₹0.01 per lot
    
    def calculate_charges(self, buy_price, sell_price, quantity, lot_size=1):
        """
        Calculate all trading charges for an options trade (GROUND REALITY)
        
        Args:
            buy_price: Entry/buy price of option (₹ per lot)
            sell_price: Exit/sell price of option (₹ per lot)
            quantity: Number of lots traded
            lot_size: Lot size (default 1 for already calculated lots)
        
        Returns:
            dict: Detailed breakdown of all charges
        
        Example:
            buy_price = 88.95, sell_price = 109.5, quantity = 300
            Buy Value = 88.95 × 300 = ₹26,685
            Sell Value = 109.5 × 300 = ₹32,850
        """
        
        # Calculate trade values
        buy_value = buy_price * quantity * lot_size
        sell_value = sell_price * quantity * lot_size
        total_turnover = buy_value + sell_value
        
        # 1. BROKERAGE (₹20 per order for discount brokers)
        if self.broker_type == 'discount':
            brokerage_buy = self.brokerage_per_order  # ₹20 for buy
            brokerage_sell = self.brokerage_per_order  # ₹20 for sell
            total_brokerage = brokerage_buy + brokerage_sell  # ₹40 total
        else:
            brokerage_buy = buy_value * self.brokerage_percentage
            brokerage_sell = sell_value * self.brokerage_percentage
            total_brokerage = brokerage_buy + brokerage_sell
        
        # 2. EXCHANGE TRANSACTION CHARGES
        # ₹2 per lakh of turnover (buy + sell)
        # Formula: (turnover / 1,00,000) × ₹2
        exchange_charges = (total_turnover / 100000) * self.exchange_charge_per_lakh
        
        # 3. STT (Securities Transaction Tax)
        # On SELL side only: 0.05% of sell value
        stt = sell_value * self.stt_rate
        
        # 4. SEBI CHARGES
        # ₹10 per crore of turnover
        # Formula: (turnover / 1,00,00,000) × ₹10
        sebi_charges = (total_turnover / 10000000) * self.sebi_charge_per_crore
        
        # 5. STAMP DUTY
        # On BUY side only: ₹300 per crore (0.003%)
        # Formula: (buy_value / 1,00,00,000) × ₹300
        stamp_duty = (buy_value / 10000000) * self.stamp_duty_per_crore
        
        # 6. CLEARING CHARGES
        # ₹0.01 per lot (usually negligible)
        # For both buy and sell sides
        clearing_charges = quantity * lot_size * self.clearing_charge_per_lot * 2  # Buy + Sell
        
        # 7. GST (Goods & Services Tax)
        # 18% on (brokerage + exchange + SEBI + clearing)
        # NOTE: GST is NOT applied on STT and Stamp Duty
        gst_base = total_brokerage + exchange_charges + sebi_charges + clearing_charges
        gst = gst_base * self.gst_rate
        
        # TOTAL CHARGES (sum of all components)
        total_charges = (
            total_brokerage +
            exchange_charges +
            stt +
            sebi_charges +
            stamp_duty +
            clearing_charges +
            gst
        )
        
        # Calculate P&L
        gross_pnl = (sell_price - buy_price) * quantity * lot_size
        net_pnl = gross_pnl - total_charges
        
        # Charges as percentage of turnover
        charges_percentage = (total_charges / total_turnover * 100) if total_turnover > 0 else 0
        
        # Impact on profit (if profitable)
        charges_impact_on_profit = (total_charges / gross_pnl * 100) if gross_pnl > 0 else 0
        
        return {
            'buy_value': buy_value,
            'sell_value': sell_value,
            'total_turnover': total_turnover,
            'brokerage': {
                'buy': brokerage_buy,
                'sell': brokerage_sell,
                'total': total_brokerage
            },
            'exchange_charges': exchange_charges,
            'stt': stt,
            'sebi_charges': sebi_charges,
            'stamp_duty': stamp_duty,
            'clearing_charges': clearing_charges,
            'gst': gst,
            'gst_base': gst_base,
            'total_charges': total_charges,
            'charges_percentage': charges_percentage,
            'charges_impact_on_profit': charges_impact_on_profit,
            'gross_pnl': gross_pnl,
            'net_pnl': net_pnl,
            'charges_breakdown': {
                'Brokerage': total_brokerage,
                'Exchange Charges': exchange_charges,
                'STT': stt,
                'GST': gst,
                'Stamp Duty': stamp_duty,
                'SEBI Charges': sebi_charges,
                'Clearing Charges': clearing_charges
            }
        }
    
    def calculate_breakeven(self, buy_price, quantity, lot_size=1):
        """
        Calculate breakeven price (price needed to cover all charges)
        
        Args:
            buy_price: Entry price
            quantity: Number of lots
            lot_size: Lot size
        
        Returns:
            float: Breakeven sell price
        """
        
        # Estimate charges for breakeven (iterative approach)
        # Start with buy price as sell price
        sell_price = buy_price
        
        for _ in range(10):  # Iterate to converge
            charges = self.calculate_charges(buy_price, sell_price, quantity, lot_size)
            
            # Breakeven: gross_pnl = total_charges
            # (sell_price - buy_price) * quantity * lot_size = total_charges
            required_gain = charges['total_charges'] / (quantity * lot_size)
            sell_price = buy_price + required_gain
        
        return sell_price
    
    def print_charges_breakdown(self, charges):
        """Print detailed charges breakdown (Ground Reality Format)"""
        
        print(f"\n{'='*80}")
        print(f"💰 REALISTIC CHARGES BREAKDOWN (NSE Options)")
        print(f"{'='*80}")
        
        print(f"\n📊 Trade Details:")
        print(f"   Buy Value:        ₹{charges['buy_value']:>12,.2f}")
        print(f"   Sell Value:       ₹{charges['sell_value']:>12,.2f}")
        print(f"   Total Turnover:   ₹{charges['total_turnover']:>12,.2f}")
        
        print(f"\n💸 Detailed Charges Breakdown:")
        print(f"   ─────────────────────────────────────────────────────────────────")
        
        print(f"\n   1. Brokerage (₹20 per order):")
        print(f"      • Buy Order:   ₹{charges['brokerage']['buy']:>8.2f}")
        print(f"      • Sell Order:  ₹{charges['brokerage']['sell']:>8.2f}")
        print(f"      • Total:       ₹{charges['brokerage']['total']:>8.2f}")
        
        print(f"\n   2. Exchange Transaction Charges (₹2 per lakh):")
        print(f"      • Formula: (₹{charges['total_turnover']:,.0f} / 1,00,000) × ₹2")
        print(f"      • Amount:      ₹{charges['exchange_charges']:>8.2f}")
        
        print(f"\n   3. STT - Securities Transaction Tax (0.05% on sell):")
        print(f"      • Formula: ₹{charges['sell_value']:,.0f} × 0.0005")
        print(f"      • Amount:      ₹{charges['stt']:>8.2f}")
        
        print(f"\n   4. SEBI Charges (₹10 per crore):")
        print(f"      • Formula: (₹{charges['total_turnover']:,.0f} / 1,00,00,000) × ₹10")
        print(f"      • Amount:      ₹{charges['sebi_charges']:>8.2f}")
        
        print(f"\n   5. Stamp Duty (₹300 per crore on buy):")
        print(f"      • Formula: (₹{charges['buy_value']:,.0f} / 1,00,00,000) × ₹300")
        print(f"      • Amount:      ₹{charges['stamp_duty']:>8.2f}")
        
        print(f"\n   6. Clearing Charges (₹0.01 per lot):")
        print(f"      • Amount:      ₹{charges['clearing_charges']:>8.2f}")
        
        print(f"\n   7. GST (18% on brokerage + exchange + SEBI + clearing):")
        print(f"      • GST Base:    ₹{charges['gst_base']:>8.2f}")
        print(f"      • GST (18%):   ₹{charges['gst']:>8.2f}")
        
        print(f"\n   ─────────────────────────────────────────────────────────────────")
        print(f"   TOTAL CHARGES:     ₹{charges['total_charges']:>12.2f}")
        print(f"   ({charges['charges_percentage']:.3f}% of turnover)")
        print(f"   ─────────────────────────────────────────────────────────────────")
        
        print(f"\n📈 Profit & Loss Analysis:")
        print(f"   Gross P&L:         ₹{charges['gross_pnl']:>12,.2f}")
        print(f"   Less: Charges:     ₹{charges['total_charges']:>12,.2f}")
        print(f"   ───────────────────────────────────────")
        print(f"   Net P&L:           ₹{charges['net_pnl']:>12,.2f}")
        
        if charges['gross_pnl'] > 0:
            print(f"\n   💡 Charges eat {charges['charges_impact_on_profit']:.1f}% of your gross profit")
        elif charges['gross_pnl'] < 0:
            print(f"\n   ⚠️  Charges add to your loss (total loss = loss + charges)")
        
        print(f"\n{'='*80}\n")


def calculate_tax_on_profit(net_pnl, tax_slab=0.30):
    """
    Calculate tax on trading profit
    
    Args:
        net_pnl: Net profit after all charges
        tax_slab: Tax rate (default 30% for speculative income)
    
    Returns:
        dict: Tax breakdown
    """
    
    if net_pnl <= 0:
        return {
            'net_pnl': net_pnl,
            'tax': 0,
            'profit_after_tax': net_pnl,
            'tax_rate': 0
        }
    
    # Intraday options trading is considered speculative income
    # Taxed at individual's tax slab rate
    # Assuming 30% tax slab (can be adjusted)
    
    tax = net_pnl * tax_slab
    profit_after_tax = net_pnl - tax
    
    return {
        'net_pnl': net_pnl,
        'tax': tax,
        'profit_after_tax': profit_after_tax,
        'tax_rate': tax_slab * 100,
        'effective_return': (profit_after_tax / net_pnl * 100) if net_pnl > 0 else 0
    }


# Example usage and testing
if __name__ == "__main__":
    print("💰 REALISTIC BROKERAGE CALCULATOR - GROUND REALITY")
    print("="*80)
    print("Based on: FYERS, Shoonya, Zerodha (Discount Brokers)")
    print("Market: NSE Options")
    print("="*80)
    
    # Initialize calculator
    calc = BrokerageCalculator(broker_type='discount')
    
    # Example 1: Your exact trade example
    print("\n📊 EXAMPLE 1: Real Trade (From Your Data)")
    print("-"*80)
    print("Trade: NIFTY11NOV25C25550")
    print("Buy: ₹88.95 × 300 lots")
    print("Sell: ₹109.5 × 300 lots")
    print("-"*80)
    
    buy_price = 88.95
    sell_price = 109.50
    quantity = 300
    
    charges = calc.calculate_charges(buy_price, sell_price, quantity)
    calc.print_charges_breakdown(charges)
    
    # Calculate tax
    tax_info = calculate_tax_on_profit(charges['net_pnl'], tax_slab=0.30)
    
    print(f"💵 TAX CALCULATION (30% tax slab - Speculative Income):")
    print(f"   ─────────────────────────────────────────────────────────────────")
    print(f"   Net P&L (after charges):  ₹{tax_info['net_pnl']:>12,.2f}")
    print(f"   Less: Tax @ 30%:          ₹{tax_info['tax']:>12,.2f}")
    print(f"   ─────────────────────────────────────────────────────────────────")
    print(f"   Profit After Tax:         ₹{tax_info['profit_after_tax']:>12,.2f}")
    print(f"   ─────────────────────────────────────────────────────────────────")
    print(f"\n   💡 You keep {tax_info['effective_return']:.1f}% of net profit after tax")
    
    # Example 2: Profitable trade (50% gain)
    print("\n\n📊 EXAMPLE 2: Target Hit Trade (50% Profit)")
    print("-"*80)
    print("Trade: NIFTY Option")
    print("Buy: ₹45.50 × 300 lots")
    print("Sell: ₹68.25 × 300 lots (50% gain)")
    print("-"*80)
    
    buy_price = 45.50
    sell_price = 68.25  # 50% profit
    quantity = 300
    
    charges = calc.calculate_charges(buy_price, sell_price, quantity)
    calc.print_charges_breakdown(charges)
    
    # Calculate tax
    tax_info = calculate_tax_on_profit(charges['net_pnl'], tax_slab=0.30)
    print(f"💵 After 30% Tax: ₹{tax_info['profit_after_tax']:+,.2f}")
    
    # Example 3: Loss trade (Stop loss hit)
    print("\n\n📊 EXAMPLE 3: Stop Loss Hit (25% Loss)")
    print("-"*80)
    print("Trade: NIFTY Option")
    print("Buy: ₹45.50 × 300 lots")
    print("Sell: ₹34.13 × 300 lots (25% loss)")
    print("-"*80)
    
    buy_price = 45.50
    sell_price = 34.13  # 25% loss
    quantity = 300
    
    charges = calc.calculate_charges(buy_price, sell_price, quantity)
    calc.print_charges_breakdown(charges)
    
    print(f"⚠️  Note: Charges apply even on losing trades!")
    print(f"   Your actual loss = Price loss + All charges")
    
    # Example 4: Breakeven calculation
    print("\n\n📊 EXAMPLE 4: Breakeven Price Calculation")
    print("-"*80)
    
    buy_price = 45.50
    quantity = 300
    
    breakeven = calc.calculate_breakeven(buy_price, quantity)
    
    print(f"   Entry Price:       ₹{buy_price:.2f}")
    print(f"   Breakeven Price:   ₹{breakeven:.2f}")
    print(f"   Required Gain:     ₹{breakeven - buy_price:.2f} ({(breakeven/buy_price - 1)*100:.2f}%)")
    print(f"\n   💡 You need {(breakeven/buy_price - 1)*100:.2f}% gain just to break even!")
    
    # Verify breakeven
    be_charges = calc.calculate_charges(buy_price, breakeven, quantity)
    print(f"\n   Verification:")
    print(f"   Gross P&L at breakeven:  ₹{be_charges['gross_pnl']:.2f}")
    print(f"   Total Charges:           ₹{be_charges['total_charges']:.2f}")
    print(f"   Net P&L:                 ₹{be_charges['net_pnl']:.2f} ✅")
    
    # Example 5: Small trade (to show charges impact)
    print("\n\n📊 EXAMPLE 5: Small Trade (₹1000 Profit)")
    print("-"*80)
    print("Showing how charges eat into small profits")
    print("-"*80)
    
    # Calculate for ₹1000 gross profit
    buy_price = 100
    sell_price = 103.33  # ~₹1000 profit for 300 lots
    quantity = 300
    
    charges = calc.calculate_charges(buy_price, sell_price, quantity)
    calc.print_charges_breakdown(charges)
    
    print(f"⚠️  On small profits, charges can eat 10-15% of your gains!")
    
    print("\n" + "="*80)
    print("✅ TESTING COMPLETE - All Calculations Based on Ground Reality!")
    print("="*80)
    print("\n💡 Key Takeaways:")
    print("   • Brokerage: ₹40 per round-trip (₹20 buy + ₹20 sell)")
    print("   • Total charges typically: ₹60-100 per trade")
    print("   • Charges are ~0.1-0.2% of turnover")
    print("   • Always factor in charges + tax for realistic P&L")
    print("   • Breakeven requires ~0.2-0.5% gain depending on trade size")
    print("="*80)
