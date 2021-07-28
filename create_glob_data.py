import pandas as pd
import os


path = '/home/KenPomGraphs/mysite/historical_data/'
all_files = os.listdir(path)
li = []
for filename in all_files:
    df = pd.read_csv('/home/KenPomGraphs/mysite/historical_data/'+filename, index_col=0, header=0)
    li.append(df)
glob_data = pd.concat(li, axis=0, ignore_index=True)

glob_data.set_index(['Team', 'Date'], inplace=True)
glob_data.sort_index(inplace=True)
glob_data.sort_values(by=['Rk', 'Date'], inplace=True)
glob_data.rename(columns={'School': 'Team', 'Tm.': 'Points For', 'Opp.': 'Points Against', 'W.1': 'Conf Wins', 'L.1': 'Conf Losses', 'W.2': 'Home Wins', 'L.2': 'Home Losses', 'W.3': 'Away Wins', 'L.3': 'Away Losses', 'MP': 'Minutes Played'}, inplace=True)

glob_data.to_csv('/home/KenPomGraphs/mysite/static_data/glob_data.csv')