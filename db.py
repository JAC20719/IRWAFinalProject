# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:39:30 2022

@author: jcane
"""

import sqlite3
from nba_api.stats.endpoints import leaguegamelog

def create_gamelogs(conn, cur):
    seasons = ["2015-16", "2016-17"]
    
    #Drop Game Logs Table
    cur.execute('''DROP TABLE IF EXISTS gamelogs''')
    
    #Create Game Logs Table
    cur.execute('''CREATE TABLE gamelogs
                    (SEASON_ID text, 
                     TEAM_ID text, 
                     TEAM_ABBREVIATION text,
                     TEAM_NAME text,
                     GAME_ID text,
                     GAME_DATE text,
                     MATCHUP text,
                     WL text,
                     MIN text,
                     FGM text,
                     FGA text,
                     FG_PCT text,
                     FG3M text,
                     FG3A text,
                     FG3_PCT text,
                     FTM text,
                     FTA text,
                     FT_PCT text,
                     OREB text,
                     DREB text,
                     REB text,
                     AST text,
                     STL text,
                     BLK text,
                     TOV text,
                     PF text,
                     PTS text,
                     PLUS_MINUS text,
                     VIDEO_AVAILABLE text)''')
                    
    #Insert a row of data
    for s in seasons:
        logs = leaguegamelog.LeagueGameLog(season=s).get_data_frames()[0]
        logs.to_sql(name='gamelogs', con=conn, if_exists='append', index=False)

def main():
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    
    create_gamelogs(conn,cur)
    
    cur.execute("SELECT * FROM gamelogs;")
    print(len(cur.fetchall()))
    
    
if __name__ == "__main__":
    main()