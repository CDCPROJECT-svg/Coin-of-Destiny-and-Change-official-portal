import math

def get_position_details(member_count):
    # Total members already in system = N
    # Next member is N + 1
    next_id = member_count + 1
    
    # Calculate Level (Level 0 is the Root)
    level = math.floor(math.log2(next_id))
    
    # Calculate Position in that Level
    pos_in_level = next_id - (2**level)
    
    print(f"🚀 GLOBAL FILLER STATUS")
    print(f"Current Total: {member_count}")
    print(f"Next Member ID: CODAC-C1A{str(next_id).zfill(4)}AIOIN")
    print(f"Target Level: {level}")
    print(f"Position: {pos_in_level + 1} of {2**level}")
    
    if level >= 20:
        print("🏆 LEVEL 20 REACHED - PROJECT SUCCESSION TRIGGERED")

# Example: If you have 1023 members, the next one fills Level 10
get_position_details(1023)
