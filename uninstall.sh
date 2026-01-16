#!/bin/bash
echo "[+] Uninstalling ECHTABLE..."

# Remove installation files
sudo rm -rf /usr/share/echtable 2>/dev/null
sudo rm -f /usr/bin/echtable 2>/dev/null
sudo rm -f /usr/bin/echt 2>/dev/null

# Remove user data if requested
if [[ "$1" == "--purge" ]] || [[ "$1" == "-p" ]]; then
    echo "[*] Removing user data..."
    rm -rf ~/.echtable 2>/dev/null
    echo "[✓] User data removed"
fi

# Verify uninstallation
if ! command -v echtable &> /dev/null; then
    echo "[✓] ECHTABLE successfully uninstalled"
else
    echo "[!] Warning: echtable command still found"
fi

echo "[*] Note: To reinstall, run: sudo bash installer/install.sh"
