import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from util import scroll_til_element_centered

player_name = "Tyler Brandt"
bookie_name = "elitesportsbook"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "BapaGeneral"
    password = "Brodee99!1"

    login_url = 'https://co.elitesportsbook.com/sports/home.sbk'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "div.glyphicon-log-in")[0].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input#CRM_form_username")[0].send_keys(username)
    driver.find_elements(By.CSS_SELECTOR, "input#CRM_form_password")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#CRM_btn_login").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):

    mma_url = 'https://co.elitesportsbook.com/sports/mma-betting/mma-odds.sbk'

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(1)

    matches = driver.find_elements(By.CSS_SELECTOR, "div.eventbox")
    for match in matches:
        competitor_one = match.find_elements(By.CSS_SELECTOR, "span#firstTeamName")[0]
        competitor_two = match.find_elements(By.CSS_SELECTOR, "span#secondTeamName")[0]

        bet_buttons = match.find_elements(By.CSS_SELECTOR, "div.column.total.pull-right")
        event_name = competitor_one.text + " vs. " + competitor_two.text
        market_name = "moneyline"
        bb1 = '_'.join(
            (player_name, bookie_name, event_name, market_name, competitor_one.text, bet_buttons[0].text))
        bb2 = '_'.join(
            (player_name, bookie_name, event_name, market_name, competitor_two.text, bet_buttons[1].text))
        print(bb1)
        print(bb2)
        mma_bet_buttons[bb1] = bet_buttons[0]
        mma_bet_buttons[bb2] = bet_buttons[1]


    test_bet = "Tyler Brandt_circasport_SEAN STRICKLAND vs. NASSOURDINE IMAVOV_moneyline_NASSOURDINE IMAVOV_-115"
    test_btn = mma_bet_buttons[test_bet]
    place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    scroll_til_element_centered(driver, bet_button)
    time.sleep(1)
    bet_button.click()
    time.sleep(1)

    if not test:
        stake_input = driver.find_element(By.CSS_SELECTOR, "input[customattrbettype='Straight Wager']")
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button#cBtn").click()
        #TODO: check for success or failure


def engine():
    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    driver = webdriver.Chrome(options=opts)
    #login(driver)
    get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
