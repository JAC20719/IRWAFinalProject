# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:27 2022

@author: jcane
"""

import argparse
import re
import time

'''Imports for sklearn'''
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

'''Imports for nba api'''
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, cumestatsteam, teamgamelog, cumestatsteamgames, playercareerstats
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams 

import pandas as pd 
import sys

class EOSClassifier:
    def train(self, trainX, trainY):
        # In this part of the code, we're loading a Scikit-Learn model.
        # We're using a DecisionTreeClassifier... it's simple and lets you
        # focus on building good features.
        # Don't start experimenting with other models until you are confident
        # you have reached the scoring upper bound.
        self.clf = RandomForestClassifier() #DecisionTreeClassifier() #MLPClassifier()       # TODO: experiment with different models
        X = [self.extract_features(x) for x in trainX]
        self.clf.fit(X, trainY)
    
    def is_valid_float(self, element: str) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
    
    def extract_features(self, array):
        #Return the list of features from the parsed data
        #season index 3
        #game index 2
        #home_team index 
        #away_team index

        features = []
        season = array[2][1:]
        #season = season + "-" + str(int(season[2:]) + 1)
        game_id = array[0]
        # print(game_id)
        home_team = array[5]
        away_team = array[6]
        game_date = array[1]
        print(game_date)
        
        print(home_team)
        print(away_team)
        
        home_team_id = teams.find_team_by_abbreviation(home_team)["id"]
        away_team_id = teams.find_team_by_abbreviation(away_team)["id"]
        
        print(home_team_id, away_team_id)
        home_team_stats, away_team_stats = game_predict(season, home_team_id, away_team_id, game_id, game_date)
        
        features.append(home_team_stats)
        features.append(away_team_stats)
        
        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)

def load_data(file):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split()
            X.append(arr[2:])
            y.append(arr[1])
        return X, y


def evaluate(outputs, golds):
    correct = 0
    for h, y in zip(outputs, golds):
        if h == y:
            correct += 1
    print(f'{correct} / {len(golds)}  {correct / len(golds)}')


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True)
    parser.add_argument('--test', required=True)
    parser.add_argument('--output')
    
    #Arguments required for betting function
    parser.add_argument('--home', required=True)
    parser.add_argument('--away', required=True)
    parser.add_argument('--season', required=True)
    return parser.parse_args()

def convert_date(date): 
    n = date.split("-")
    d = n[1] + "/" + n[2] + "/" + n[0]
    return d

def game_predict(year,home_team,away_team, game_id, game_date):
    time.sleep(1)
    #print(home_team)
    print(year, home_team, away_team)
    print(game_date)
    # home_game_ids = [game_id]
    home_game_ids = teamgamelog.TeamGameLog(team_id=home_team,season=year, date_to_nullable=convert_date(game_date)).get_data_frames()[0].get("Game_ID").tolist()
    print(home_game_ids)
    away_game_ids = teamgamelog.TeamGameLog(team_id=away_team,season=year, date_to_nullable=convert_date(game_date)).get_data_frames()[0].get("Game_ID").tolist()

    home_team_stats = cumestatsteam.CumeStatsTeam(home_team, home_game_ids).total_team_stats.get_data_frame()
    away_team_stats = cumestatsteam.CumeStatsTeam(away_team, away_game_ids).total_team_stats.get_data_frame()
    #print(home_team_stats)
    
    #print(home_team_stats)

    return home_team_stats, away_team_stats

def main():
    args = parseargs()
    trainX, trainY = load_data(args.train)
    testX, testY = load_data(args.test)
    
    #Get general info from arguments
    current_year = "2022"
    home_team = args.home
    away_team = args.away
    season = args.season

    classifier = EOSClassifier()
    classifier.train(trainX, trainY)
    outputs = classifier.classify(testX)
    
    '''
    if args.output is not None:
        with open(args.output, 'w') as fout:
            for output in outputs:
                print(output, file=fout)  
     '''
    
    
    all_teams = teams.get_teams()
    all_players = players.get_players()
    
    #Turn stats into a vector
    '''
    jordan_id = players.find_players_by_full_name("Michael Jordan")[0]["id"]
    jordan_stats = playercareerstats.PlayerCareerStats(jordan_id).career_totals_regular_season.get_data_frame()
    jordan_stats_vec = jordan_stats.iloc[0].to_list()
    print(jordan_stats_vec)
    '''
    
    #Retrieve all player's stats
    '''
    all_player_ids = [p["id"] for p in all_players]
    all_player_stats = playercareerstats.PlayerCareerStats(all_player_ids[300]).career_totals_regular_season.get_data_frame()
    print(all_player_stats)
    '''
    
    
    team_abrvs = [t["abbreviation"] for t in all_teams]
    
    if home_team not in team_abrvs:
        print("Incorrect home team abbreviation")
    if away_team not in team_abrvs:
        print("Incorrect away team abbreviation")
    if re.search('[0-9]{4}-[0-9]{2}',season) == None or len(season) > 7:
        print("Incorrect formatting of season!")
    
    #atl_id = all_teams[0]["id"]
    #cel_id = all_teams[1]["id"]
    
    
    evaluate(outputs, testY)
    

if __name__ == "__main__":
    main()