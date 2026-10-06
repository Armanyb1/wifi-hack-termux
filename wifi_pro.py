import sys
import os

if __name__ == "__main__":
    try:
        print("[*] Tool is running... Press Ctrl+C to exit safely.")
        
        # তোর ওয়াইফাই টুল রান করার আসল কমান্ড
        os.system('su -c "export PATH=$PATH:/data/data/com.termux/files/usr/bin; oneshot -i wlan0 -K"')
        
    except KeyboardInterrupt:
        # এই লাইনটাই কিবোর্ড হ্যাং ঠিক করবে এবং টুল পুরোপুরি বন্ধ করে দেবে
        os.system('stty sane')
        print("\n\n[!] Tool closed safely by user. Terminal is back to normal. Have a nice day!")
        sys.exit(0)
