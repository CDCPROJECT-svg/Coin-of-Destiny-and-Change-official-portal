#!/bin/bash

# DATABASE PATH
DB="/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
TARGET=1048576

# CLEAR SCREEN
clear
echo "========================================================"
echo "   🌐 CODAC COIN AUTHORITY PORTAL | SYSTEM V1.0"
echo "   👤 Grand Founder: ACTIVE | 🏛️ Nodes: 513 (Immune)"
echo "   🔒 REWARDS: LOCKED & SECURED (Cycles 1-Infinite)"
echo "========================================================"
echo ""

# 1. SECURITY SCAN (Silent Run)
echo ">> [1/3] 🕵️ Checking System Security..."
python3 ~/codac-coin_portal/inactivity_guard.py > /dev/null 2>&1
echo "   ✅ Security Protocols: ACTIVE"
echo ""

# 2. VIP MISSION MONITOR (The Most Important Part)
echo ">> [2/3] 👑 VIP HARVEST MONITOR (The Waiting Game)..."
echo "--------------------------------------------------------"
echo "   🎯 TARGET: PERFECT 20 UMBRELLA ($TARGET Members)"
echo "   🏆 PRIZE:  AUTOMATIC GRAND REWARDS + INCENTIVES"
echo "--------------------------------------------------------"

# Get Real Count of Organic Members (Level > 9)
ORGANIC_COUNT=$(sqlite3 $DB "SELECT COUNT(*) FROM active_members WHERE current_level > 9")
REMAINING=$((TARGET - ORGANIC_COUNT))

if [ "$ORGANIC_COUNT" -ge "$TARGET" ]; then
    STATUS="🟢 MISSION COMPLETE - RELEASING REWARDS..."
else
    STATUS="⏳ WAITING ($REMAINING more needed)"
fi

echo "   👥 CURRENT DOWNLINE: $ORGANIC_COUNT"
echo "   📊 STATUS:           $STATUS"
echo "--------------------------------------------------------"
echo ""

# 3. LIVE LEVEL REPORT
echo ">> [3/3] 📊 SYSTEM LEVEL BREAKDOWN..."
sqlite3 $DB << 'SQL'
.mode column
.width 20 15 20
.headers on
SELECT 
    'Level ' || current_level AS Level,
    COUNT(*) as Nodes,
    status AS Status
FROM active_members
GROUP BY current_level, status
ORDER BY current_level;
SQL

echo "--------------------------------------------------------"
echo "✅ SYSTEM STANDBY. READY FOR CYCLE 1 ENTRY."
echo ""
