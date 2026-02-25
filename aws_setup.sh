#!/bin/bash
# ☁️ AWS EC2 AUTOMATED SETUP SCRIPT
# Run this script on your AWS EC2 instance after connecting via SSH

echo "=========================================="
echo "🚀 AUTO TRADING BOT - AWS SETUP"
echo "=========================================="
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python..."
sudo apt install -y python3 python3-pip python3-venv git

# Install system dependencies
echo "📚 Installing system dependencies..."
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Create project directory
echo "📁 Creating project directory..."
cd ~
mkdir -p trading-bot
cd trading-bot

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install pandas numpy python-dotenv pyotp schedule psutil

# Install NorenRestApiPy (Shoonya API)
echo "📡 Installing Shoonya API..."
pip install NorenRestApiPy

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Upload your trading bot files to this server"
echo "   Use WinSCP, FileZilla, or scp command:"
echo "   scp -i your-key.pem -r /path/to/your/files ubuntu@$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):~/trading-bot/"
echo ""
echo "2. Create .env file with your credentials:"
echo "   nano .env"
echo ""
echo "3. Test the bot:"
echo "   source .venv/bin/activate"
echo "   python run_high_accuracy.py"
echo ""
echo "4. Setup auto-start service:"
echo "   sudo nano /etc/systemd/system/trading-bot.service"
echo ""
echo "5. Enable and start service:"
echo "   sudo systemctl enable trading-bot"
echo "   sudo systemctl start trading-bot"
echo ""
echo "=========================================="
