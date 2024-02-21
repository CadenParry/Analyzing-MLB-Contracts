import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os


def parse_player_name(player):
    player = player.replace(' ', '-')
    return player

def request_base_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    return response

def get_ulr_spotrac_player(player, teams):

    for team in teams:
        domain = 'https://www.spotrac.com/mlb'
        domain_team = domain + '/' + team
        domain_team_player = domain_team + '/' + player + '/' + 'transactions/'

        if request_base_html(domain_team_player) is not None:
            return str(domain_team_player)
        
    return None

def create_team_dict():
    dict = {}
    #NL West
    dict['AD'] = 'arizona-diamondbacks'
    dict['CR'] = 'colorado-rockies'
    dict['LAD'] = 'los-angeles-dodgers'
    dict['SD'] = 'san-diego-padres'
    dict['SF'] = 'san-francisco-giants'
    #NL Central
    dict['CHC'] = 'chicago-cubs'
    dict['CIN'] = 'cincinnati-reds'
    dict['MIL'] = 'milwaukee-brewers'
    dict['PIT'] = 'pittsburgh-pirates'
    dict['STL'] = 'st-louis-cardinals'
    #NL East
    dict['ATL'] = 'atlanta-braves'
    dict['MIA'] = 'miami-marlins'
    dict['NYM'] = 'new-york-mets'
    dict['PHI'] = 'philadelphia-phillies'
    dict['WSH'] = 'washington-nationals'
    #AL West
    dict['HOU'] = 'houston-astros'
    dict['LAA'] = 'los-angeles-angels'
    dict['OAK'] = 'oakland-athletics'
    dict['SEA'] = 'seattle-mariners'
    dict['TEX'] = 'texas-rangers'
    #AL Central
    dict['CWS'] = 'chicago-white-sox'
    dict['CLE'] = 'cleveland-indians'
    dict['DET'] = 'detroit-tigers'
    dict['KC'] = 'kansas-city-royals'
    dict['MIN'] = 'minnesota-twins'
    #AL East
    dict['BAL'] = 'baltimore-orioles'
    dict['BOS'] = 'boston-red-sox'
    dict['NYY'] = 'new-york-yankees'
    dict['TB'] = 'tampa-bay-rays'
    dict['TOR'] = 'toronto-blue-jays'
   
    return dict

def make_soup(response):
    return BeautifulSoup(response.text, 'html.parser')

def get_player_info(soup):
    player_info = {}

    for transaction in soup.find_all('div', class_='transitem'):
        year = transaction.find('span', class_='transdate').text.strip()
        year = datetime.strptime(year, '%b %d %Y').year
        info = transaction.find('span', class_='transdesc').text.strip()

        if ('$' in info):
            if year not in player_info:
                player_info[year] = [info]
            else:
                if info not in player_info[year]:
                    player_info[year].append(info)
                
    return player_info

def get_largest_contract(player_info):
    largest_contract = 0
    largest_contract_year = None
    largest_contract_duration = None
    largest_contract_team = None
    for year in player_info:
        for contract in player_info[year]:
            match = re.search(r'\$(\d+(?:\.\d+)?)( million)?', contract)
            duration_match = re.search(r'(\d+) year', contract)
            team_match = re.search(r'\((.*?)\)', contract)  # get the text within parentheses
            if match:
                value = float(match.group(1))
                if match.group(2):
                    value *= 1e6  # convert to millions if 'million' is present
                if value > largest_contract:
                    largest_contract = value
                    largest_contract_year = year
                    if duration_match:
                        largest_contract_duration = int(duration_match.group(1))
                    if team_match:
                        largest_contract_team = team_match.group(1)
    return largest_contract_year, "${:,.2f}".format(largest_contract), largest_contract_duration, largest_contract_team

def continuous_player_search():
    while True:
    
        player_name = input('Enter a player (X to exit): ')
        if player_name == 'x' or player_name == 'X':
            break

        user_chosen_player = parse_player_name(player_name)
    
        team_dict = create_team_dict()
            
        player_ulr = get_ulr_spotrac_player(str(user_chosen_player), team_dict)

        response = request_base_html(player_ulr)

        player_info = get_player_info(make_soup(response))
            
        largest_contract = get_largest_contract(player_info)

        print('player: ' + player_name)
        print('year: ' + str(largest_contract[0]))
        print('contract value: ' + str(largest_contract[1]))
        print('duration: ' + str(largest_contract[2]))
        print('team: ' + str(largest_contract[3]))
        print('\n')

        # add the results of a search to a file in the correct directory
        os.chdir('/Users/cadenparry/Analyzing-MLB-Contracts')

        with open('results-test-1.txt', 'a') as file:
            file.write('player: ' + player_name + '\n')
            file.write('year: ' + str(largest_contract[0]) + '\n')
            file.write('contract value: ' + str(largest_contract[1]) + '\n')
            file.write('duration: ' + str(largest_contract[2]) + '\n')
            file.write('team: ' + str(largest_contract[3]) + '\n')
            file.write('\n')
            file.close()
            
def main():
    # print('Welcome to the MLB contract scrapper')
    # print('Press C for continuous search of players contracts')
    # print('Press X to exit at any time')
    # choice = input('Enter your choice: ')

    # if choice == 'C' or 'c':
    #     continuous_player_search()
    # else:
    #     print('Goodbye')

   #print(os.getcwd())
   continuous_player_search()


    


main()
