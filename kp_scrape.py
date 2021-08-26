import requests
import bs4
import pandas as pd
from datetime import date
import os

team_names = {'Alabama Birmingham': 'UAB',
             'Albany (NY)': 'Albany',
             'Boston': 'Boston University',
             'Bowling Green St.': 'Bowling Green',
             'Brigham Young': 'BYU',
             'California Baptist': 'Cal Baptist',
             'Central Connecticut St.': 'Central Connecticut',
             'Central Florida': 'UCF',
             'Citadel': 'The Citadel',
             'College of Charleston': 'Charleston',
             'Detroit Mercy': 'Detroit',
             'Florida International': 'FIU',
             'Grambling': 'Grambling St.',
             'Cal St. Long Beach': 'Long Beach St.',
             'Long Island': 'LIU',
             'Louisiana St.': 'LSU',
             'Loyola (IL)': 'Loyola Chicago',
             'Loyola (MD)': 'Loyola MD',
             'Maryland Baltimore County': 'UMBC',
             'Massachusetts Lowell': 'UMass Lowell',
             'Miami (FL)': 'Miami FL',
             'Miami (OH)': 'Miami OH',
             'Missouri Kansas City': 'UMKC',
             'Omaha': 'Nebraska Omaha',
             'Nevada Las Vegas': 'UNLV',
             'North Carolina Asheville': 'UNC Asheville',
             'North Carolina Greensboro': 'UNC Greensboro',
             'North Carolina St.': 'N.C. State',
             'North Carolina Wilmington': 'UNC Wilmington',
             'Pennsylvania': 'Penn',
             'Prairie View': 'Prairie View A&M',
             'Saint Francis (PA)': 'St. Francis PA',
             "Saint Mary's (CA)": "Saint Mary's",
             'South Carolina Upstate': 'USC Upstate',
             'Southern California': 'USC',
             'Southern Methodist': 'SMU',
             'Southern Mississippi': 'Southern Miss',
             'St. Francis (NY)': 'St. Francis NY',
             "St. John's (NY)": "St. John's",
             'Texas A&M Corpus Christi': 'Texas A&M Corpus Chris',
             'Texas Arlington': 'UT Arlington',
             'Texas Christian': 'TCU',
             'Texas El Paso': 'UTEP',
             'Texas Rio Grande Valley': 'UT Rio Grande Valley',
             'Texas San Antonio': 'UTSA',
             'Virginia Commonwealth': 'VCU'}

def clean_name(txt):
    txt = txt.replace('University of', '')
    txt = txt.replace('University At', '')
    txt = txt.replace('University', '')
    txt = txt.replace('State', 'St.')
    txt = txt.replace('-', ' ')
    txt = txt.strip()
    return txt

### KenPom Scraping ###
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

### Sports Reference Scraping ###
page = requests.get('https://www.sports-reference.com/cbb/seasons/2021-school-stats.html')
soup = bs4.BeautifulSoup(page.content)
table = soup.find('table')
body = soup.find('tbody')
rows = body.find_all('tr', attrs={'class': None})
header = table.find_all('tr')[1]
columns = [c.text for c in header.select('th') if c['data-stat'] not in ['ranker', 'DUMMY']]

l = []
for tr in rows:
    row = [td.text for td in tr.select('td[data-stat!=DUMMY]')]
    l.append(row)
print(len(l))
sr_data = pd.DataFrame(l, columns=columns)

sr_data['School'] = sr_data['School'].apply(clean_name)
sr_data.replace({'School': team_names}, inplace = True)
sr_data.rename(columns={'School': 'Team',
                        'Tm.': 'Points For',
                        'Opp.': 'Points Against',
                        'W.1': 'Conf Wins',
                        'L.1': 'Conf Losses',
                        'W.2': 'Home Wins',
                        'L.2': 'Home Losses',
                        'W.3': 'Away Wins',
                        'L.3': 'Away Losses',
                        'MP': 'Minutes Played'}, inplace=True)


sr_data.sort_values(by='Team', inplace=True)
kp_data.sort_values(by='Team', inplace=True)

combined = pd.merge(left=kp_data, right=sr_data, how='inner', on='Team')
combined.iloc[:,14:] = combined.iloc[:,14:].apply(pd.to_numeric, errors='coerce', axis=1)
combined[['Points For', 'Points Against', 'Minutes Played', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']] = combined[['Points For', 'Points Against', 'Minutes Played', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].div(combined.G, axis=0)

print(combined.info())


if os.path.exists(r'/home/KenPomGraphs/mysite/historical_data/' + today.strftime('%m_%d_%y') + '.csv'):
  os.remove(r'/home/KenPomGraphs/mysite/historical_data/' + today.strftime('%m_%d_%y') + '.csv')
else:
  pass

combined.to_csv(r'/home/KenPomGraphs/mysite/historical_data/' + today.strftime('%m_%d_%y') + '.csv')

if os.path.exists('/home/KenPomGraphs/mysite/static_data/current_data.csv'):
  os.remove('/home/KenPomGraphs/mysite/static_data/current_data.csv')
else:
  pass

combined.to_csv(r'/home/KenPomGraphs/mysite/static_data/current_data.csv')




username = "[insert username]"
api_token = "[insert API token]"
domain_name = "www.kpgraphs.com"

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username=username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=api_token)}
)
if response.status_code == 200:
    print('reloaded OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
