#!/usr/bin/env bash
set -e

echo "[+] Installing ECHTABLE"

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="/usr/share/echtable"
BIN_ECHTABLE="/usr/bin/echtable"
BIN_ECHT="/usr/bin/echt"

# Clean install
sudo rm -rf "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"

# Copy files
echo "[*] Copying files..."
sudo cp -r "$BASE_DIR/core" "$INSTALL_DIR/"
sudo cp -r "$BASE_DIR/cli" "$INSTALL_DIR/"
sudo cp "$BASE_DIR/echtable.py" "$INSTALL_DIR/"

# Create echtable binary (Framework)
sudo tee "$BIN_ECHTABLE" > /dev/null <<'BINARY_EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/share/echtable')

from echtable import start_framework

if __name__ == "__main__":
    start_framework()
BINARY_EOF

# Create echt binary (Fast CLI)
sudo tee "$BIN_ECHT" > /dev/null <<'BINARY_EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/share/echtable')

from cli.non_interactive import main

if __name__ == "__main__":
    sys.exit(main())
BINARY_EOF

sudo chmod +x "$BIN_ECHTABLE"
sudo chmod +x "$BIN_ECHT"

# Create user data directory
mkdir -p ~/.echtable

echo "[✓] ECHTABLE installed successfully"
echo "[*] Commands:"
echo "    echtable    # Interactive framework"
echo "    echt        # Fast CLI"
echo ""
echo "[*] Examples:"
echo "    echt set @target 10.10.10.5"
echo "    echt create slot \"nmap -sV @target\" --name scan"
echo "    echt run 1"
echo "    echtable    # For interactive use"
