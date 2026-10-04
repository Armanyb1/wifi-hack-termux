import urllib.request
from datetime import datetime
import os
import ssl

# গিটহাবের রফ (Raw) ডেটাবেজ লিংক
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Armanyb1/wifi-hack-termux/main/expiry_database.txt"
LOCAL_EXPIRY_FILE = "expiry_database.txt"
DEVICE_ID_FILE = ".device_id"

# তোর টেলিগ্রাম বট টোকেন এবং চ্যাট আইডি
BOT_TOKEN = "8443437373:AAElo2WYed5wTdZslN1Pm3ttnEs_Y4G7TIs"
CHAT_ID = "5940676703"

def get_or_create_device_id():
    if os.path.exists(DEVICE_ID_FILE):
        with open(DEVICE_ID_FILE, "r") as f:
            return f.read().strip()
    else:
        import uuid
        new_id = "ARMAN-" + str(uuid.uuid4()).split('-')[0].upper()
        with open(DEVICE_ID_FILE, "w") as f:
            f.write(new_id)
        return new_id

def print_banner(device_id, expiry_status="LIFETIME (আজীবন)"):
    print("=" * 65)
    print("          🔥 ARMAN WIFI TOOL v1.0 🔥")
    print("=" * 65)
    print(" [+] Developer  : Arman Yb")
    print(" [+] Telegram   : @Armanyb")
    print(" [+] Status     : Private & Secure Tool")
    print("=" * 65)
    print(" [!] INITIALIZING SECURE HACKING ENVIRONMENT...")
    print(f" [!] Your Device Unique Code: {device_id}")
    print("-" * 65)
    print(f" ♾️  Expiry Status: {expiry_status}")
    print("=" * 65)
    print("      A R M A N      ")
    print("-" * 65)
    print(" [!] WARNING: FOR AUTHORIZED TESTING ONLY [!]")
    print("=" * 65)

def check_online_license(device_id):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.urlopen(GITHUB_RAW_URL, timeout=5, context=ctx)
        content = req.read().decode('utf-8')
        
        with open(LOCAL_EXPIRY_FILE, "w") as f:
            f.write(content)

        for line in content.splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 2:
                stored_id, expiry = parts[0], parts[1]
                if stored_id == device_id:
                    if expiry.upper() == "LIFETIME":
                        return True, "LIFETIME (আজীবন)"
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() <= expiry_date:
                        return True, expiry
            elif line.strip().startswith(device_id):
                return True, "LIFETIME (আজীবন)"
        return False, "Expired/Invalid"
    except Exception as e:
        print(f"[!] Network Error Details: {e}")
        return False, "Error"

if __name__ == "__main__":
    my_device_id = get_or_create_device_id()
    print(f"[*] Your Device ID: {my_device_id}")
    print("[*] Connecting to GitHub to verify license...")
    
    is_valid, expiry_info = check_online_license(my_device_id)
    
    if is_valid:
        print("[+] License Verified Successfully! Welcome, Boss!")
        
        # সফল ভেরিফিকেশনের পর ব্যানার প্রিন্ট হবে
        print_banner(my_device_id, expiry_info)
        
        # সফল লঞ্চের পর টেলিগ্রামে নোটিফিকেশন পাঠানো
        USER_IP_INFO = "Termux Android Device"
        alert_msg = f"[!] Arman Tool Launched!%0A👤 Device: {USER_IP_INFO}%0A🔑 Unique Code: {my_device_id}%0A⚡ Status: Active & Connected"
        os.system(f'curl -s -X POST "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" -d "chat_id={CHAT_ID}" -d "text={alert_msg}" > /dev/null 2>&1')
        
        # মূল ওয়াইফাই টুল ইঞ্জিন রান করার সঠিক কমান্ড (পাথ ফিক্সসহ)
        os.system('su -c "export PATH=\$PATH:/data/data/com.termux/files/usr/bin; oneshot -i wlan0 -K"')
    else:
        print("[-] Access Denied! Invalid or Expired License.")
        
        # মেয়াদ শেষ বা ব্লক হলে টেলিগ্রামে অ্যালার্ট পাঠানো
        unauth_alert = f"[!] Alert: Tool Locked / Expired!%0A👤 Device: Termux Device%0A🔑 Unique Code: {my_device_id}%0A❌ Status: Access Denied (Expired/No License)"
        os.system(f'curl -s -X POST "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" -d "chat_id={CHAT_ID}" -d "text={unauth_alert}" > /dev/null 2>&1')
