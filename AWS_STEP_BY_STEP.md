# 🚀 AWS EC2 SETUP - COMPLETE STEP-BY-STEP GUIDE

## ⏱️ Total Time: 30-45 minutes
## 💰 Cost: FREE for 12 months

---

## 📋 WHAT YOU'LL NEED

- ✅ Email address
- ✅ Phone number
- ✅ Credit/Debit card (for verification only, won't be charged)
- ✅ Your trading bot files (from your laptop)
- ✅ Your Shoonya credentials (.env file)

---

## PART 1: CREATE AWS ACCOUNT (10 minutes)

### Step 1: Sign Up
1. Open browser → Go to: **https://aws.amazon.com/free/**
2. Click **"Create a Free Account"** (orange button)
3. Enter:
   - Email address
   - Password (strong password)
   - AWS account name (e.g., "My Trading Bot")
4. Click **"Continue"**

### Step 2: Contact Information
1. Select **"Personal"** account
2. Fill in your details:
   - Full name
   - Phone number
   - Address
3. Check the agreement box
4. Click **"Create Account and Continue"**

### Step 3: Payment Information
1. Enter credit/debit card details
2. ⚠️ **Don't worry**: You won't be charged if you stay in free tier
3. AWS will verify with ₹2 charge (refunded immediately)
4. Click **"Verify and Add"**

### Step 4: Identity Verification
1. Enter phone number
2. Choose **"Text message (SMS)"** or **"Voice call"**
3. Enter the 4-digit code you receive
4. Click **"Continue"**

### Step 5: Choose Support Plan
1. Select **"Basic support - Free"**
2. Click **"Complete sign up"**

### Step 6: Wait for Activation
1. You'll see "Congratulations" message
2. Wait 5-10 minutes for account activation
3. Check email for confirmation

✅ **Account Created!** Now let's launch your server...

---

## PART 2: LAUNCH EC2 INSTANCE (10 minutes)

### Step 1: Login to AWS Console
1. Go to: **https://console.aws.amazon.com/**
2. Click **"Sign in to the Console"**
3. Enter your email and password
4. You'll see AWS Management Console

### Step 2: Open EC2 Service
1. In the search bar at top, type: **"EC2"**
2. Click **"EC2"** (Virtual Servers in the Cloud)
3. You'll see EC2 Dashboard

### Step 3: Launch Instance
1. Click **"Launch Instance"** (orange button)
2. You'll see "Launch an instance" page

### Step 4: Configure Instance

**Name and Tags:**
- Name: **Trading-Bot**

**Application and OS Images:**
- Click **"Ubuntu"**
- Select **"Ubuntu Server 22.04 LTS"**
- Make sure it says **"Free tier eligible"** ✅

**Instance Type:**
- Select **"t2.micro"** (should be selected by default)
- Make sure it says **"Free tier eligible"** ✅

**Key Pair (Important!):**
1. Click **"Create new key pair"**
2. Key pair name: **trading-bot-key**
3. Key pair type: **RSA**
4. Private key file format: **".pem"** (for Windows with OpenSSH)
5. Click **"Create key pair"**
6. ⚠️ **IMPORTANT**: File will download - **SAVE IT SAFELY!**
7. Move the file to a safe location (e.g., Documents folder)

**Network Settings:**
1. Click **"Edit"** next to Network settings
2. Auto-assign public IP: **Enable**
3. Firewall (security groups): **Create security group**
4. Security group name: **trading-bot-sg**
5. Description: **Allow SSH access**
6. Keep the SSH rule (port 22) as is

**Configure Storage:**
- Keep default: **8 GB gp3** (Free tier eligible)

**Advanced Details:**
- Leave everything as default

### Step 5: Launch!
1. Review everything on the right side
2. Click **"Launch Instance"** (orange button)
3. You'll see "Successfully initiated launch of instance"
4. Click **"View all instances"**

### Step 6: Wait for Instance to Start
1. You'll see your instance in the list
2. Wait until **"Instance state"** shows **"Running"** (green)
3. Wait until **"Status check"** shows **"2/2 checks passed"** (green)
4. This takes about 2-3 minutes

✅ **Server is Running!** Now let's connect to it...

---

## PART 3: CONNECT TO YOUR SERVER (5 minutes)

### Step 1: Get Connection Details
1. Click on your instance (checkbox)
2. Click **"Connect"** button at top
3. Go to **"SSH client"** tab
4. You'll see connection instructions

### Step 2: Prepare Your Key File (Windows)

**Option A: Using PowerShell (Recommended)**
1. Open PowerShell (search "PowerShell" in Start menu)
2. Navigate to where you saved the .pem file:
```powershell
cd C:\Users\YourName\Documents
```
3. Set correct permissions:
```powershell
icacls "trading-bot-key.pem" /inheritance:r
icacls "trading-bot-key.pem" /grant:r "$($env:USERNAME):(R)"
```

**Option B: Using PuTTY (Alternative)**
- Download PuTTY and PuTTYgen
- Convert .pem to .ppk format
- (Google "convert pem to ppk" for detailed steps)

### Step 3: Connect via SSH
1. In PowerShell, copy the connection command from AWS:
```bash
ssh -i "trading-bot-key.pem" ubuntu@YOUR-IP-ADDRESS
```
2. Replace `YOUR-IP-ADDRESS` with the IP shown in AWS console
3. Press Enter
4. Type **"yes"** when asked "Are you sure you want to continue connecting?"
5. You're now connected! You'll see: `ubuntu@ip-xxx-xxx-xxx-xxx:~$`

✅ **Connected to Server!** Now let's install the bot...

---

## PART 4: INSTALL TRADING BOT (10 minutes)

### Step 1: Run Automated Setup
1. In the SSH terminal, run:
```bash
wget https://raw.githubusercontent.com/YOUR-REPO/aws_setup.sh
chmod +x aws_setup.sh
./aws_setup.sh
```

**OR manually:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install -y python3 python3-pip python3-venv

# Create directory
mkdir -p ~/trading-bot
cd ~/trading-bot

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install pandas numpy python-dotenv pyotp schedule psutil NorenRestApiPy
```

### Step 2: Upload Your Files

**Option A: Using WinSCP (Easiest)**
1. Download WinSCP: https://winscp.net/
2. Install and open WinSCP
3. Click "New Site"
4. File protocol: **SFTP**
5. Host name: **Your EC2 IP address**
6. Port: **22**
7. User name: **ubuntu**
8. Click "Advanced" → "SSH" → "Authentication"
9. Private key file: Browse to your **trading-bot-key.pem**
10. Click "OK" then "Login"
11. Drag and drop your files from left (laptop) to right (server)
12. Upload these files:
    - run_high_accuracy.py
    - high_accuracy_algo.py
    - auto_trader_scheduler.py
    - priority_features.py
    - adaptive_market_engine.py
    - trailing_stop_manager.py
    - trade_state_persistence.py
    - brokerage_calculator.py
    - expiry_config.json
    - .env (with your credentials)
    - All other .py files

**Option B: Using SCP Command**
```bash
# On your laptop (PowerShell)
scp -i "trading-bot-key.pem" -r "E:\SHOONYS PAPER\*" ubuntu@YOUR-IP:~/trading-bot/
```

### Step 3: Create .env File
If you didn't upload .env, create it:
```bash
cd ~/trading-bot
nano .env
```

Paste your credentials:
```
SHOONYA_USER_ID=your_user_id
SHOONYA_PASSWORD=your_password
SHOONYA_TOTP_KEY=your_totp_key
SHOONYA_VENDOR_CODE=your_vendor_code
SHOONYA_API_SECRET=your_api_secret
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 4: Test the Bot
```bash
cd ~/trading-bot
source .venv/bin/activate
python test_scheduler.py
```

You should see: ✅ All systems ready!

✅ **Bot Installed!** Now let's make it run 24/7...

---

## PART 5: SETUP AUTO-START (5 minutes)

### Step 1: Create Service File
```bash
sudo nano /etc/systemd/system/trading-bot.service
```

### Step 2: Paste This Configuration
```ini
[Unit]
Description=Auto Trading Bot Scheduler
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading-bot
Environment="PATH=/home/ubuntu/trading-bot/.venv/bin"
ExecStart=/home/ubuntu/trading-bot/.venv/bin/python auto_trader_scheduler.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/trading-bot/service.log
StandardError=append:/home/ubuntu/trading-bot/service.log

[Install]
WantedBy=multi-user.target
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 3: Enable and Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable trading-bot

# Start service now
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot
```

You should see: **Active: active (running)** in green!

### Step 4: View Logs
```bash
# View service logs
sudo journalctl -u trading-bot -f

# View scheduler logs
tail -f ~/trading-bot/auto_trader_scheduler.log

# View today's trades
cat ~/trading-bot/high_accuracy_trades_$(date +%Y%m%d).csv
```

Press `Ctrl+C` to stop viewing logs.

✅ **Bot is Running 24/7!** 

---

## PART 6: MONITORING & MAINTENANCE

### Check Status Anytime
```bash
# SSH into server
ssh -i "trading-bot-key.pem" ubuntu@YOUR-IP

# Check if running
sudo systemctl status trading-bot

# View recent logs
tail -n 50 ~/trading-bot/auto_trader_scheduler.log

# Check today's trades
cat ~/trading-bot/high_accuracy_trades_$(date +%Y%m%d).csv
```

### Restart Bot
```bash
sudo systemctl restart trading-bot
```

### Stop Bot
```bash
sudo systemctl stop trading-bot
```

### Update Bot Code
```bash
# Upload new files via WinSCP
# Then restart service
sudo systemctl restart trading-bot
```

### View All Logs
```bash
# Scheduler logs
cat ~/trading-bot/auto_trader_scheduler.log

# Service logs
sudo journalctl -u trading-bot --no-pager

# Last 100 lines
sudo journalctl -u trading-bot -n 100
```

---

## 🔒 SECURITY BEST PRACTICES

1. **Never share your .pem key file**
2. **Keep .env file secure**
3. **Enable AWS MFA (Multi-Factor Authentication)**:
   - AWS Console → Your Name → Security Credentials
   - Enable MFA
4. **Set up billing alerts**:
   - AWS Console → Billing → Billing Preferences
   - Enable "Receive Free Tier Usage Alerts"
   - Set alert at $1

---

## 💰 COST MONITORING

### Check Your Usage
1. AWS Console → Billing Dashboard
2. Check "Free Tier Usage"
3. Make sure you're within limits:
   - EC2: 750 hours/month (t2.micro)
   - Storage: 30 GB
   - Data transfer: 15 GB out

### Set Up Billing Alert
1. AWS Console → CloudWatch → Billing
2. Create Alarm
3. Set threshold: $1
4. Enter your email
5. You'll get alert if charges exceed $1

---

## 🎉 YOU'RE DONE!

Your trading bot is now running 24/7 on AWS!

**What happens now:**
- ✅ Bot starts automatically at 9:15 AM (Mon-Fri)
- ✅ Bot stops automatically at 3:30 PM
- ✅ Restarts if it crashes
- ✅ Runs even when your laptop is off
- ✅ You can monitor from anywhere

**To check trades:**
1. SSH into server
2. View CSV files
3. Or setup Telegram notifications (already configured!)

---

## 🆘 TROUBLESHOOTING

### Bot not starting
```bash
# Check service status
sudo systemctl status trading-bot

# View error logs
sudo journalctl -u trading-bot -n 50

# Check if files exist
ls -la ~/trading-bot/

# Check Python environment
source ~/trading-bot/.venv/bin/activate
python --version
```

### Can't connect via SSH
- Check security group allows SSH from your IP
- Verify .pem file permissions
- Check instance is running (AWS Console)

### Bot crashes repeatedly
- Check logs: `tail -f ~/trading-bot/auto_trader_scheduler.log`
- Verify .env credentials are correct
- Check internet connectivity: `ping google.com`

---

## 📞 NEED HELP?

If you get stuck at any step, note down:
1. Which step you're on
2. What error message you see
3. Screenshot if possible

I can help you troubleshoot!
