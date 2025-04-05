import pandas as pd

def get_unique_players( ):
    file = pd.read_csv("data/player_logged_in.csv") 
    return file['pid'].nunique()


def get_monthtly_active_users():
    file = pd.read_csv("data/player_logged_in.csv")
    file['Time'] =  pd.to_datetime(file['Time']) # make surr in time format
    file['Date'] =  file['Time'].dt.date # get date
    daily_players = file.groupby('Date')['pid'].nunique().reset_index()
    daily_players.columns = ['Date', 'UniqueActivePlayers']

    return daily_players