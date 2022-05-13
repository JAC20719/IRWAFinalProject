import sqlite3
from tkinter.tix import REAL
conn = sqlite3.connect('example.db')
c = conn.cursor()
print("Database created and Successfully Connected to SQLite")

def get_team_stats(team_id, game_ids):
    t = tuple(game_ids)
    query = '''SELECT 
                avg(CAST(PTS as INTEGER)),
                avg(CAST(FGM as REAL)),
                avg(CAST(FGA as REAL)),
                avg(CAST(FG_PCT as REAL)),
                avg(CAST(FG3M as REAL)),
                avg(CAST(FG3A as REAL)),
                avg(CAST(FG3_PCT as REAL)),
                avg(CAST(FTM as REAL)),
                avg(CAST( FTA as REAL)),
                avg(CAST(FT_PCT as REAL)),
                avg(CAST(OREB as REAL)),
                avg(CAST(DREB as REAL)),
                avg(CAST(REB as REAL)),
                avg(CAST(AST as REAL)),
                avg(CAST(STL as REAL)),
                avg(CAST(BLK as REAL)),
                avg(CAST(TOV as REAL)),
                avg(CAST(PF as REAL)),
                avg(CAST(PTS as REAL))
                FROM gamelogs WHERE TEAM_ID = ? AND GAME_ID in {}'''.format(t)
    c.execute(query, (team_id,)) 

def main():
    get_team_stats("1610612741", ["0021500927","000000000"])
    print(c.fetchall())


if __name__ == "__main__":
    main()
