# CDC INFINITY FEEDING: INTERVAL MANAGEMENT PILLARS
def calculate_feeding(project_id, current_max_level):
    print(f"--- Project {project_id} Feeding Status ---")
    
    # Ang Management Account ay papasok lang every 21 levels
    # 21, 42, 63, 84... pataas nang pataas
    for level in range(1, current_max_level + 1):
        if level % 21 == 0:
            pillar_num = level // 21
            print(f"[PILLAR] Management Account #{pillar_num} activated at Level {level}")
        
    print(f"[OK] Feeding synchronized for 28 levels and beyond.\n")

# Awtomatikong i-apply sa 18 Projects
for p in range(1, 19):
    calculate_feeding(p, 28) # Default is 28, but scalable to infinity

print("[GUARDIAN] Interval Feeding System: ONLINE.")

