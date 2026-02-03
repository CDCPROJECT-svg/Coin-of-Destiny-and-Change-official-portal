import hashlib
import secrets

# This generates a 24-word recovery sequence
def generate_recovery_seed():
    # In a real system, we use a BIP-39 wordlist
    # For this Termux logic, we will generate a secure hex-key
    recovery_token = secrets.token_hex(32)
    print("\n⚠️  CRITICAL: FOUNDER RECOVERY KEY ⚠️")
    print("------------------------------------------")
    print(f"KEY: {recovery_token}")
    print("------------------------------------------")
    print("IF YOUR PHONE IS LOST, THIS IS THE ONLY WAY TO REGAIN CONTROL.")
    print("WRITE THIS DOWN ON PAPER. DO NOT SCREENSHOT.")
    
    # Store the HASH only, so even if the DB is hacked, they can't see the key
    hashed_token = hashlib.sha256(recovery_token.encode()).hexdigest()
    return hashed_token

if __name__ == "__main__":
    token_hash = generate_recovery_seed()
    # Save token_hash to your secure config...
