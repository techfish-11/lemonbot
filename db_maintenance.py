import sqlite3

# データベース接続
def get_lemon_db_connection():
    conn = sqlite3.connect('lemon.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初回起動時にテーブルが存在しない場合、作成する
def create_lemon_table():
    conn = get_lemon_db_connection()
    cursor = conn.cursor()
    
    # テーブル作成クエリ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lemons (
            user_id INTEGER PRIMARY KEY,
            lemon_name TEXT,
            health INTEGER,
            happiness INTEGER,
            level INTEGER,
            growth_time INTEGER,
            last_care TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# この関数をBot起動時に一度だけ呼び出す
create_lemon_table()
