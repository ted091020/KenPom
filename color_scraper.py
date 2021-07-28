import requests
import bs4
import pandas as pd 
import re

page = requests.get('https://teamcolorcodes.com/ncaa-color-codes/')
soup = bs4.BeautifulSoup(page.content, 'html.parser')

paragraphs = soup.findAll('p', class_=lambda x: x not in ['site-title', 'site-description', 'team-button'])[1:]

team_links = []
for p in paragraphs:
	for a in p.find_all('a'):
		team_links.append(a['href'])

all_data = []
iteration = 0
bad_words = ['Colors', 'Color', 'Codes']
big_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, bad_words)))

for link in team_links[:-2]:
	iteration += 1
	page = requests.get(link)
	soup = bs4.BeautifulSoup(page.content, 'html.parser')
	team_data = []
	title = soup.find('h1', class_='entry-title').text
	team_name = big_regex.sub('', title).strip()
	print(team_name)
	team_data.append(team_name)
	try:
		primary_color = soup.find('div', class_='colorblock')['style'].split(';')[0].split(':')[1].strip()
	except KeyError:
		primary_color = '#000000'
	print(primary_color)
	team_data.append(primary_color)
	all_data.append(team_data)

df = pd.DataFrame(all_data, columns=['Team', 'Color'])

df.to_csv(r'C:\Users\Evan\Desktop\KenPom_project\team_colors.csv')

