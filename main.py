# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:27 2022

@author: jcane
"""

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, cumestatsteam, teamgamelog, cumestatsteamgames
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams 

import pandas as pd 

import sys

def game_predict(year,home_team,away_team,playoff):
    winning_team = home_team
    win_margin = 0
    
    home_game_ids = cumestatsteamgames.CumeStatsTeamGames(team_id=home_team,season=year).get_data_frames()[0].get("GAME_ID").tolist()
    away_game_ids = cumestatsteamgames.CumeStatsTeamGames(team_id=home_team,season=year).get_data_frames()[0].get("GAME_ID").tolist()

    home_team_stats = cumestatsteam.CumeStatsTeam(home_team, home_game_ids).get_data_frames()
    away_team_stats = cumestatsteam.CumeStatsTeam(away_team, away_game_ids).get_data_frames()
    # print(home_team_stats[0].get("FG_PCT"))
    
    return winning_team, win_margin

def main(argv):
    all_players = players.get_players()
    all_teams = teams.get_teams()
    
    atl_id = all_teams[0]["id"]
    cel_id = all_teams[1]["id"]
    
    '''2021-22'''
    
    game_predict('2021-22', atl_id, cel_id, False)
        
    

if __name__ == "__main__":
    main(sys.argv[1:])