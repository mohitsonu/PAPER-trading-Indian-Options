# 🔔 Telegram Trading Signals

Send real-time trading signals to your Telegram channel/group to share results with friends!

## 📋 Quick Setup (5 minutes)

### Step 1: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name (e.g., "My Trading Signals")
4. Choose a username (e.g., "my_trading_bot")
5. Copy the **bot token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Chat ID

**Option A - Personal Chat (Private):**
1. Search for `@userinfobot` on Telegram
2. Start chat - it will show your chat ID
3. Copy the number

**Option B - Channel (Public/Private):**
1. Create a channel in Telegram
2. Add your bot as administrator
3. For public channel: use `@channel_username`
4. For private channel: Get ID using @userinfobot method

**Option C - Group:**
1. Create a group
2. Add your bot to the group
3. Add `@userinfobot` to get group ID (starts with `-`)
4. Remove @userinfobot after getting ID

### Step 3: Configure

Edit `telegram_signals/config.py`:

```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your bot token
TELEGRAM_CHAT_ID = "-1001234567890"  # Your chat/channel/group ID
TELEGRAM_ENABLED = True  # Enable notifications
```

### Step 4: Test

```bash
cd telegram_signals
python test_telegram.py
```

You should receive test messages in your Telegram!

## 🚀 Usage

The integration is automatic. Once configured, signals will be sent for:

- ✅ **Session Start** - When trading begins
- 🟢 **Entry Signals** - When positions are opened
- 🔴 **Exit Signals** - When positions are closed
- 📊 **Daily Summary** - End of day results

## 📱 Signal Format

### Entry Signal
```
🟢 ENTRY SIGNAL 🟢

📊 Symbol: NIFTY11NOV25C25400
💰 Entry Price: ₹110.30
📦 Quantity: 300
🎯 Accuracy Score: 100/100
📈 Strategy: TREND_BULL_CE

💡 Reason: Good OI, Strong trend
⏰ Time: 07-Nov-2025 11:20:52 AM
```

### Exit Signal
```
🟢 EXIT SIGNAL - PROFIT 🟢

📊 Symbol: NIFTY11NOV25C25400
💵 Entry: ₹110.30
💵 Exit: ₹129.40
📦 Quantity: 300

💰 P&L: ₹+5,690 (+17.3%)
⏱️ Holding Time: 8 minutes
📋 Exit Reason: IMMEDIATE_PROFIT_BOOK

⏰ Time: 07-Nov-2025 11:29:13 AM
```

### Daily Summary
```
🎉 DAILY SUMMARY 🎉

📅 Date: 07-Nov-2025

💰 Starting Capital: ₹1,00,000
💰 Ending Capital: ₹1,46,310
📊 Net P&L: ₹+46,310 (+46.31%)

📋 Total Trades: 16
🎯 Win Rate: 75.0% (12W / 4L)

⏰ Session End: 03:17:32 PM
```

## 🔧 Troubleshooting

**Bot not sending messages?**
- Check bot token is correct
- Make sure bot is added to channel/group as admin
- Verify chat ID is correct (should start with `-` for groups)

**"Chat not found" error?**
- Send a message to your bot first
- For channels: Make bot an administrator
- For groups: Add bot before getting chat ID

**Connection timeout?**
- Check internet connection
- Verify firewall isn't blocking Telegram API

## 🎯 Tips

1. **Create a private channel** for personal use
2. **Create a public channel** to share with friends
3. **Use a group** for team trading discussions
4. **Multiple channels**: You can send to multiple chats by creating multiple notifier instances

## 📝 Notes

- Free forever (Telegram API is free)
- No rate limits for normal usage
- Messages are instant (< 1 second)
- Works on all devices (mobile, desktop, web)
- Your friends can subscribe to your channel to see signals

## 🔒 Privacy

- Bot token is private - don't share it
- Chat ID is just a number - safe to share
- Messages are only sent to configured chat
- No data is stored by Telegram bot
