import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
print("Database created and Successfully Connected to SQLite")

def get_team_stats(team_id, game_ids):
    t = tuple(game_ids)
    query = 'SELECT avg(CAST(PTS as INTEGER)) FROM gamelogs WHERE TEAM_ID = ? AND GAME_ID in {}'.format(t)
    c.execute(query, (team_id,)) 
    #:)

def main():
    get_team_stats("1610612741", ["0021500927","000000000"])
    print(c.fetchall())


if __name__ == "__main__":
    main()
