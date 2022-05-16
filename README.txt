    Welcome to our final project, your interactive Bestfriend Betting Bot! Here
to help you hedge your bets and fuel your gambling addiction! The aim of our 
project was to train a bot that could predict the output of a given game given the
home and away teams and use bets from different betting sites to assess the risk vs
reward of placing a bet. 
    
    Information on how to run the program can be found at the bottom:
    
Successes:
    66% accuracy on classification of game's hard to predict outcome
    Implementation of centroid calculation and similarity functions resulting in 
        one of most high performing features.
    Scraping a web doc for betting information
    Standing up a local db to run operations and preprocess information
    Use API to abstract much of the data collection from nba.com
    Out perform home team win% of ~56%

Findings:
    Smaller range of data splits overtrained and yielded lower accuracy
    More features with less weights were better than fewer features with more weight

Hardships:

    1. Features:
    One of our greatest hardships was deciding on which features to include in the
    features list. A brain dead solution is having two binary features depicting 
    if it was the home or away team that won which achieved 56%, since the average 
    win% of the home team in the nba is ~56%. Thus we sought to see how much we 
    could increase this base accuracy. During this project we really felt the weight of 
    how expensive and time consuming creating features could be, especially when 
    they ended up not yielding good results. Creating each feature consumed a 
    substantial amount of time since we first had to obtain, parse, store, and 
    extract the data we believed would be necessary. Initially, we tried making api
    calls to nba.com during runtime but quickly had to scrap that due to timeouts and
    long runtimes. Instead, we created a local database where we could preprocess and
    store a majority of the information we needed and minimize the number of api calls
    we had to perform during runtime. Consquently, it became easier for us to retrieve
    the info we needed during runtime and allowed us to introduce more data and features
    into our classification. After addressing that issue we then had to tackle the
    creation and testing of features. (This was surprisingly far more difficult than
    the text and EOS classifications we did earlier in the course since we could not
    find any features that were largely indicative of a tea winning.) Even so, we
    were able to achieve a 66% accuracy with a 90:10 split.

    2. Getting Labeled Data
    While nba.com has an impressive amount of data, creating quality labeled data from 
    the overwhelming reserves of data remained a challenge. (still far better than
    hand labeling data) We first had to decide on the dataset in which we could extract
    labels and outcomes of games and even once we decided this, the data still had
    to be greatly refined in order to use it. We had to strip information that was
    unnecessary, programatically label each row depending on the matchup, (they
    had their matchup in two formats of 'away @ home' and home vs away) and then
    append necessary information to each row.

Future:
    Factor in web scraping of news articles about two teams as a doc vector and 
        factor in to decision process (i.e. is the new favorable for particular 
        team?)

How to Run:
    Arguments:
        --train logs-train.txt
        --test logs-dev.txt
        --output output.txt
        --errors errors.txt
        
    Once training completes, you will be prompted to enter 3 pieces of info, the
    home team, away team, and season.
        Home and Away team are the teams 3-Letter abbreviation, for example. CLE
        Season is the year the season began, for example the 2015-16 season would
            be entered as 2015.
            Disclaimer: acceptable dates only from 2010 to 2020