import sqlite3

def initialize_db():
    conn = sqlite3.connect('joinmessage.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS join_messages (
        server_id INTEGER PRIMARY KEY,
        message TEXT,
        enabled BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()