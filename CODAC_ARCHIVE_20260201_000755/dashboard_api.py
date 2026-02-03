import json
from main_engine import CODACEngine

def get_founder_stats():
    engine = CODACEngine()
    stats = []
    
    # Kinakalkula ang 18 Projects
    for p_id in range(1, 19):
        # Base reward logic mula sa main_engine.py
        reward = engine.calculate_reward(cycle=1, project_id=p_id)
        deduction = engine.get_deduction(p_id)
        
        stats.append({
            "project_id": p_id,
            "reward": reward,
            "net_limit": round(reward * (1 - deduction), 2),
            "daily_withdrawal": round(reward * engine.withdrawal_limit, 2)
        })
    
    return stats

if __name__ == "__main__":
    # Sinisave ang data para mabasa ng Dashboard mo
    with open('live_stats.json', 'w') as f:
        json.dump(get_founder_stats(), f, indent=4)
    print("Dashboard Data Updated: live_stats.json is ready.")
