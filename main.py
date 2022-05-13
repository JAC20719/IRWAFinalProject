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
    def train(self, trainX, trainY, dic):
        # In this part of the code, we're loading a Scikit-Learn model.
        # We're using a DecisionTreeClassifier... it's simple and lets you
        # focus on building good features.
        # Don't start experimenting with other models until you are confident
        # you have reached the scoring upper bound.
        self.clf = RandomForestClassifier() #DecisionTreeClassifier() #MLPClassifier()       # TODO: experiment with different models
        X = [self.extract_features(x,dic) for x in trainX]
        self.clf.fit(X, trainY)
    
    def is_valid_float(self, element: str) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
        
    def extract_features(self, array, dic):
        #Return the list of features from the parsed data
        #season index 3
        #game index 2
        #home_team index 
        #away_team index
        
        features = []
        season = array[1][1:]
        #season = season + "-" + str(int(season[2:]) + 1)
        game_id = array[0]
        home_team = array[4]
        away_team = array[5]
        
        #print(home_team)
        #print(away_team)
        
        home_team_id = teams.find_team_by_abbreviation(home_team)["id"]
        away_team_id = teams.find_team_by_abbreviation(away_team)["id"]
        
        hgids = [i for i in dic[home_team]]
        agids = [i for i in dic[away_team]]
    
        time.sleep(1)
        home_team_stats = cumestatsteam.CumeStatsTeam(home_team_id, hgids).total_team_stats.get_data_frame()
        time.sleep(1)
        away_team_stats = cumestatsteam.CumeStatsTeam(away_team_id, agids).total_team_stats.get_data_frame()
                
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
        dic = {}
        for line in fin:
            arr = line.strip().split()
            
            if arr[6] not in dic.keys():
                dic[arr[6]] = [arr[2]]
            else:
                dic[arr[6]].append(arr[2])
            if arr[7] not in dic.keys():
                dic[arr[7]] = [arr[2]]
            else:
                dic[arr[7]] = [arr[2]]
                
            X.append(arr[2:])
            y.append(arr[1])
        return X, y, dic


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

def game_predict(year,home_team,away_team,game_id,dic):
    
    '''
    for g in home_game_ids:
        if g < game_id:
             updated_hgids.append(g)
        
    
    for g in away_game_ids:
        if g < game_id:
            updated_agids.append(g)
    '''

def main():
    args = parseargs()
    trainX, trainY, dic = load_data(args.train)
    testX, testY, dic = load_data(args.test)
    
    #Get general info from arguments
    current_year = "2022"
    home_team = args.home
    away_team = args.away
    season = args.season

    classifier = EOSClassifier()
    classifier.train(trainX, trainY,dic)
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