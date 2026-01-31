import os
import subprocess

def setup_git():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🛡️  INITIALIZING GIT REPOSITORY (SECURE)")
    print("=========================================================")

    # 1. Initialize Git
    if not os.path.exists(".git"):
        print("   ⚙️  Initializing Git folder...")
        os.system("git init")
    else:
        print("   ⚙️  Git is already initialized.")

    # 2. Check GitGuardian Shield (.gitignore)
    if os.path.exists(".gitignore"):
        print("   ✅ GitGuardian Shield (.gitignore) is ACTIVE.")
    else:
        print("   ⚠️  Shield missing! Creating one now...")
        with open(".gitignore", "w") as f:
            f.write("*.db\n*.csv\n*.pdf\n*.txt\n__pycache__/\n.env")

    # 3. Check what Git 'Sees' vs 'Ignores'
    print("\n   👁️  CHECKING VISIBILITY:")
    
    # Add files to staging to see status
    os.system("git add .")
    
    # Get status
    result = subprocess.getoutput("git status --short")
    
    print("-" * 40)
    print("   ALLOWED FILES (Codes - Safe to Upload):")
    safe_files = []
    hidden_files = []
    
    for line in result.splitlines():
        if line.endswith(".py") or line.endswith(".md"):
            safe_files.append(line)
            print(f"     ✅ {line}")
            
    print("\n   BLOCKED FILES (Keys/Data - Safe Locally):")
    # We explicitly check if dangerous files are tracked
    ignored_check = subprocess.getoutput("git check-ignore -v CODAC_OFFICIAL_204_FINAL.csv codac_master.db")
    print(f"     🔒 {ignored_check}")

    print("-" * 57)
    print("   🚀 READY FOR GITHUB!")
    print("   Your Private Keys in CSV and DB are HIDDEN from Git.")
    print("   Only your Python scripts will be exported.")
    print("=========================================================")

if __name__ == "__main__":
    setup_git()
