import sqlite3
import os

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username FROM accounts_customuser")
        users = cursor.fetchall()
        print("Users in SQLite:")
        for u in users:
            print(f"- {u[0]}")
    except Exception as e:
        print(f"Error reading SQLite: {e}")
    finally:
        conn.close()
else:
    print("SQLite db.sqlite3 not found.")
