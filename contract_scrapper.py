import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

def request_base_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    return response

def get_ulr_spotrac_player(player, team):
    domain = 'https://www.spotrac.com/mlb'
    domain_team = domain + '/' + team
    domain_team_player = domain_team + '/' + player

    return str(domain_team_player)

def create_team_dict():
    dict = {}
    #NL West
    dict['Arizona Diamondbacks'] = 'arizona-diamondbacks'
    dict['Colorado Rockies'] = 'colorado-rockies'
    dict['Los Angeles Dodgers'] = 'los-angeles-dodgers'
    dict['San Diego Padres'] = 'san-diego-padres'
    dict['San Francisco Giants'] = 'san-francisco-giants'
    #NL Central
    dict['Chicago Cubs'] = 'chicago-cubs'
    dict['Cincinnati Reds'] = 'cincinnati-reds'
    dict['Milwaukee Brewers'] = 'milwaukee-brewers'
    dict['Pittsburgh Pirates'] = 'pittsburgh-pirates'
    dict['St. Louis Cardinals'] = 'st-louis-cardinals'
    #NL East
    dict['Atlanta Braves'] = 'atlanta-braves'
    dict['Miami Marlins'] = 'miami-marlins'
    dict['New York Mets'] = 'new-york-mets'
    dict['Philadelphia Phillies'] = 'philadelphia-phillies'
    dict['Washington Nationals'] = 'washington-nationals'
    #AL West
    dict['Houston Astros'] = 'houston-astros'
    dict['Los Angeles Angels'] = 'los-angeles-angels'
    dict['Oakland Athletics'] = 'oakland-athletics'
    dict['Seattle Mariners'] = 'seattle-mariners'
    dict['Texas Rangers'] = 'texas-rangers'
    #AL Central
    dict['Chicago White Sox'] = 'chicago-white-sox'
    dict['Cleveland Indians'] = 'cleveland-indians'
    dict['Detroit Tigers'] = 'detroit-tigers'
    dict['Kansas City Royals'] = 'kansas-city-royals'
    dict['Minnesota Twins'] = 'minnesota-twins'
    #AL East
    dict['Baltimore Orioles'] = 'baltimore-orioles'
    dict['Boston Red Sox'] = 'boston-red-sox'
    dict['New York Yankees'] = 'new-york-yankees'
    dict['Tampa Bay Rays'] = 'tampa-bay-rays'
    dict['Toronto Blue Jays'] = 'toronto-blue-jays'
    return dict

def make_pretty_soup(response):
    return BeautifulSoup(response.text, 'html.parser').prettify()

def get_contract_info(player_ulr):
    response = request_base_html(player_ulr)
    soup = make_pretty_soup(response)

    player_info = {}

    for transaction in soup.find_all('div', class_='transitem'):
        year = transaction.find('span', class_='transdate').text.strip()
        year = datetime.strptime(year, '%b %d %Y').year
        info = transaction.find('span', class_='transdesc').text.strip()

        if ('$' in info) and (year not in player_info):
            player_info[year] = info

    return player_info

  

def main():
    team_dict = create_team_dict()

    player_ulr = get_ulr_spotrac_player('randy-johnson', team_dict['Arizona Diamondbacks'])

    print(player_ulr)

    response = request_base_html(player_ulr)

    print(response)

    pretty_soup = make_pretty_soup(response)

    print(get_contract_info(player_ulr))

main()
