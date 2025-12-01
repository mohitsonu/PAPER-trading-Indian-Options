#!/usr/bin/env python3
"""
🌐 OPEN TRADING REPORT IN BROWSER
Simple script to open the trading report in your default browser
"""

import webbrowser
import os
import sys

def open_report():
    report_file = "trading_report.html"
    
    if not os.path.exists(report_file):
        print(f"❌ Report file not found: {report_file}")
        print(f"💡 Generate it first: python generate_dynamic_report.py")
        return False
    
    # Get absolute path
    abs_path = os.path.abspath(report_file)
    
    print(f"🌐 Opening trading report in browser...")
    print(f"📊 File: {abs_path}")
    
    try:
        webbrowser.open(f"file:///{abs_path}")
        print(f"✅ Report opened successfully!")
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print(f"💡 Open manually: {abs_path}")
        return False

if __name__ == "__main__":
    open_report()
