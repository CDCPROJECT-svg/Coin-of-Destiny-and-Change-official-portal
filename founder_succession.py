import hashlib
import time
from datetime import datetime
import os
import json
from math import radians, sin, cos, sqrt, atan2

# ==============================
# DIRECT BLOODLINE METADATA
# ==============================
FOUNDER = "CRIS"
SUCCESSOR = [
    "CRIS DANIEL ECALNE",
    "SUCCESSOR_2",
    "SUCCESSOR_3",
]
RULE = "VERTICAL_BLOODLINE_INFINITY"
MASTER_KEY_FILE = "codac_portal/.master_lock"
BIRTH_CERT_FILE = "codac_portal/birth_cert_successor.txt"  # optional

# ==============================
# AUTOMATED INCOME SOURCES
# ==============================
PORTAL_INCOME_FILE = "codac_portal/portal_income.json"
BLOCKCHAIN_INCOME_FILE = "codac_portal/blockchain_income.json"

# ==============================
# BURIAL SITE GEOLOCATION
# ==============================
REQUIRED_LAT = 14.5995  # example latitude
REQUIRED_LON = 120.9842 # example longitude
LOCATION_TOLERANCE_KM = 1  # within 1 km radius
SUCCESSOR_LOCATION_FILE = "codac_portal/successor_location.json"

# ==============================
# ATTENDANCE RECORDS
# ==============================
VISIT_RECORD_FILE = "codac_portal/visit_record.json"

# ==============================
# HELPER FUNCTIONS
# ==============================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return R * c  # distance in km

def all_successors_present():
    if not os.path.exists(SUCCESSOR_LOCATION_FILE):
        print("[WARNING] Successor location file not found. Cannot verify presence.")
        return False

    with open(SUCCESSOR_LOCATION_FILE, "r") as f:
        locations = json.load(f)

    for name in SUCCESSOR:
        if name not in locations:
            print(f"❌ {name} location missing.")
            return False
        lat, lon = locations[name]["lat"], locations[name]["lon"]
        distance = haversine(lat, lon, REQUIRED_LAT, REQUIRED_LON)
        if distance > LOCATION_TOLERANCE_KM:
            print(f"❌ {name} is not at the burial site (distance: {distance:.2f} km).")
            return False
    return True

def update_visit_record(year):
    if os.path.exists(VISIT_RECORD_FILE):
        with open(VISIT_RECORD_FILE, "r") as f:
            record = json.load(f)
    else:
        record = {name: [] for name in SUCCESSOR}

    for name in SUCCESSOR:
        if year not in record[name]:
            record[name].append(year)

    with open(VISIT_RECORD_FILE, "w") as f:
        json.dump(record, f, indent=4)

def missed_dec8_consecutive(year):
    if not os.path.exists(VISIT_RECORD_FILE):
        return {name: 0 for name in SUCCESSOR}

    with open(VISIT_RECORD_FILE, "r") as f:
        record = json.load(f)

    missed = {}
    for name in SUCCESSOR:
        visits = record.get(name, [])
        count = 0
        for y in range(year-2, year+1):  # check last 3 years
            if y not in visits:
                count += 1
        missed[name] = count
    return missed

# ==============================
# FETCH TOTAL INCOME
# ==============================
def fetch_total_income():
    total_income = 0.0
    if os.path.exists(PORTAL_INCOME_FILE):
        with open(PORTAL_INCOME_FILE, "r") as f:
            portal_data = json.load(f)
            total_income += portal_data.get("founder_income", 0)
            total_income += portal_data.get("cofounder_income", 0)
    if os.path.exists(BLOCKCHAIN_INCOME_FILE):
        with open(BLOCKCHAIN_INCOME_FILE, "r") as f:
            chain_data = json.load(f)
            total_income += chain_data.get("founder_income", 0)
            total_income += chain_data.get("cofounder_income", 0)
    return total_income

# ==============================
# MASTER KEY GENERATION
# ==============================
def generate_founder_key():
    print("--- CODAC COIN: SECURITY KEY GENERATION ---")
    print("[SYSTEM] Encrypting Succession Rules...")

    raw_data = f"{FOUNDER}-{''.join(SUCCESSOR)}-{RULE}-{time.time()}"
    secure_hash = hashlib.sha256(raw_data.encode()).hexdigest()

    if os.path.exists(BIRTH_CERT_FILE):
        with open(BIRTH_CERT_FILE, "rb") as f:
            birth_data = f.read()
        secure_hash = hashlib.sha256((secure_hash + birth_data.hex()).encode()).hexdigest()
        print("[INFO] Birth Certificate verified and applied.")
    else:
        print("[WARNING] Birth Certificate file not found. Skipping this layer.")

    master_key = f"CODAC-{secure_hash[:16]}"
    os.makedirs(".codac_secure", exist_ok=True)
    with open(".codac_secure/.master_lock", "w") as f:
        f.write(secure_hash)

    print("\n[GUARDIAN] Key Generated and Locked to Bloodline.")
    print(f"FOUNDER MASTER KEY: {master_key}")
    return master_key

# ==============================
# VERIFY SUCCESSOR ACCESS
# ==============================
def verify_successor(name):
    if name in SUCCESSOR:
        print(f"✅ {name} VERIFIED as legitimate successor.")
        return True
    else:
        print(f"❌ {name} is NOT authorized to withdraw.")
        return False

# ==============================
# CALCULATE WITHDRAWAL
# ==============================
def calculate_withdrawal(total_income, name):
    num_successors = len(SUCCESSOR)
    today = datetime.today()
    withdrawal = 0

    # Monthly 1% withdrawal on 8th day
    if today.day == 8 and today.month != 12:
        withdrawal = (total_income * 0.01) / num_successors
        print("💡 Monthly 1% Withdrawal Activated.")

    # Annual 8% withdrawal on Dec 8
    if today.month == 12 and today.day == 8:
        year = today.year
        # Check geolocation
        if all_successors_present():
            missed = missed_dec8_consecutive(year)
            for name in SUCCESSOR:
                if missed[name] >= 3:
                    print(f"❌ {name} missed Dec 8th bonus 3 consecutive years. No bonus this year.")
                    continue
                withdrawal = (total_income * 0.08) / num_successors
                print(f"🎉 Annual Dec 8th Bonus Activated for {name}: {withdrawal:.2f}")
            update_visit_record(year)
        else:
            print("❌ Not all successors present at burial site. Annual bonus cannot be withdrawn.")

    print(f"💰 {name} can withdraw: {withdrawal:.2f}")
    return withdrawal

# ==============================
# MAIN PANEL
# ==============================
def founder_succession_panel():
    master_key = generate_founder_key()
    print("\n--- FOUNDER SUCCESSION PANEL ---")
    name = input("Enter successor name: ").strip()

    if verify_successor(name):
        total_income = fetch_total_income()
        print(f"💎 Total Founder + Co-Founder income: {total_income}")
        calculate_withdrawal(total_income, name)
    else:
        print("[ACCESS DENIED] Only Direct Bloodline can withdraw.")

if __name__ == "__main__":
    founder_succession_panel()
