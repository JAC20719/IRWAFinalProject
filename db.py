# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:39:30 2022

@author: jcane
"""

import sqlite3
from nba_api.stats.endpoints import leaguegamelog, commonteamroster
from nba_api.stats.static import teams
import time

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

def create_rosters(conn, cur):
    #Drop Rosters Table
    cur.execute('''DROP TABLE IF EXISTS rosters''')
    
    #Create Rosters Table
    cur.execute('''CREATE TABLE rosters
                (TeamID text,
                SEASON text,
                LeagueID text,
                PLAYER text,
                PLAYER_SLUG text,
                NUM text,
                POSITION text,
                HEIGHT text,
                WEIGHT text,
                BIRTH_DATE text,
                AGE text,
                EXP text,
                SCHOOL text,
                NICKNAME text,
                PLAYER_ID text)''')
    
    seasons = ["2015-16", "2016-17"]
    all_teams = teams.get_teams()

    for s in seasons:
        for t in all_teams:
            tid = t.get('id')
            time.sleep(1)
            rosters = commonteamroster.CommonTeamRoster(season=s, team_id=tid).get_data_frames()[0]
            time.sleep(1)
            rosters.to_sql(name='rosters', con=conn, if_exists='append', index=False)

def main():
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    
    # create_gamelogs(conn,cur)
    create_rosters(conn, cur)
    
    # cur.execute("SELECT * FROM gamelogs;")
    # print(len(cur.fetchall()))

    # cur.execute("SELECT * FROM rosters;")
    # print(len(cur.fetchall()))
    
    
if __name__ == "__main__":
    main()