import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

rows_to_filter = ["Over 1½ rounds", "Under 1½ rounds", "Over 2½ rounds", "Under 2½ rounds", "Over 3½ rounds",
                  "Under 3½ rounds", "Over 4½ rounds", "Under 4½ rounds", "Fight goes to decision",
                  "Fight doesn't go to decision", "Fight is a draw", "Fight is not a draw"]

values_to_filter = ["Over ", "Under ", "in round", "result", "decision", "distance", "submission", "TKO", "draw",
                    "handicap", "scorecards", "of round", "deducted", "round ", "takedown"]

odds_portal_home_url = 'https://www.oddsportal.com'

odds_league_pages = ['https://www.oddsportal.com/mma/world/bantamweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/flyweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/heavyweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/light-heavyweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/lightweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/middleweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/welterweight-ufc-men/',
                     'https://www.oddsportal.com/mma/world/bantamweight-ufc-women/',
                     'https://www.oddsportal.com/mma/world/featherweight-ufc-women/',
                     'https://www.oddsportal.com/mma/world/strawweight-ufc-women/']


def filter_rows_by_values(df, col, values):
    return df[~df[col].isin(values)]


def filter_rows_containing_values(df, col, values):
    indices_to_remove = []

    for index, row in df.iterrows():
        if any(value in row[col] for value in values):
            indices_to_remove.append(index)
    df.drop(index=indices_to_remove, inplace=True)
    return df


def scrape_best_fight_odds():
    driver = webdriver.Chrome()
    driver.get('https://www.bestfightodds.com/')

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    tableDivs = soup.find_all("div", {"class": "table-div"})

    eventTables = {}
    for tablediv in tableDivs:
        eventDate = tablediv.find('span', {"class": "table-header-date"})
        eventName = tablediv.find('h1')

        if eventDate and eventName:
            tables = tablediv.find_all('table')
            df = pd.read_html(str(tables))[1] #have to get the second table because the first table only has fighter links
            expected_column_name = "Unnamed: 0"
            colname = df.columns[0]
            if colname == expected_column_name:
                df = filter_rows_containing_values(df, expected_column_name, values_to_filter)
                df.dropna(axis=1, how='all', inplace=True)
                if 'Props.2' in df.columns:
                    df.drop('Props.2', axis=1, inplace=True)
                df.replace('▲', '', regex=True, inplace=True)
                df.replace('▼', '', regex=True, inplace=True)
                df.rename(columns={expected_column_name: "Fighter"}, inplace=True)
                eventTables[(eventName.text, eventDate.text)] = df

    for key, df in eventTables.items():
        print(key[0])
        print(key[1])
        print(df.to_string())
        print("\n")

def login_odds_portal(driver):
    username = "Napageneral"
    password = "Brodee99!1"

    driver.get('https://www.oddsportal.com/login/')
    driver.find_element("name", "login-username").send_keys(username)
    driver.find_element("name", "login-password").send_keys(password)
    driver.find_elements("name", "login-submit")[1].click()

def scrape_odds_portal_match_page(driver, url):
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    colDiv = soup.find("div", {"id": "col-content"})
    matchName = colDiv.find("h1").text
    matchDate = colDiv.find("p").text
    print(matchDate)
    fighters = [x.strip() for x in matchName.split('-')]

    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))

    oddsTable = dfs[0]
    oddsTable.drop('Unnamed: 4', axis=1, inplace=True)
    oddsTable.dropna(inplace=True)
    oddsTable.rename(columns={"1": fighters[0], "2": fighters[1]}, inplace=True)
    oddsTable = oddsTable[oddsTable.Bookmakers != "Log in to display the OddsAlert!"]
    print(oddsTable.to_string())


def scrape_odds_league_page(driver, url, odds_urls):
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    tournamentTable = soup.find("table", {"id": "tournamentTable"})

    for link in tournamentTable.find_all('a', href=True):
        endpoint = odds_portal_home_url + link['href']
        if len(endpoint) > len(url):
            odds_urls.append(endpoint)

def scrape_odds_portal():
    driver = webdriver.Chrome()

    odds_urls = []
    for url in odds_league_pages:
        scrape_odds_league_page(driver, url, odds_urls)

    login_odds_portal(driver)

    #scrape_odds_portal_match_page(driver, 'https://www.oddsportal.com/mma/world/light-heavyweight-ufc-men/teixeira-glover-hill-jamahal-QumsRylD/')

    for url in odds_urls:
        scrape_odds_portal_match_page(driver, url)

    driver.close()


if __name__ == '__main__':
    scrape_best_fight_odds()
    scrape_odds_portal()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
