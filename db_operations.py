import sqlite3
from tkinter.tix import REAL

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def get_team_stats(team_id, game_ids):
    conn = sqlite3.connect('example.db')
    #conn.row_factory = sqlite3.Row #Used if we want to make a dictionary
    c = conn.cursor()

    if len(game_ids) != 1:
        t = tuple(game_ids)
        #print(t)
        query = '''SELECT
                    avg(CAST(PLUS_MINUS as REAL)) as plus_minus,
                    avg(CAST(FGM as REAL)) as fgm,
                    avg(CAST(FGA as REAL)) as fga,
                    avg(CAST(FG_PCT as REAL)) as fg_pct,
                    avg(CAST(FG3M as REAL)) as fg3m,
                    avg(CAST(FG3A as REAL)) as fg3a,
                    avg(CAST(FG3_PCT as REAL)) as fg3_pct,
                    avg(CAST(FTM as REAL)) as ftm,
                    avg(CAST( FTA as REAL)) as fta,
                    avg(CAST(FT_PCT as REAL)) as ft_pct,
                    avg(CAST(OREB as REAL)) as oreb,
                    avg(CAST(DREB as REAL)) as dreb,
                    avg(CAST(REB as REAL)) as reb,
                    avg(CAST(AST as REAL)) as ast,
                    avg(CAST(STL as REAL)) as stl,
                    avg(CAST(BLK as REAL)) as blk,
                    avg(CAST(TOV as REAL)) as tov,
                    avg(CAST(PF as REAL)) as pf,
                    avg(CAST(PTS as REAL)) as pts,
                    (SELECT COUNT(WL) FROM gamelogs WHERE WL = 'w')
                    FROM gamelogs 
                    WHERE TEAM_ID = ? AND GAME_ID in {}'''.format(t)
        c.execute(query, (team_id,)) 

    else:
        query = '''SELECT
                    avg(CAST(PLUS_MINUS as REAL)) as plus_minus,
                    avg(CAST(FGM as REAL)) as fgm,
                    avg(CAST(FGA as REAL)) as fga,
                    avg(CAST(FG_PCT as REAL)) as fg_pct,
                    avg(CAST(FG3M as REAL)) as fg3m,
                    avg(CAST(FG3A as REAL)) as fg3a,
                    avg(CAST(FG3_PCT as REAL)) as fg3_pct,
                    avg(CAST(FTM as REAL)) as ftm,
                    avg(CAST( FTA as REAL)) as fta,
                    avg(CAST(FT_PCT as REAL)) as ft_pct,
                    avg(CAST(OREB as REAL)) as oreb,
                    avg(CAST(DREB as REAL)) as dreb,
                    avg(CAST(REB as REAL)) as reb,
                    avg(CAST(AST as REAL)) as ast,
                    avg(CAST(STL as REAL)) as stl,
                    avg(CAST(BLK as REAL)) as blk,
                    avg(CAST(TOV as REAL)) as tov,
                    avg(CAST(PF as REAL)) as pf,
                    avg(CAST(PTS as INTEGER)) as pts,
                    (SELECT COUNT(WL) FROM gamelogs WHERE WL = 'w')
                    FROM gamelogs 
                    WHERE TEAM_ID = ? AND GAME_ID = ?'''
        c.execute(query, (team_id,game_ids[0])) 
     
    #dict_from_row(c.fetchall()[0]) #Used if we want to make a dictionary
    return c.fetchall()

def get_prior_ids(date,team,season):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
   
    query = 'SELECT GAME_ID from gamelogs WHERE TEAM_ID = ? AND SEASON_ID = ? AND date(GAME_DATE) < date(?)'
    c.execute(query, (team,season,date, ))
    # print(c.fetchall())
    ids = []
    for row in c.fetchall():
        ids.append(row[0])
    return ids

def get_gameID(season, date, home, away):
    print(season,date,home,away)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    query = 'SELECT GAME_ID from gamelogs WHERE SEASON_ID = ? and GAME_DATE = ? and (TEAM_ABBREVIATION = ? or TEAM_ABBREVIATION = ?)'
    c.execute(query, (season, date, home, away, ))
    return c.fetchall()

def main():
    #get_prior_ids("2015-10-30","1610612741","22015")
    #print(get_team_stats("1610612741", ["0021500927"]))
    # print(c.fetchall())
    print()


if __name__ == "__main__":
    main()
