import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import csv

# Jason Giambi
def make_player_list():
    names = """
    Alex Rodriguez
    Derek Jeter
    Alex Rodriguez
    Manny Ramirez
    Albert Pujols
    Clayton Kershaw
    Prince Fielder
    Mark Teixeira
    Dave Winfield
    David Price
    Joe Mauer
    Kevin Brown
    Robinson Cano
    Zack Greinke
    Catfish Hunter
    Max Scherzer
    Mike Hampton
    Felix Hernandez
    Alfonso Soriano
    Jason Heyward
    Mike Piazza
    Chipper Jones
    Johan Santana
    Carlos Beltran
    Ken Griffey Jr
    Bernie Williams
    Adrian Gonzalez
    Barry Zito
    Barry Bonds
    Masahiro Tanaka
    Chris Davis
    Mo Vaughn
    Jacoby Ellsbury
    Carl Crawford
    Mike Mussina
    Jon Lester
    Jim Thome
    Vernon Wells
    Mike Schmidt
    Pedro Martinez
    Matt Holliday
    David Wright
    Cliff Lee
    Ryan Howard
    Eric Hosmer
    Carlos Lee
    Jayson Werth
    Justin Verlander
    CC Sabathia
    Magglio Ordonez
    Cecil Fielder
    Greg Maddux
    Albert Belle
    Shin-Soo Choo
    Vladimir Guerrero
    Barry Bonds
    Johnny Cueto
    Torii Hunter
    Ichiro Suzuki
    Greg Maddux
    Josh Hamilton
    George Brett
    Jose Reyes
    Adrian Beltre
    Bobby Bonilla
    AJ Burnett
    Matt Cain
    Miguel Tejada
    Nolan Ryan
    JD Martinez
    JD Martinez
    Randy Johnson
    Jordan Zimmermann
    Justin Upton
    Mark McGwire
    Aramis Ramirez
    Reggie Jackson
    JD Drew
    Roger Clemens
    Adrian Beltre
    Rod Carew
    Ivan Rodriguez
    Ryan Braun"""

    # Split the string by newline character to create a list
    name_list = [name.strip() for name in names.split('\n') if name]

    return name_list

def parse_player_name(player):
    player = player.replace(' ', '-')
    return player

def request_base_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    return response

def get_spotrac_url(player, teams, type):
    if type == 'tran':
        type = 'transactions'
    
    if type == 'stat' or 'stats':
        type = 'statistics'

    for team in teams:
        domain = 'https://www.spotrac.com/mlb'
        domain_team = domain + '/' + team
        domain_team_player = domain_team + '/' + player + '/' + type + '/'

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

def continuous_contract():
    while True:
    
        player_name = input('Enter a player (X to exit): ')
        if player_name == 'x' or player_name == 'X':
            break
            
        player_ulr = get_spotrac_url(str(parse_player_name(player_name)), create_team_dict(), 'tran')

        player_info = get_player_info(make_soup(request_base_html(player_ulr)))
            
        largest_contract = get_largest_contract(player_info)

        print('player: ' + player_name)
        print('year: ' + str(largest_contract[0]))
        print('contract value: ' + str(largest_contract[1]))
        print('duration: ' + str(largest_contract[2]))
        print('team: ' + str(largest_contract[3]))
        print('\n')

        os.chdir('/Users/cadenparry/Analyzing-MLB-Contracts')
        filename = 'results-test.csv'

        # Check if the file does not exist or is empty
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'a') as file:
                file.write('player;amount;length;year;team' + '\n')

        # Read existing data
        with open(filename, 'r') as file:
            existing_data = list(csv.reader(file, delimiter=';'))

        # Prepare new data
        new_data = [player_name, str(largest_contract[1]), str(largest_contract[2]), str(largest_contract[0]), str(largest_contract[3])]

        # Check if new data already exists in the file
        if new_data not in existing_data:
            # If not, append it
            with open(filename, 'a') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(new_data)

def db_contract(player_list, team_dict):
    for player in player_list:
        player_ulr = get_spotrac_url(parse_player_name(player), team_dict, 'tran')
        response = request_base_html(player_ulr)
        player_info = get_player_info(make_soup(response))
        largest_contract = get_largest_contract(player_info)

        os.chdir('/Users/cadenparry/Analyzing-MLB-Contracts')
        filename = 'results-test.csv'

        # Check if the file does not exist or is empty
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'a') as file:
                file.write('player;amount;length;year;team' + '\n')

        # Read existing data
        with open(filename, 'r') as file:
            existing_data = list(csv.reader(file, delimiter=';'))

        # Prepare new data
        new_data = [player, str(largest_contract[1]), str(largest_contract[2]), str(largest_contract[0]), str(largest_contract[3])]

        # Check if new data already exists in the file
        if new_data not in existing_data:
            # If not, append it
            with open(filename, 'a') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(new_data)

                print(player + ' added to the file')
        else:
            print(player + ' already exists in the file')
            
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
   #os.chdir('/Users/cadenparry/Analyzing-MLB-Contracts')
   
   #continuous_player_search()

    #db_search(make_player_list(), create_team_dict())

    # for names in make_player_list():
    #     print(names)

    stat_url = get_spotrac_url('mike-trout', create_team_dict(), 'stat')
    response = request_base_html(stat_url)
    soup = make_soup(response)

    print(soup)

main()
