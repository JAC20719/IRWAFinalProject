# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:27 2022

@author: jcane
"""

import argparse
from datetime import date
import re
import time
from tkinter import W
from numpy.linalg import norm

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
import db_operations
from matplotlib import pyplot


class EOSClassifier:
    def train(self, trainX, trainY):
        # In this part of the code, we're loading a Scikit-Learn model.
        # We're using a DecisionTreeClassifier... it's simple and lets you
        # focus on building good features.
        # Don't start experimenting with other models until you are confident
        # you have reached the scoring upper bound.
        self.clf =  RandomForestClassifier() #MLPClassifier() #DecisionTreeClassifier()  # TODO: experiment with different models
        X = [self.extract_features(x) for x in trainX]
        print(len(X), len(X[0]))
        print(len(trainY), len(trainY[0]))
        self.clf.fit(X, trainY)
        # get importance
        importance = self.clf.feature_importances_
        # summarize feature importance
        for i,v in enumerate(importance):
        	print('Feature: %0d, Score: %.5f' % (i,v))
        # plot feature importance
        pyplot.bar([x for x in range(len(importance))], importance)
        pyplot.show()
    
    def is_valid_float(self, element: str) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
    
    def extract_features(self, array):
        #Return the list of features from the parsed data
 
        features = []
        season = array[2]
        #season = season + "-" + str(int(season[2:]) + 1)
        game_id = array[0]
        # print(game_id)
        home_team = array[5]
        away_team = array[6]
        game_date = array[1]        
        #print(game_id, game_date, home_team, away_team)
        
        home_team_id = teams.find_team_by_abbreviation(home_team)["id"]
        away_team_id = teams.find_team_by_abbreviation(away_team)["id"]

        home_game_ids = db_operations.get_prior_ids(game_date, home_team_id, season)
        #print("home_ids: ", home_game_ids)
        away_game_ids = db_operations.get_prior_ids(game_date, away_team_id, season)
        
        #Append game id to ids if first game
        if(len(home_game_ids)) == 0:
            home_game_ids.append(game_id)
        if(len(away_game_ids)) == 0:
            away_game_ids.append(game_id)
        
        home_team_stats = []
        count = 0
        for stats in db_operations.get_team_stats(home_team_id, home_game_ids):
            count += 1
            for s in stats:
                if s != None:
                    home_team_stats.append(float(f'{s:.3f}'))
                else:
                    home_team_stats.append(0)
        
        away_team_stats = []
        for stats in db_operations.get_team_stats(away_team_id, away_game_ids):
            for s in stats:
                if s != None:
                    away_team_stats.append(float(f'{s:.3f}'))
                else:
                    away_team_stats.append(0)
        features = []
        features.append(home_team_stats[0])
        features.append(away_team_stats[0])
        '''
        features = home_team_stats
        for f in away_team_stats:
            features.append(f)
        '''
        DOHome = (.4*home_team_stats[3])-(.25*home_team_stats[16])+(.2*home_team_stats[10])+(.15*home_team_stats[9])
        DOAway = (.4*away_team_stats[3])-(.25*away_team_stats[16])+(.2*away_team_stats[10])+(.15*away_team_stats[9])

        
        features.append(DOHome)
        features.append(DOAway)
        
        
        
        home_players_stats = db_operations.get_player_stats(home_team_id, season[1:])[4:]
        away_players_stats = db_operations.get_player_stats(away_team_id, season[1:])[4:]
        
        
        c3 = cluster(home_players_stats)
        c4 = cluster(away_players_stats)
        
        similarity= cosine_sim(c3, c4)
        features.append(similarity)
        
        # home/away feature (0.56)
        '''
        if home_team == array[3]:
            features.append(1.0)
            features.append(0.0)
        if away_team == array[3]:
            features.append(0.0)
            features.append(1.0)
        '''
        
        #print(features)
        # print("Features: ", features)
        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)

#Clustering     

def cluster(vectors):
    cluster = []
    if len(vectors) >= 1:
        for v in vectors[0]:
            if v != None:
                cluster.append(float(v))
            else:
                cluster.append(0)
        if len(vectors) >= 2:
            for v in vectors[1:]:
                for i in range(0,len(v)):
                    if v[i] != None:
                        cluster[i] += float(v[i])
                
    cluster = [c / len(vectors) for c in cluster]
    return cluster

# Vector Similarity

def dictdot(x, y):
    '''
    Computes the dot product of vectors x and y, represented as sparse dictionaries.
    '''
    return sum(x[i] * y[i] for i in range(0,len(x)))


def cosine_sim(x, y):
    '''
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    '''
    num = dictdot(x, y)
    if num == 0:
        return 0
    return num / (norm(x) * norm(y))

def dice_sim(x, y):
    num = dictdot(x, y)
    if num == 0:
        return 0
    # TODO: implement
    return (2 * num) / (sum(x) + sum(y))


def jaccard_sim(x, y):
    num = dictdot(x, y)
    if num == 0:
        return 0
    x_sum = sum(x)
    y_sum = sum(y)
    if x_sum + y_sum - num == 0:
        return 0
    return num / (x_sum + y_sum - num)  # TODO: implement


def overlap_sim(x, y):
    num = dictdot(x, y)
    if num == 0:
        return 0
    # TODO: implement
    return num / min(sum(x), sum(y))


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
    parser.add_argument('--errors')
    
    #Arguments required for betting function
    #parser.add_argument('--home', required=True)
    #parser.add_argument('--away', required=True)
    #parser.add_argument('--season', required=True)
    return parser.parse_args()

def convert_date(date): 
    n = date.split("-")
    d = n[1] + "/" + n[2] + "/" + n[0]
    return d

def create_query_vec( season, home_team, away_team):
    game_info = db_operations.get_gameID(season, home_team, away_team)
    game_id = game_info[0][1]
    game_date = game_info[0][0]
    team_abr = game_info[0][2]
    vec = [game_id, game_date, season, team_abr, "", home_team, away_team]
    return [vec]

def main():
    '''----------------------TRAIN ALGORITHM-------------------------'''
    args = parseargs()
    trainX, trainY = load_data(args.train)
    testX, testY = load_data(args.test)
    
    classifier = EOSClassifier()
    classifier.train(trainX, trainY)
    outputs = classifier.classify(testX)
    
    if args.output is not None:
        with open(args.output, 'w') as fout:
            for output in outputs:
                print(output, file=fout)  
     
    if args.errors is not None:
        with open(args.errors, 'w') as fout:
            for y, h, x in zip(testY, outputs, testX):
                if y != h:
                    print(y, h, x, sep='\t', file=fout)
    
    evaluate(outputs, testY)
    '''--------------------------------------------------------------'''
    
    
    
    '''----------PREDICT OUTCOME OF USER INPUTTED MATCHUP------------'''
    #Get general info from arguments
    '''
    stop = "No"
    while(stop != "Yes"):
        
        home_team = input("Enter home team: ")
        away_team = input("Enter away team: ")
        season = input("Enter season: ")
        season = "2" + season[0:4]
        
        all_teams = teams.get_teams()
        #all_players = players.get_players()
        team_abrvs = [t["abbreviation"] for t in all_teams]
        
        if home_team not in team_abrvs:
            print("Incorrect home team abbreviation")
        if away_team not in team_abrvs:
            print("Incorrect away team abbreviation")
        if re.search('[0-9]{4}-[0-9]{2}',season) == None or len(season) > 7:
            print("Incorrect formatting of season!")
    
        query_vec = create_query_vec(season, home_team, away_team)
        if (None in query_vec[0]):
            print("Woops, try again!")
        else:
            out = classifier.classify(query_vec)
            print("prediction: ", out)
        
        stop = input("Quit? (Yes/No): ")
    '''
    '''---------------------------------------------------------------'''
    
   
    
    
    
    
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
    
    
    
    #atl_id = all_teams[0]["id"]
    #cel_id = all_teams[1]["id"]
    
    
    

if __name__ == "__main__":
    main()