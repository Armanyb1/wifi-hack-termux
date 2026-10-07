#!/bin/bash
pkg update -y
pkg install root-repo wireless-tools wget openssl python -y
apt install -y ./oneshot.deb || dpkg -i oneshot.deb
echo "Setup completed!"
