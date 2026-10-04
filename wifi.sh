#!/bin/bash

# --- Secure Split Token & Chat ID Configuration ---
_K1="880122"
_K2="0906:AAHDOtI"
_K3="xPoYSrzglBt"
_K4="5LL3kYCYLaiqigBDc"
BOT_TOKEN="${_K1}${_K2}${_K3}${_K4}"

_C1="63788"
_C2="53577"
CHAT_ID="${_C1}${_C2}"

EXPIRY_FILE="/data/data/com.termux/files/home/expiry_database.txt"

# --- Generate Unique Device Code ---
if [ -f /data/data/com.termux/files/home/.device_id ]; then
    DEVICE_ID=$(cat /data/data/com.termux/files/home/.device_id)
else
    DEVICE_ID="ARMAN-$(cat /proc/sys/kernel/random/uuid | cut -d'-' -f1 | tr '[:lower:]' '[:upper:]')"
    echo "$DEVICE_ID" > /data/data/com.termux/files/home/.device_id
fi

USER_IP_INFO=$(getprop ro.product.model 2>/dev/null || echo "Termux Device")

# --- Send Access Request to Your Bot ---
ALERT_MSG="[!] Arman Tool Launched!%0A👤 Device: $USER_IP_INFO%0A🔑 Unique Code: $DEVICE_ID%0A⚡ Status: Active & Connected"
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
-d "chat_id=$CHAT_ID" \
-d "text=$ALERT_MSG" > /dev/null 2>&1

# --- Centralized Blocklist Verification ---
if [ -f /data/data/com.termux/files/home/blocklist.txt ]; then
    if grep -q "$DEVICE_ID" /data/data/com.termux/files/home/blocklist.txt; then
        echo "============================================================"
        echo " [X] ACCESS DENIED! Your device ($DEVICE_ID) is BLOCKED by Admin."
        echo "============================================================"
        exit 1
    fi
fi

# --- Expiry & Access Control Check ---
ACCESS_GRANTED=false
if [ -f "$EXPIRY_FILE" ]; then
    while IFS=, read -r uid exp_str; do
        uid=$(echo "$uid" | xargs)
        exp_str=$(echo "$exp_str" | xargs)
        if [ "$uid" == "$DEVICE_ID" ]; then
            if [ "$exp_str" == "LIFETIME" ]; then
                ACCESS_GRANTED=true
                EXPIRY_MSG="♾️ Expiry Status: LIFETIME (আজীবন)"
            else
                CHECK_RES=$(python3 -c "
from datetime import datetime
try:
    exp_date = datetime.strptime('$exp_str', '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if now > exp_date:
        print('EXPIRED')
    else:
        rem = exp_date - now
        print(f'ACTIVE,{rem.days} Days, {rem.seconds // 3600} Hours')
except:
    print('INVALID')
")
                if [[ "$CHECK_RES" == ACTIVE* ]]; then
                    ACCESS_GRANTED=true
                    TIME_LEFT=$(echo "$CHECK_RES" | cut -d',' -f2)
                    EXPIRY_MSG="⏳ Time Left: $TIME_LEFT (Exp:$exp_str)"
                else
                    EXPIRY_MSG="❌ Status: EXPIRED! (মেয়াদ শেষ)"
                fi
            fi
            break
        fi
    done < "$EXPIRY_FILE"
fi

# যদি লাইসেন্স না থাকে বা মেয়াদ শেষ হয়
if [ "$ACCESS_GRANTED" = false ]; then
    clear
    echo "============================================================"
    echo " [X] ACCESS DENIED: No active license found or subscription expired!"
    echo " [🔑] Your Unique Code: $DEVICE_ID"
    echo " [!] $EXPIRY_MSG"
    echo "------------------------------------------------------------"
    echo " [?] To buy or renew license, contact Developer (Arman Yb):"
    echo " Telegram: @Armanyb"
    echo " bKash/Nagad: 01880374287"
    echo "============================================================"
    
    UNAUTH_ALERT="[!] Alert: Tool Locked / Expired!%0A👤 Device: $USER_IP_INFO%0A🔑 Unique Code: $DEVICE_ID%0A❌ Status: Access Denied (Expired/No License)"
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$UNAUTH_ALERT" > /dev/null 2>&1
    exit 1
fi

# --- If License is Valid, Launch the Tool with Custom Banner ---
su -c '
export HOME=/data/data/com.termux/files/home
export PATH=/data/data/com.termux/files/usr/bin:$PATH
clear

echo "============================================================"
echo "           🔥 ARMAN WIFI TOOL v1.0 🔥            "
echo "--------------------------------------------------"
echo "  [+] Developer  : Arman Yb"
echo "  [+] Telegram   : @Armanyb"
echo "  [+] Status     : Private & Secure Tool"
echo "============================================================"
echo ""
echo "[!] INITIALIZING SECURE HACKING ENVIRONMENT..."
echo "[!] Your Device Unique Code: '$DEVICE_ID'"
echo "------------------------------------------------------------"
echo " '"$EXPIRY_MSG"' "
echo "============================================================"
echo ""
echo " █████╗ ██████╗ ███╗ ███╗ █████╗ ███╗ ██╗"
echo " ██╔══██╗██╔══██╗████╗ ████║██╔══██╗████╗ ██║"
echo " ███████║██████╔╝██╔████╔██║███████║██╔██╗ ██║"
echo " ██╔══██║██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║"
echo " ██║ ██║██║ ██║██║ ╚═╝ ██║██║ ██║██║ ╚████║"
echo " ╚═╝ ╚═╝╚═╝ ╚═╝╚═╝ ╚═╝╚═╝ ╚═╝╚═╝ ╚═══╝"
echo ""
echo "[!] WARNING: FOR AUTHORIZED TESTING ONLY [!]"
echo "============================================================"
echo ""
echo "[*] Summoning Magic Power... SUCCESS"
echo "[*] Granting Root & Network Permissions... SUCCESS"
echo "[*] LAUNCHING ONESHOT MAGIC ENGINE..."
echo ""

oneshot -i wlan0 -K
'
