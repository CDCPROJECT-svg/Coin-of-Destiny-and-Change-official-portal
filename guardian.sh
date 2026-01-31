#!/data/data/com.termux/files/usr/bin/bash

# 1. Load the Keys
if [ -f .env ]; then
    source .env
else
    echo "❌ CRITICAL ERROR: .env file missing. Guardian cannot verify identity."
    exit 1
fi

# 2. Identity Verification
PROTECTED="xzbozofttuvyijeimxkj"

if [ "$PROJECT_ID" != "$PROTECTED" ]; then
    echo "❌ SECURITY ALERT: Project ID mismatch ($PROJECT_ID). Operation Blocked."
    exit 1
fi

# 3. Safe Execution Function
execute_portal_task() {
    echo "⚠️  GUARDIAN: You are about to modify the 28-level binary for $PROJECT_ID."
    read -p "Type 'CONFIRM' to proceed: " confirm
    if [ "$confirm" == "CONFIRM" ]; then
        echo "✅ Identity Verified. Executing..."
        python3 -c "$1"
    else
        echo "🚫 Operation Cancelled by Founder."
    fi

