import sqlite3

# connects to the database file "level.db"
connection = sqlite3.connect("level.db")

# cursor for executing the sql commands
cursor = connection.cursor


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        UserId  TEXT PRIMARY KEY,
        Xp INT DEFAULT 0,
        Level INT DEFAULT 1
    )
""")

# save the changes
connection.commit()