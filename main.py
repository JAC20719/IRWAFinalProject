# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:27 2022

@author: jcane
"""

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams 

import pandas as pd 


def main():
    all_players = players.get_players()
    all_teams = teams.get_teams()
    

if __name__ == "__main__":
    main()