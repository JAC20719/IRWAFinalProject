# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:27 2022

@author: jcane
"""

import argparse
import re

'''Imports for sklearn'''
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

'''Imports for nba api'''
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, cumestatsteam, teamgamelog, cumestatsteamgames
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

    def extract_features(self, array):
        #Return the list of features from the parsed data
        return []

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)

def load_data(file):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split()
            X.append(arr[1:])
            y.append(arr[0])
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
    

    if args.output is not None:
        with open(args.output, 'w') as fout:
            for output in outputs:
                print(output, file=fout)
                    
    all_players = players.get_players()
    all_teams = teams.get_teams()
    
    team_abrvs = [t["abbreviation"] for t in all_teams]
    if home_team not in team_abrvs:
        print("Incorrect home team abbreviation")
    if away_team not in team_abrvs:
        print("Incorrect away team abbreviation")
    if re.search('[0-9]{4}-[0-9]{2}',season) == None or len(season) > 7:
        print("Incorrect formatting of season!")
    
    atl_id = all_teams[0]["id"]
    cel_id = all_teams[1]["id"]
    
    '''2021-22'''
    #game_predict('2021-22', atl_id, cel_id, False)
        
    

if __name__ == "__main__":
    main(sys.argv[1:])