import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
print("Database created and Successfully Connected to SQLite")

def get_team_stats(team_id, game_ids):
    bind = ','.join(i for i in game_ids)
    print(bind)
    c.execute('SELECT * FROM gamelogs WHERE TEAM_ID = ? GAME_ID in (%s)' %(bind,),(team_id,))  

def main():
    get_team_stats("1610612741", ("0021500927",))
    print(c.fetchall())


if __name__ == "__main__":
    main()


# ("0021500927", )
#avg(CAST(PTS as INTEGER))
#,