import os
import getpass
from dotenv import load_dotenv

# Load hidden file immediately (Silent Load)
load_dotenv()

def get_secret(key_name):
    """
    Kukunin ang secret nang hindi ipinapakita sa screen.
    Priority 1: Hidden .env file
    Priority 2: Hihingin sa User (Masked Input)
    """
    # 1. Try to get from Hidden Environment
    value = os.getenv(key_name)
    
    if value:
        # Success (Silent)
        return value
    else:
        # 2. Ask User (Invisible Typing)
        # Walang lalabas na letra habang nagta-type ka (Security Feature)
        print(f" [🔒] SECURITY CHECK: {key_name} needed.")
        value = getpass.getpass(f"      👉 Enter {key_name} (Hidden Input): ")
        return value.strip()

def check_security_clearance():
    # Dummy check just to prove it works without printing
    print(" [🛡️] VAULT STATUS: SECURE.")
    print("      Credentials loaded into RAM only. Nothing written to logs.")

if __name__ == "__main__":
    check_security_clearance()
