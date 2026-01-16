#!/bin/bash
echo "[+] Testing ECHTABLE..."

# 1. Framework startup test
timeout 2 echtable <<< "exit" && echo "✅ Framework starts OK" || echo "❌ Framework startup failed"

# 2. Help command test
echo "Testing help command..."
echtable <<< "help" | grep -q "ECHTABLE Framework" && echo "✅ Help command works" || echo "❌ Help command failed"

# 3. Variable test
echo "Testing variable operations..."
echtable <<< "set @test_target 192.168.1.1" 2>&1 | grep -q "Variable set" && echo "✅ Variable set works" || echo "❌ Variable set failed"

echo "[✓] Basic tests completed"
