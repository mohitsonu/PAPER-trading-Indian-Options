#!/usr/bin/env python3
"""
🤖 AUTOMATIC TRADING SCHEDULER
Runs the high accuracy trading algorithm automatically during market hours
Monday to Friday: 9:15 AM - 3:30 PM

Features:
- Auto-starts at 9:15 AM on trading days
- Auto-stops at 3:30 PM
- Skips weekends and holidays
- Restarts if algorithm crashes
- Logs all activities
"""

import schedule
import time
import subprocess
import os
import sys
from datetime import datetime, time as dt_time
import logging
from pathlib import Path

# Setup logging
log_file = "auto_trader_scheduler.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

class AutoTrader:
    def __init__(self):
        self.process = None
        self.is_running = False
        self.market_open_time = dt_time(9, 15)  # 9:15 AM
        self.market_close_time = dt_time(15, 30)  # 3:30 PM
        
    def is_trading_day(self):
        """Check if today is a trading day (Monday-Friday)"""
        today = datetime.now()
        # 0 = Monday, 6 = Sunday
        is_weekday = today.weekday() < 5
        
        if not is_weekday:
            logging.info(f"📅 Today is {today.strftime('%A')} - Not a trading day")
            return False
        
        # TODO: Add holiday check here if needed
        # You can maintain a list of market holidays
        
        return True
    
    def is_market_hours(self):
        """Check if current time is within market hours"""
        now = datetime.now().time()
        return self.market_open_time <= now <= self.market_close_time
    
    def start_trading(self):
        """Start the trading algorithm"""
        if not self.is_trading_day():
            logging.info("⏸️ Skipping - Not a trading day")
            return
        
        if not self.is_market_hours():
            logging.info("⏸️ Skipping - Outside market hours")
            return
        
        if self.is_running:
            logging.info("✅ Algorithm already running")
            return
        
        try:
            logging.info("🚀 Starting trading algorithm...")
            
            # Start the algorithm as a subprocess
            self.process = subprocess.Popen(
                [sys.executable, "run_high_accuracy.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.is_running = True
            logging.info(f"✅ Trading algorithm started (PID: {self.process.pid})")
            
        except Exception as e:
            logging.error(f"❌ Failed to start algorithm: {e}")
            self.is_running = False
    
    def stop_trading(self):
        """Stop the trading algorithm"""
        if not self.is_running or self.process is None:
            logging.info("⏸️ Algorithm not running")
            return
        
        try:
            logging.info("🛑 Stopping trading algorithm...")
            self.process.terminate()
            
            # Wait for process to terminate (max 30 seconds)
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                logging.warning("⚠️ Process didn't terminate, forcing kill...")
                self.process.kill()
                self.process.wait()
            
            self.is_running = False
            self.process = None
            logging.info("✅ Trading algorithm stopped")
            
        except Exception as e:
            logging.error(f"❌ Failed to stop algorithm: {e}")
    
    def check_health(self):
        """Check if algorithm is still running and restart if needed"""
        if not self.is_trading_day():
            return
        
        if not self.is_market_hours():
            if self.is_running:
                logging.info("⏰ Market closed - Stopping algorithm")
                self.stop_trading()
            return
        
        # Check if process is still alive
        if self.is_running and self.process is not None:
            poll = self.process.poll()
            if poll is not None:
                # Process has terminated
                logging.warning(f"⚠️ Algorithm crashed with exit code {poll}")
                self.is_running = False
                self.process = None
                
                # Restart
                logging.info("🔄 Restarting algorithm...")
                time.sleep(5)  # Wait 5 seconds before restart
                self.start_trading()
        elif not self.is_running:
            # Should be running but isn't
            logging.info("🔄 Algorithm should be running - Starting...")
            self.start_trading()
    
    def run_scheduler(self):
        """Main scheduler loop"""
        logging.info("=" * 60)
        logging.info("🤖 AUTO TRADER SCHEDULER STARTED")
        logging.info("=" * 60)
        logging.info(f"📅 Trading Days: Monday - Friday")
        logging.info(f"⏰ Market Hours: 9:15 AM - 3:30 PM")
        logging.info(f"🔄 Health Check: Every 5 minutes")
        logging.info("=" * 60)
        
        # Schedule tasks
        schedule.every().day.at("09:15").do(self.start_trading)
        schedule.every().day.at("15:30").do(self.stop_trading)
        schedule.every(5).minutes.do(self.check_health)
        
        # Initial check
        self.check_health()
        
        # Run scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            logging.info("\n🛑 Scheduler stopped by user")
            if self.is_running:
                self.stop_trading()
        except Exception as e:
            logging.error(f"❌ Scheduler error: {e}")
            if self.is_running:
                self.stop_trading()

def main():
    """Main entry point"""
    trader = AutoTrader()
    trader.run_scheduler()

if __name__ == "__main__":
    main()
