import pandas as pd

def get_unique_players( ):
    file = pd.read_csv("data/player_logged_in.csv") 
    return file['pid'].nunique()