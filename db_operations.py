import sqlite3
conn = sqlite3.connect('nba.db')
c = conn.cursor()
print("Database created and Successfully Connected to SQLite")

c.execute("""CREATE TABLE team_stats (
                team_id int,
                
    )""")

