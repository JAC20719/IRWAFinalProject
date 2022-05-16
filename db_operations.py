import sqlite3
import requests
from tkinter.tix import REAL
from nba_api.stats.endpoints import playercareerstats


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
                    avg(CAST(PTS as REAL)) as pts
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
                    avg(CAST(PTS as INTEGER)) as pts
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

def get_gameID(season, home, away):
    #print(season,home,away)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    query = '''SELECT MAX(GAME_DATE), GAME_ID, TEAM_ABBREVIATION
                FROM gamelogs 
                WHERE SEASON_ID = ? AND (TEAM_ABBREVIATION = ? or TEAM_ABBREVIATION = ?)'''
    c.execute(query, (season, home, away, ))
    return c.fetchall()

def get_player_stats(team_id,season):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    query = 'SELECT PLAYER_ID FROM rosters WHERE TeamID = ? AND SEASON = ?'
    c.execute(query, (team_id,season))
    all_players_stats = []
    for ID in c.fetchall():
        query = 'SELECT * FROM playerstats WHERE PLAYER_ID = ?'
        c.execute(query, (ID[0], ))
        player_stats = c.fetchall()
        player_stats_vec = list(player_stats[0])
        all_players_stats.append(player_stats_vec)
    return all_players_stats
    #Add more functionality to return all the player's stats for that season and player_id

def get_standings(team_id, season_id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    query = 'SELECT * FROM standings WHERE TeamID = ? and SeasonID = ?'
    c.execute(query, (team_id, season_id))
    return c.fetchall()


def main():
    #get_prior_ids("2015-10-30","1610612741","22015")
    #print(get_team_stats("1610612741", ["0021500927"]))
    # print(c.fetchall())
    #print(get_gameID("22015", "DET", "CLE"))
    #print(get_player_stats("1610612739","2015"))
    
    '''
    source = requests.get("https://api.lineups.com/nba/fetch/lineups/gateway").json()
    print(source)
    for player in source['data'][0]['away_players']:
        print(player['name'])
    '''
    return


if __name__ == "__main__":
    main()
