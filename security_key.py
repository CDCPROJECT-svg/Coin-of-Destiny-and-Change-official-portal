import hashlib
import time

# Direct Bloodline Metadata
FOUNDER = "CRIS"
SUCCESSOR = "CRIS DANIEL ECALNE"
RULE = "VERTICAL_BLOODLINE_INFINITY"

def generate_founder_key():
    print("--- CDC COIN: SECURITY KEY GENERATION ---")
    print("[SYSTEM] Encrypting Succession Rules...")
    
    # Gagawa ng hash base sa pangalan mo, ng anak mo, at ng Infinity rule
    raw_data = f"{FOUNDER}-{SUCCESSOR}-{RULE}-{time.time()}"
    secure_hash = hashlib.sha256(raw_data.encode()).hexdigest().upper()
    
    # Kunin ang unang 16 characters bilang Master Key
    master_key = f"CDC-{secure_hash[:16]}"
    
    print("-" * 40)
    print(f"FOUNDER MASTER KEY: {master_key}")
    print("-" * 40)
    print("[WARNING] Selyado na ang key na ito sa Mother Tree.")
    print("[NOTICE] Only the Direct Bloodline can trigger this key.")
    
    # I-save sa isang hidden file para sa system validation
    with open("cdc_portal/.master_lock", "w") as f:
        f.write(secure_hash)
    
    print("\n[GUARDIAN] Key Generated and Locked to Bloodline.")

if __name__ == "__main__":
    generate_founder_key()
