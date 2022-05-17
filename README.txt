





Isaac Frumkin & Justin Canedy
601.466
ifrumki1@jhu.edu, jcanedy1@jhu.edu

The aim of our project was to train a model that could predict the outcome of an NBA game and use bets from different betting sites to assess the risk of placing a bet given the prediction from our model.




























2) How to Run:

Run main.py
    Arguments:
        --train logs-train.txt
        --test logs-dev.txt
        --output output.txt
        --errors errors.txt
      
When you run main.py, the model will begin training. Once training completes, you will be prompted to enter 3 pieces of info, the home team, away team, and season.
Home and Away team are the teams’ 3-letter abbreviation (i.e. CLE)
Season is the year the season began, for example the 2015-16 season would be entered as 2015 (Disclaimer: acceptable dates only from 2010 to 2020)

3) Successes

Our model’s classification performed with a 66% accuracy in predicting the winner of NBA games. We viewed this as a success in light of the baseline we were comparing our model to. Simply predicting that the home team would win for every game had a 56% accuracy, so we achieved a ~10 percentage point improvement over our baseline.
Another success was our implementation of centroid calculation and similarity functions. We used these to compare different combinations of individual metrics. Compared to our use of individual metrics as features, the features we got from the similarity functions were generally higher performing (as evidenced by those features getting a higher weighting from the classifier).
We are also proud of standing up a database for our project. During this project we really felt the weight of how expensive and time consuming creating features could be, especially when they ended up not yielding good results. Creating each feature consumed a substantial amount of time since we first had to obtain, parse, store, and extract the data we believed would be necessary. Initially, we tried making API calls to nba.com during runtime but quickly had to scrap that due to timeouts and long runtimes. In order to comply with web crawling politeness, we pivoted to create a local database where we could preprocess and store a majority of the information we needed and minimize the number of API calls (hits to nba.com) that we had to perform during runtime. Consequently, it became easier for us to retrieve the info we needed during runtime and allowed us to introduce more data and features into our classification. 
Given the time it took for us to label and process the data that we trained on, we would also like to highlight that aspect of our project. While nba.com has an impressive amount of data, creating quality labeled data from the overwhelming reserve of data remained a challenge. We first had to decide on the datasets in which we could extract outcomes of games and even once we decided this, the data still had to be greatly refined in order to use it. For one, we had to write a script to label the data as to whether the home or away team one because the datasets we ingested did not format their data in this way. For example, nba.com listed matchups in two different formats ('away @ home' and home vs away) which added some complexity to processing the data. Also, we had to strip information that was unnecessary and then append necessary information to each row.


4) Limitations, Possibilities for Improvement, Potential Extensions

Limitations and possibilities for improvement:
	We could make our model more comprehensive if we trained on data from every NBA season, whereas currently we only use data from 2010 to the present. Another way we could improve our model is if we improved our features that related to individual player stats by weighting the stats for a given player differently depending on whether they were a starter or a bench player.

Potential extensions:
One possible extension could be to factor in web scraping of news articles into our features. We could scrape the news to determine what insiders/journalists/fans have to say about the game in question, and use these to create document vectors that could factor into the decision process.
Another possible extension would be to add a playoff-specific model. It would be interesting to see whether our existing features work better or worse in playoff games or regular season games.

5) 

7) 

We used an API for most of our data collection from nba.com. The repository for this API can be found here: https://github.com/swar/nba_api

























