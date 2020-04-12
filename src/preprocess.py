import pandas as pd
import numpy as np


def load_dataset(path: str = "data/IPL Data/matches.csv"):
    matches = pd.read_csv(path, index_col=0)
    list_of_teams = np.unique(matches[["team1", "team2"]]).tolist()
    matches_cities = pd.read_csv("data/IPL Data/matches_cities_lat_long.csv")
    return matches, list_of_teams, matches_cities


matches, list_of_teams, matches_cities = load_dataset()
