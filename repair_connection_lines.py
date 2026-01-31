import sqlite3
import os

class NetworkRepairman:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    def fix_connections(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\033[H\033[J", end="")
        print("=========================================================")
        print("      🔧 NETWORK CONNECTION REPAIR")
        print("      Task: Re-attach disconnected nodes to Founder")
        print("=========================================================")

        # 1. GET THE LISTS (HIERARCHY)
        root = "FOUNDER-001"
        
        # A. VIPs (Not Founder, Not Country, Not Public, Not Wallet)
        cursor.execute("""
            SELECT user_id FROM active_members 
            WHERE user_id != ? 
            AND user_id NOT LIKE 'CODAC-A09L%' 
            AND status != 'PUBLIC_MEMBER'
            AND user_id NOT IN ('COLLECTOR-001', 'RESERVE-WALLET', 'BURN-WALLET')
            ORDER BY user_id ASC
        """, (root,))
        vips = [r[0] for r in cursor.fetchall()]
        
        # B. Countries
        cursor.execute("SELECT user_id FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY user_id ASC")
        countries = [r[0] for r in cursor.fetchall()]
        
        # C. Public (Juan)
        cursor.execute("SELECT user_id FROM active_members WHERE status='PUBLIC_MEMBER'")
        public = [r[0] for r in cursor.fetchall()]

        print(f" [📊] NODES FOUND:")
        print(f"      - VIPs: {len(vips)}")
        print(f"      - Countries: {len(countries)}")
        print(f"      - Public: {len(public)}")

        # 2. START LINKING: FOUNDER -> VIPS
        print("\n [1] Linking VIPs to Founder...")
        parent_queue = [root]
        
        # We process VIPs and add them to queue so Countries can attach to them later
        node_index = 0
        while node_index < len(vips) and parent_queue:
            parent = parent_queue.pop(0)
            
            # Left
            if node_index < len(vips):
                child = vips[node_index]
                cursor.execute("UPDATE active_members SET parent_id=?, position='LEFT' WHERE user_id=?", (parent, child))
                # Add back to queue (end) so it becomes a parent for next layer
                parent_queue.append(child) 
                node_index += 1
                
            # Right
            if node_index < len(vips):
                child = vips[node_index]
                cursor.execute("UPDATE active_members SET parent_id=?, position='RIGHT' WHERE user_id=?", (parent, child))
                parent_queue.append(child)
                node_index += 1

        # NOTE: At this point, parent_queue contains the bottom-most VIPs.
        # We will attach Countries to THEM.
        
        # 3. LINKING: VIPs -> COUNTRIES
        print(" [2] Linking Countries to Bottom VIPs...")
        # Reuse parent_queue (it has the last layer of VIPs)
        
        country_index = 0
        while country_index < len(countries) and parent_queue:
            parent = parent_queue.pop(0)
            
            # Connect Country Left
            if country_index < len(countries):
                child = countries[country_index]
                cursor.execute("UPDATE active_members SET parent_id=?, position='AUTO' WHERE user_id=?", (parent, child))
                # We DON'T add countries to queue for general filling, 
                # unless we want countries to parent other countries. 
                # Ideally, countries are ANCHORS.
                country_index += 1
            
            # Connect Country Right
            if country_index < len(countries):
                child = countries[country_index]
                cursor.execute("UPDATE active_members SET parent_id=?, position='AUTO' WHERE user_id=?", (parent, child))
                country_index += 1

        # 4. SPECIAL CASE: JUAN -> PHILIPPINES
        print(" [3] Linking Public Members to Countries...")
        # Find Philippines
        cursor.execute("SELECT user_id FROM active_members WHERE user_id LIKE '%Phi%' LIMIT 1")
        ph_node = cursor.fetchone()
        
        if ph_node and public:
            ph_id = ph_node[0]
            juan = public[0] # Assuming Juan is the first public member
            cursor.execute("UPDATE active_members SET parent_id=? WHERE user_id=?", (ph_id, juan))
            print(f"      -> Attached {juan} to {ph_id}")
            
        conn.commit()
        conn.close()

        print("-" * 57)
        print(" [✅] REPAIR COMPLETE.")
        print("      Try opening the Explorer Tree again.")
        print("=========================================================")

if __name__ == "__main__":
    fixer = NetworkRepairman()
    fixer.fix_connections()
