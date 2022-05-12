# data.py
import pandas as pd

from nba_api.stats.endpoints import leaguegamelog

def label(row):
    result = row.get("WL")
    # print(result)
    matchup = row.get("MATCHUP").split()
    mid = matchup[1]
    first = matchup[0]
    second = matchup[2]
    abr = row.get("TEAM_ABBREVIATION")
    # print(matchup)
    # print(abr)
    status = ""
    home = ""
    away = ""
    if mid == "@":
        home = second
        away = first
        if abr == matchup[0]:
            status = "AWAY"
        else:
            status = "HOME"
    if mid == "vs.":
        home = first
        away = second
        if abr == matchup[2]:
            status = "AWAY"
        else:
            status = "HOME"
    # print(status)
    label = ""
    if result == "W":
        label = status
    else:
        if status == "AWAY":
            # print("AAAAAA")
            label = "HOME"
        if status == "HOME":
            label = "AWAY"
    # print("LABEL: ", label)
    return label, home, away

def main():

    seasons = ["2016-17", "2017-18", "2018-19"]
    s1=pd.DataFrame(leaguegamelog.LeagueGameLog(season="2015-16").get_data_frames()[0])
    s2=pd.DataFrame(leaguegamelog.LeagueGameLog(season="2016-17").get_data_frames()[0])
    s3=pd.DataFrame(leaguegamelog.LeagueGameLog(season="2017-18").get_data_frames()[0])
    # s3.insert(1, "LABEL", "HOME")

    all_games = pd.concat([s1, s2, s3], ignore_index=True)
    all_games.insert(0, "LABEL", "HOME")

    for i, row in all_games.iterrows():
        # if i == 1:
            # print(row.get("SEASON_ID"))
            l, home, away = label(row)
            # print(l)
            all_games.at[i, "LABEL"] = l
            all_games.at[i, "HOME"] = home
            all_games.at[i, "AWAY"] = away
        

    all_games = all_games[["LABEL", "GAME_ID", "SEASON_ID", "TEAM_ABBREVIATION", "WL", "HOME", "AWAY" ]]
    # for i in range(len(all_games)) :
    #     print(all_games.loc(i))
    # print(all_games)
    

    
    # all_games.insert(5, "HOME", "HOME")
    # all_games.insert(6, "AWAY", "HOME")


    all_games = all_games.drop_duplicates(subset=["GAME_ID"])

    

    f = open("logs.txt", "w")
    dfAsString = all_games.to_string()
    # l = dfAsString.splitlines()[1]
    # print(l)


    f.write(dfAsString)


if __name__ == "__main__":
    main()