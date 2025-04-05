import pandas as pd

def get_unique_players( ):
    file = pd.read_csv("data/player_logged_in.csv") 
    return file['pid'].nunique()


def get_daily_active_users():
    file = pd.read_csv("data/player_logged_in.csv")
    file['Time'] =  pd.to_datetime(file['Time']) # make surr in time format
    file['Date'] =  file['Time'].dt.date # get date
    daily_players = file.groupby('Date')['pid'].nunique().reset_index()
    daily_players.columns = ['Date', 'UniqueActivePlayers']

    return daily_players

def get_monthly_active_users():
    file = pd.read_csv("data/player_logged_in.csv")
    file['Time'] = pd.to_datetime(file['Time'])
    file['YearMonth'] = file['Time'].dt.to_period('M').astype(str) # moth column
    monthly_active_players = file.groupby('YearMonth')['pid'].nunique().reset_index()
    monthly_active_players.columns = ['Month', 'UniqueActivePlayers']

    return monthly_active_players

def get_stickyness():
    daly_active = get_daily_active_users()
    monthly_active = get_monthly_active_users()

    daly_active['YearMonth'] = pd.to_datetime(daly_active['Date']).dt.to_period('M').astype(str)

    avg_daly_active = daly_active.groupby('YearMonth')['UniqueActivePlayers'].mean().reset_index()
    avg_daly_active.columns = ['Month', 'AvgDAU']

    monthly_active.columns = ['Month', 'MAU']

    stickiness = pd.merge(avg_daly_active, monthly_active, on='Month')
    stickiness['Stickiness'] = stickiness['AvgDAU'] / stickiness['MAU']

    return stickiness


def get_totol_session_times():
    file = pd.read_csv("data/player_logged_in.csv")
    return len(file)

def get_session_times():
    file = pd.read_csv("data/player_logged_in.csv")
    file['Time'] = pd.to_datetime(file(file['Time']))

    # sort player and time
    file = file.sort_values(['pid', 'Time'])

    file['NextTime'] = file.groupby('pid')['Time'].shift(-1) # time diference between session and player
    file['SessionLength'] = (file['NextTime'] - file['Time']).dt.total_seconds() / 60  # minutes

    file = file[file['SessionLength'] > 0]

    return file


def get_median_session_times():
    session_times = get_totol_session_times()
    return session_times['SessionLength'].median()

def get_avg_sessions_per_month():
    
    file= pd.read_csv("data/player_logged_in.csv")
    file['Time'] = pd.to_datetime(file['Time'])
    file['YearMonth'] = file['Time'].dt.to_period('M').astype(str)

    
    session_count = file.groupby('YearMonth').size().reset_index(name='TotalSessions')
    unique_users = file.groupby('YearMonth')['pid'].nunique().reset_index(name='UniqueUsers')

    median_session_times = pd.merge(session_count, unique_users, on='YearMonth')
    median_session_times['AvgSessionsPerUser'] =median_session_times['TotalSessions'] / median_session_times['UniqueUsers']

    return median_session_times

def get_progress_speed():
    file = pd.read_csv("data/study_prompt_answered.csv")
    file["Time_utc"] = pd.to_datetime(file["Time_utc"])
    file = file.sort_values(by=["pid", "Time_utc"])
    file["LevelProgressionAmount"] = pd.to_numeric(file["LevelProgressionAmount"], errors='coerce')

    # Debug: Check if column exists before calculating diff
    if "LevelProgressionAmount" not in file.columns:
        raise KeyError("Column 'LevelProgressionAmount' is missing!")

    # Calculate diff
    file["LevelProgressionAmount_diff"] = file.groupby("pid")["LevelProgressionAmount"].diff()

    # Debug: Confirm it exists
    if "LevelProgressionAmount_diff" not in file.columns:
        raise KeyError("Failed to create 'LevelProgressionAmount_diff'!")

    # Filter out NaNs and negative/zero progression
    progress_diffs = file.dropna(subset=["LevelProgressionAmount_diff"])
    progress_diffs = progress_diffs[progress_diffs["LevelProgressionAmount_diff"] > 0]

    return progress_diffs