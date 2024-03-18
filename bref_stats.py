import requests
from bs4 import BeautifulSoup
import time
import os
import csv
player_url_finished_dict = {'Ken Griffey': ['https://www.baseball-reference.com/players/g/griffke02.shtml', 'https://www.baseball-reference.com/players/g/griffke01.shtml'], 'Alex Rodriguez': ['https://www.baseball-reference.com/players/r/rodrial01.shtml'], 'Derek Jeter': ['https://www.baseball-reference.com/players/j/jeterde01.shtml'], 'Manny Ramirez': ['https://www.baseball-reference.com/players/r/ramirma03.shtml', 'https://www.baseball-reference.com/players/r/ramirma02.shtml', 'https://www.baseball-reference.com/players/r/ramirma01.shtml'], 'Albert Pujols': ['https://www.baseball-reference.com/players/p/pujolal01.shtml'], 'Clayton Kershaw': ['https://www.baseball-reference.com/players/k/kershcl01.shtml'], 'Prince Fielder': ['https://www.baseball-reference.com/players/f/fieldpr01.shtml'], 'Mark Teixeira': ['https://www.baseball-reference.com/players/t/teixema01.shtml'], 'Dave Winfield': ['https://www.baseball-reference.com/players/w/winfida01.shtml'], 'David Price': ['https://www.baseball-reference.com/players/p/priceda01.shtml'], 'Joe Mauer': ['https://www.baseball-reference.com/players/m/mauerjo01.shtml'], 'Kevin Brown': ['https://www.baseball-reference.com/players/b/brownke03.shtml']}
def test_list():
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
    Rod Carew
    Ivan Rodriguez
    Ryan Braun"""

    # Split the string by newline character to create a list
    name_list = [name.strip() for name in names.split('\n') if name]

    return name_list

def create_bref_urls():

    from tqdm import tqdm 

    player_dict = {}

    names = test_list()

    for name in tqdm(names):

        base_url = 'https://www.baseball-reference.com/players/'

        name_parts = name.split()  # Split the name into parts

        # Handle names with different number of parts
        if len(name_parts) == 2:  # If the name has two parts
            first_name, last_name = name_parts
            suff = ''
        elif len(name_parts) == 3:  # If the name has three parts
            first_name, last_name, suff = name_parts
        else:
            print(f"Unexpected name format: {name}")
            continue

        first_of_last = last_name[0]

        if len(last_name) > 5:
            base_url = (base_url + first_of_last + '/' + last_name[0:5] + first_name[0:2]).lower()
        else:
            base_url = (base_url + first_of_last + '/' + last_name + first_name[0:2]).lower()

        # possible_player_urls = []
        # for i in range(5, 0, -1):
        #     final_url = base_url + '0' + str(i) + '.shtml'
        #     final_url
        #     response = requests.get(final_url)
        #     time.sleep(1)

        #     if response.status_code == 200:
        #         possible_player_urls.append(final_url)
        
        # player_dict[name] = possible_player_urls
        player_dict[name] = base_url + '01.shtml'
    return player_dict


# def main():
    # player_url = player_url_finished_dict['Albert Pujols'][0]
    # response = requests.get(player_url)
    # print(response)

# main()

# https://www.baseball-reference.com/players/g/griffke02.shtml



#  os.chdir('/Users/cadenparry/Analyzing-MLB-Contracts')
#     filename = 'bref_urls.csv'

#     with open(filename, 'w') as file:
#         writer = csv.writer(file, delimiter=';')
#         num = 0
#         writer.writerow([str(num), url])
    


