import json

def generate_ids():
    # 0001 and 0002 are Treasury and Reserve
    ids = {
        "256": "CODAC-C1A0001AIOIN", # Treasury
        "257": "CODAC-C1A0002AIOIN"  # Reserve
    }
    
    # 258 to 461 are the 204 Countries
    for i in range(258, 462):
        country_num = i - 257 + 2 # Offsetting to start after 0002
        formatted_id = f"CODAC-C1A{country_num:04d}AIOIN"
        ids[str(i)] = formatted_id

    with open('binary_core/aioin_master_list.json', 'w') as f:
        json.dump(ids, f, indent=4)
    print(f"✅ Master ID list created for 204 countries.")

generate_ids()
