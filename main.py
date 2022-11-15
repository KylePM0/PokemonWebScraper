# Author: Kyle Marques

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# These are XPATH constants which obtain the HTML information we require to create our Excel sheet.
# They're written as global constants as the structure from webpage to webpage remains consistent for all listed
# Pokemon.
POKEMON_NAME = '/html/body/main/h1'
NATIONAL_INDEX = '/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td/strong'
POKEMON_TYPE = '/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td'
SPECIES = '/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td'
HEIGHT = '/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td'
WEIGHT = '/html/body/main/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td'
BASE_HP = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]'
BASE_ATK = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[1]'
BASE_DEF = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[1]'
BASE_SP_ATK = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[4]/td[1]'
BASE_SP_DEF = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[1]'
BASE_SPEED = '/html/body/main/div[3]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[6]/td[1]'
CATCH_RATE = '/html/body/main/div[3]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td'
BASE_EXP = '/html/body/main/div[3]/div[2]/div/div[1]/div[3]/div/div[1]/table/tbody/tr[4]/td'


# Function which searches the national pokedex webpage for all hyperlinks that lead to a pokemon's stat webpage.
def national_pokedex_scrape(url_list):
    for pokemon in driver.find_elements(By.CLASS_NAME, "ent-name"):
        pokemon_link = pokemon.get_attribute('href')
        url_list.append(pokemon_link)


# Function that parses individual stat information from a pokemon's stat webpage and appends it to a dictionary named
# pokedex.
def pokemon_info_scrape(url_list):
    for link in url_list:
        driver.get(link)

        pokemon_name = driver.find_element(By.XPATH, POKEMON_NAME).text
        national_num = driver.find_element(By.XPATH, NATIONAL_INDEX).text
        poke_type = driver.find_element(By.XPATH, POKEMON_TYPE).text
        species = driver.find_element(By.XPATH, SPECIES).text
        height = driver.find_element(By.XPATH, HEIGHT).text
        weight = driver.find_element(By.XPATH, WEIGHT).text
        base_hp = driver.find_element(By.XPATH, BASE_HP).text
        base_atk = driver.find_element(By.XPATH, BASE_ATK).text
        base_def = driver.find_element(By.XPATH, BASE_DEF).text
        base_sp_atk = driver.find_element(By.XPATH, BASE_SP_ATK).text
        base_sp_def = driver.find_element(By.XPATH, BASE_SP_DEF).text
        base_speed = driver.find_element(By.XPATH, BASE_SPEED).text
        catch_rate = driver.find_element(By.XPATH, CATCH_RATE).text
        base_exp = driver.find_element(By.XPATH, BASE_EXP).text

        attribute_list = [pokemon_name, national_num, poke_type, species, height, weight,
                          base_hp, base_atk, base_def, base_sp_atk, base_sp_def, base_speed,
                          catch_rate, base_exp]

        add_to_pokedex(attribute_list)


# Function to add the list of statistic information into our dictionary.
def add_to_pokedex(list_of_info):
    iterator = 0
    for k in pokedex.keys():
        pokedex[k].append(list_of_info[iterator])
        iterator += 1


if __name__ == '__main__':
    # A dictionary to hold all of our pokemon stat information.
    pokedex = {"Name": [], "National#": [], "Type": [], "Species": [],
               "Height": [], "Weight": [], "Base HP": [], "Base Atk": [],
               "Base Def": [], "Sp. Atk": [], "Sp. Def": [], "Base Speed": [],
               "Catch Rate(%)": [], "Base EXP": []
               }

    # A list of column names we'll be using to create our table of information.
    table_columns = ['Name', 'National#', 'Type', 'Species', 'Height',
                     'Weight', 'Base HP', 'Base Atk', 'Base Def', 'Sp. Atk',
                     'Sp. Def', 'Base Speed', 'Catch Rate(%)', 'Base EXP']

    # Code that'll connect to our browser and open the website we need.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://pokemondb.net/pokedex/national')
    driver.implicitly_wait(10)
    driver.maximize_window()

    # We create an empty list to hold all the URLS we obtain from scraping the national pokedex webpage.
    pokemon_url_list = []
    print("Scraping for all pokemon URLS...")
    national_pokedex_scrape(pokemon_url_list)

    # With the URLS in a list, we pass it into the info_scrape function to parse individual stats of each pokemon.
    print("URLS Obtained. Scraping for individual pokemon stats...")
    pokemon_info_scrape(pokemon_url_list)

    print("Stats obtained. Writing all info to a csv file...")
    # Lastly, we use the pandas library to create a dataframe of all the information we collected.
    # Data is ordered by columns named in the table_columns list.
    data_frame = pd.DataFrame(pokedex, columns=table_columns)
    data_frame.to_excel('Pokemon_database.xlsx', index=False)

    print("Operation Complete.")
