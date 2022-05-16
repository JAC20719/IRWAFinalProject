# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:39:30 2022

@author: jcane
"""

import sqlite3
from nba_api.stats.endpoints import leaguegamelog, commonteamroster, playercareerstats, leaguestandings
from nba_api.stats.static import teams
from nba_api.stats.static import players
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

def create_player_stats(conn, cur):
    #Drop Playerstats Table
    cur.execute('''DROP TABLE IF EXISTS playerstats''')
    
    #Create Playerstats Table
    cur.execute('''CREATE TABLE playerstats
                (PLAYER_ID text,
                 LEAGUE_ID text, 
                 Team_ID text,
                 PLAYER_AGE text,
                 GP text,
                 GS text, 
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
                 PTS text)''')
    
    all_players = players.get_players()
    all_player_ids = [p["id"] for p in all_players]
    
    for ID in all_player_ids:
        player_stats = playercareerstats.PlayerCareerStats(ID)
        career_stats = player_stats.career_totals_regular_season.get_data_frame()
        career_stats.to_sql(name='playerstats', con=conn, if_exists='append', index=False)


def create_standings(conn, cur):
    #Drop Standings Table
    cur.execute('''DROP TABLE IF EXISTS standings''')
    
    #Create Standings Table
    cur.execute('''CREATE TABLE standings
                (LeagueID text,
                SeasonID text,
                TeamID text,
                TeamCity text,
                TeamName text,
                Conference text,
                ConferenceRecord text,
                PlayoffRank text,
                ClinchIndicator text,
                Division text,
                DivisionRecord text,
                DivisionRank text,
                WINS text,
                LOSSES text,
                WinPCT text,
                LeagueRank text,
                Record text,
                HOME text,
                ROAD text,
                L10 text,
                Last10Home text,
                Last10Road text,
                OT text,
                ThreePTSOrLess text,
                TenPTSOrMore text,
                LongHomeStreak text,
                strLongHomeStreak text,
                LongRoadStreak text,
                strLongRoadStreak text,
                LongWinStreak text,
                LongLossStreak text,
                CurrentHomeStreak text,
                strCurrentHomeStreak text,
                CurrentRoadStreak text,
                strCurrentRoadStreak text,
                CurrentStreak text,
                strCurrentStreak text,
                ConferenceGamesBack text,
                DivisionGamesBack text,
                ClinchedConferenceTitle text,
                ClinchedDivisionTitle text,
                ClinchedPlayoffBirth text,
                EliminatedConference text,
                EliminatedDivision text,
                AheadAtHalf text,
                BehindAtHalf text,
                TiedAtHalf text,
                AheadAtThird text,
                BehindAtThird text,
                TiedAtThird text,
                Score100PTS text,
                OppScore100PTS text,
                OppOver500 text,
                LeadInFGPCT text,
                LeadInReb text,
                FewerTurnovers text,
                PointsPG text,
                OppPointsPG text,
                DiffPointsPG text,
                vsEast text,
                vsAtlantic text,
                vsCentral text,
                vsSoutheast text,
                vsWest text,
                vsNorthwest text,
                vsPacific text,
                vsSouthwest text,
                Jan text,
                Feb text,
                Mar text,
                Apr text,
                May text,
                Jun text,
                Jul text,
                Aug text,
                Sep text,
                Oct text,
                Nov text,
                Dec text,
                PreAS text,
                PostAS text)''')

    seasons = ["2015-16", "2016-17"]
    all_teams = teams.get_teams()

    for s in seasons:
        standings = leaguestandings.LeagueStandings(season=s).get_data_frames()
        for team_stand in standings:
            team_stand.to_sql(name='standings', con=conn, if_exists='append', index=False)

def main():
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    
    # create_gamelogs(conn,cur)
    #create_rosters(conn, cur)
    #create_player_stats(conn, cur) #!!!!WARNING, DO NOT RUN, OPERATION Takes 1.5hrs!!!###
    # create_standings(conn,cur)

    '''
    cur.execute('SELECT * FROM playerstats')
    print(len(cur.fetchall()))
    '''
    
    # cur.execute("SELECT * FROM gamelogs;")
    # print(len(cur.fetchall()))

    # cur.execute("SELECT * FROM rosters;")
    # print(len(cur.fetchall()))
    
    
if __name__ == "__main__":
    main()