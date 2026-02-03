import csv
import os

FILE_PATH = "cdc_wallets_thirdweb.csv"

def inspect():
    print("\033[H\033[J", end="")
    print(f"Checking file: {FILE_PATH}...")
    
    if not os.path.exists(FILE_PATH):
        print("❌ File not found! Hanapin natin sa ibang folder?")
        return

    try:
        with open(FILE_PATH, "r") as f:
            lines = f.readlines()
            
        print(f"📊 Total Lines Found: {len(lines)}")
        print("-" * 50)
        
        # Show First 10 lines (Header + Data)
        for i, line in enumerate(lines[:10]):
            print(f"Line {i+1}: {line.strip()}")
            
        print("-" * 50)
        print("👆 Yan ba ang listahan ng 204 Countries mo?")
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    inspect()
