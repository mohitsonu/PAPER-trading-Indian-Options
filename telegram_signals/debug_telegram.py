"""
🔍 Debug Telegram Connection
Find out what's wrong with your setup
"""

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def debug_telegram():
    """Debug Telegram connection issues"""
    
    print("🔍 TELEGRAM DEBUG TOOL")
    print("=" * 60)
    
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    
    # Test 1: Check bot token
    print("\n1️⃣ Testing Bot Token...")
    try:
        response = requests.get(f"{base_url}/getMe", timeout=10)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result['result']
            print(f"✅ Bot is valid!")
            print(f"   Bot Name: {bot_info.get('first_name')}")
            print(f"   Bot Username: @{bot_info.get('username')}")
            print(f"   Bot ID: {bot_info.get('id')}")
        else:
            print(f"❌ Invalid bot token!")
            print(f"   Error: {result}")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Test 2: Try to send message
    print(f"\n2️⃣ Testing Message Send to: {TELEGRAM_CHAT_ID}")
    try:
        url = f"{base_url}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': '🧪 Test message from debug tool',
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Message sent successfully!")
            print(f"   Message ID: {result['result'].get('message_id')}")
            print(f"   Chat ID: {result['result']['chat'].get('id')}")
            print(f"   Chat Type: {result['result']['chat'].get('type')}")
            if 'title' in result['result']['chat']:
                print(f"   Chat Title: {result['result']['chat'].get('title')}")
        else:
            print(f"❌ Failed to send message!")
            print(f"   Error Code: {result.get('error_code')}")
            print(f"   Error Description: {result.get('description')}")
            
            # Common error solutions
            error_desc = result.get('description', '')
            print(f"\n💡 SOLUTION:")
            
            if 'chat not found' in error_desc.lower():
                print("   ❌ Chat ID is wrong or bot hasn't started chat")
                print("   📝 For channel: Make sure bot is added as ADMIN")
                print("   📝 For personal: Send /start to your bot first")
                print("   📝 For group: Add bot to group first")
                
            elif 'bot was blocked' in error_desc.lower():
                print("   ❌ You blocked the bot")
                print("   📝 Unblock the bot in Telegram")
                
            elif 'not enough rights' in error_desc.lower():
                print("   ❌ Bot doesn't have permission to post")
                print("   📝 Make bot an ADMIN in the channel/group")
                
            elif 'username' in error_desc.lower():
                print("   ❌ Channel username is wrong")
                print("   📝 Check channel username (without @)")
                print("   📝 Or use numeric chat ID instead")
    
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    # Test 3: Get updates to find chat ID
    print(f"\n3️⃣ Checking Recent Updates (to find correct chat ID)...")
    try:
        response = requests.get(f"{base_url}/getUpdates", timeout=10)
        result = response.json()
        
        if result.get('ok') and result.get('result'):
            updates = result['result']
            print(f"✅ Found {len(updates)} recent updates")
            
            # Extract unique chat IDs
            chat_ids = set()
            for update in updates:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    chat_type = update['message']['chat']['type']
                    chat_title = update['message']['chat'].get('title', 
                                 update['message']['chat'].get('first_name', 'Unknown'))
                    chat_ids.add((chat_id, chat_type, chat_title))
            
            if chat_ids:
                print(f"\n📋 Available Chats:")
                for chat_id, chat_type, title in chat_ids:
                    print(f"   • {title} ({chat_type})")
                    print(f"     Chat ID: {chat_id}")
                    print(f"     Use this in config.py: TELEGRAM_CHAT_ID = \"{chat_id}\"")
                    print()
            else:
                print("   ℹ️ No messages found")
                print("   📝 Send a message to your bot first, then run this again")
        else:
            print("   ℹ️ No updates available")
            print("   📝 Send /start to your bot, then run this again")
    
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
    
    print("\n" + "=" * 60)
    print("📝 QUICK FIXES:")
    print("1. For CHANNEL: Add bot as admin with 'Post Messages' permission")
    print("2. For PERSONAL: Send /start to your bot first")
    print("3. For GROUP: Add bot to group, then get group ID")
    print("4. Use numeric ID instead of @username (more reliable)")

if __name__ == "__main__":
    debug_telegram()
