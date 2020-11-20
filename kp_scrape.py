import requests
import bs4
import pandas as pd
from datetime import date
import os

page = requests.get('https://kenpom.com/')
soup = bs4.BeautifulSoup(page.content, 'html.parser')
tables = soup.find('table', id='ratings-table')
rows = tables.find_all('tr', class_=lambda x: x != 'thead1' and x != 'thead2')
header = tables.find('tr', class_= 'thead2')
columns = []
for th in header.find_all('th'):
    columns.append(th.text)

l = []
for tr in rows:
    td = tr.find_all('td', class_ = lambda x: x != 'td-right')
    row = [tr.text for tr in td]
    l.append(row)
kp_data = pd.DataFrame(l, columns=columns)
kp_data.columns = ['Rk', 'Team', 'Conf', 'W-L', 'AdjEM', 'AdjO', 'AdjD', 'AdjT', 'Luck', 'OppAdjEM', 'OppO', 'OppD', 'NcOppAdjEM']
kp_data['AdjEM'] = kp_data['AdjEM'].str.replace('+', '')
kp_data['Luck'] = kp_data['Luck'].str.replace('+', '')
kp_data['OppAdjEM'] = kp_data['OppAdjEM'].str.replace('+', '')
kp_data['NcOppAdjEM'] = kp_data['NcOppAdjEM'].str.replace('+', '')

num_cols = [column for column in kp_data.columns if column not in ['Team', 'Conf', 'W-L']]
kp_data[num_cols] = kp_data[num_cols].apply(pd.to_numeric, errors='coerce', axis=1)
today = date.today()
kp_data['Date'] = today.strftime('%m/%d/%y')

kp_data.to_csv(r'/home/KenPomGraphs/mysite/historical_data/' + today.strftime('%m_%d_%y') + '.csv')

if os.path.exists('/home/KenPomGraphs/mysite/static_data/current_data.csv'):
  os.remove('/home/KenPomGraphs/mysite/static_data/current_data.csv')
else:
  pass

kp_data.to_csv(r'/home/KenPomGraphs/mysite/static_data/current_data.csv')
