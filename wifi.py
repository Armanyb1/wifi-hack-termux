import urllib.request
from datetime import datetime
import os
import ssl
import time

GITHUB_RAW_URL = "https://raw.githubusercontent.com/Armanyb1/wifi-hack-termux/main/expiry_database.txt"
LOCAL_EXPIRY_FILE = "expiry_database.txt"
DEVICE_ID_FILE = os.path.expanduser("~/.arman_device_id")

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

def print_banner(device_id, expiry_status="LIFETIME (Ajobon)"):
    print("\033[1;36m" + "=" * 65 + "\033[0m")
    print("\033[1;32m          🔥 ARMAN ADVANCED WIFI SECURITY TOOL v2.5 🔥          \033[0m")
    print("\033[1;36m" + "=" * 65 + "\033[0m")
    print(" [\033[1;33m+\033[0m] Developer    : Arman Yb (Cyber Security Expert)")
    print(" [\033[1;33m+\033[0m] Telegram     : @Armanyb")
    print(" [\033[1;33m+\033[0m] Tool Status  : Pro Edition | Authorized & Secure")
    print("\033[1;36m" + "=" * 65 + "\033[0m")
    print(" [\033[1;31m!\033[0m] INITIALIZING ADVANCED ENCRYPTION & PACKET INJECTION...")
    print(f" [\033[1;32m✓\033[0m] Device Unique Code : \033[1;33m{device_id}\033[0m")
    print("\033[1;36m" + "-" * 65 + "\033[0m")
    print(f" ♾️  License Status   : \033[1;32m{expiry_status}\033[0m")
    print("\033[1;36m" + "=" * 65 + "\033[0m")
    print("                  [ A R M A N   Y B   S E C U R I T Y ]                  ")
    print("\033[1;36m" + "-" * 65 + "\033[0m")
    print(" [\033[1;31m!\033[0m] WARNING: FOR AUTHORIZED WIRELESS PENETRATION TESTING ONLY [!]")
    print("\033[1;36m" + "=" * 65 + "\033[0m")

def check_online_license(device_id):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        live_url = f"{GITHUB_RAW_URL}?v={int(time.time())}"
        
        req = urllib.request.urlopen(live_url, timeout=5, context=ctx)
        content = req.read().decode('utf-8')
        
        with open(LOCAL_EXPIRY_FILE, "w") as f:
            f.write(content)

        for line in content.splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            
            clean_line = line.replace('=', ',')
            parts = [p.strip() for p in clean_line.split(',')]
            
            if len(parts) >= 2:
                stored_id, expiry = parts[0], parts[1]
                if stored_id.upper() == device_id.upper():
                    if expiry.upper() == "LIFETIME":
                        return True, "LIFETIME (Ajobon)"
                    try:
                        expiry_date = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
                        if datetime.now() <= expiry_date:
                            return True, expiry
                    except:
                        pass
            elif line.strip().upper().startswith(device_id.upper()):
                return True, "LIFETIME (Ajobon)"
                
        return False, "Expired/Invalid"
    except Exception as e:
        print(f"[\033[1;31m!\033[0m] Network Error Details: {e}")
        return False, "Error"

if __name__ == "__main__":
    try:
        my_device_id = get_or_create_device_id()
        print(f"[*] Your Permanent Device ID: {my_device_id}")
        print("[*] Connecting to GitHub Server to verify license...")
        
        is_valid, expiry_info = check_online_license(my_device_id)
        
        if is_valid:
            print("[+] License Verified Successfully! Welcome, Boss!")
            print_banner(my_device_id, expiry_info)
            
            alert_msg = f"[!] Arman Tool Launched!%0A👤 Device: Termux Android%0A🔑 Unique Code: {my_device_id}%0A⚡ Status: Active & Connected"
            os.system(f'curl -s -X POST "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" -d "chat_id={CHAT_ID}" -d "text={alert_msg}" > /dev/null 2>&1')
            
            os.system('su -c "export PATH=$PATH:/data/data/com.termux/files/usr/bin; oneshot -i wlan0 -K"')
        else:
            print("\n\033[1;31m" + "=" * 65 + "\033[0m")
            print("\033[1;31m           ❌ ACCESS DENIED - LICENSE REQUIRED ❌           \033[0m")
            print("\033[1;31m" + "=" * 65 + "\033[0m")
            print(" [!] Apnar device-ti active na ba license-er meyad shesh!")
            print(f" [!] Apnar Device ID: \033[1;33m{my_device_id}\033[0m")
            print("-" * 65)
            print(" [💡 Tool Activate Korar Niyom:]")
            print("  1. Upore dewa Device ID ti copy korun ba screenshot nin.")
            print("  2. Payment korun (Bkash Personal): 01880374287")
            print("     • 7 Din: 100 Taka")
            print("     • 1 Mas: 330 Taka")
            print("     • Lifetime: 700 Taka")
            print("  3. Telegram-e jogajog korun:")
            print("     • Username: \033[1;36m@Armanyb\033[0m")
            print("     • Link: \033[1;36mhttps://t.me/Armanyb\033[0m" )
            print("     Device ID o payment-er screenshot pathiye license activate kore nin.")
            print("\033[1;31m" + "=" * 65 + "\033[0m")
            
            unauth_alert = f"[!] Alert: Tool Locked / Expired!%0A👤 Device: Termux Device%0A🔑 Unique Code: {my_device_id}%0A❌ Status: Access Denied (Expired/No License)"
            os.system(f'curl -s -X POST "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" -d "chat_id={CHAT_ID}" -d "text={unauth_alert}" > /dev/null 2>&1')
            
    except KeyboardInterrupt:
        os.system('stty sane')
        print("\n\n[!] Tool closed safely by user. Terminal is back to normal. Have a nice day!")
