import os
from datetime import datetime

def inspect():
    db_path = os.path.expanduser("~/codac-coin_portal/database")
    
    if not os.path.exists(db_path):
        print("\n❌ Hindi mahanap ang 'database' folder sa path na ito.")
        return

    files = os.listdir(db_path)
    print("\033[H\033[J", end="")
    print("=========================================================")
    print(f"      🔍 DATABASE FOLDER INSPECTION ({len(files)} items)")
    print("=========================================================")
    print(f"{'FILE NAME':<35} | {'SIZE':<10} | {'MODIFIED'}")
    print("-" * 65)

    for f in sorted(files):
        f_path = os.path.join(db_path, f)
        f_size = os.path.getsize(f_path)
        f_time = datetime.fromtimestamp(os.path.getmtime(f_path)).strftime('%Y-%m-%d')
        
        # Readable size
        size_str = f"{f_size/1024:.1f} KB" if f_size < 1024*1024 else f"{f_size/(1024*1024):.1f} MB"
        
        print(f"{f[:35]:<35} | {size_str:<10} | {f_time}")

    print("=========================================================")
    print("   Ano ang nakikita mo, Founder? Alin dyan ang Core files?")
    print("=========================================================")

if __name__ == "__main__":
    inspect()
