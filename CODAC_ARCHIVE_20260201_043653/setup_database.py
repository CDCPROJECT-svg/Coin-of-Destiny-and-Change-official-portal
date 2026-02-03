import sqlite3

def init_db():
    conn = sqlite3.connect('mother_tree.db')
    c = conn.cursor()
    
    # 1. USERS TABLE (Identity)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'member',
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 2. WALLETS TABLE (Money)
    c.execute('''CREATE TABLE IF NOT EXISTS wallets (
        user_id INTEGER PRIMARY KEY,
        codac_balance REAL DEFAULT 0.0,
        usdt_balance REAL DEFAULT 0.0,
        locked_balance REAL DEFAULT 0.0,
        points INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    # 3. MERCHANT TABLE (Business)
    c.execute('''CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        business_name TEXT,
        business_type TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Database Tables Verified: Users, Wallets, Merchants.")

if __name__ == '__main__':
    init_db()
