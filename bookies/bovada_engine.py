import time

from selenium import webdriver
from selenium.webdriver.common.by import By

player_name = "Tyler Brandt"
bookie_name = "Bovada"


def login(driver):
    email = "tnapathy@gmail.com"
    password = "Ollyollyoxenfree!1"

    driver.get('https://www.bovada.lv/?overlay=login')
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "login-password").send_keys(password)
    driver.find_elements(By.ID, "login-submit")[0].click()
    time.sleep(3)

def get_mma_bet_buttons(driver):
    mma_bet_buttons = {}
    driver.get('https://www.bovada.lv/sports/ufc-mma')
    time.sleep(1)
    mma_events = driver.find_elements(By.CLASS_NAME, "grouped-events")
    for mma_event in mma_events:
        matches = mma_event.find_elements(By.TAG_NAME, "sp-coupon")
        for match in matches:
            match_date = match.find_element(By.CLASS_NAME, "scores")
            competitors = match.find_elements(By.CLASS_NAME, "competitor-name")
            bet_buttons = match.find_elements(By.CLASS_NAME, "bet-btn")
            event_name = competitors[0].text + " vs. " + competitors[1].text
            event_date = match_date.text
            market_name = "moneyline"
            bb1 = '_'.join((player_name, bookie_name, event_name, market_name, competitors[0].text, bet_buttons[0].text))
            bb2 = '_'.join((player_name, bookie_name, event_name, market_name, competitors[1].text, bet_buttons[1].text))
            mma_bet_buttons[bb1] = bet_buttons[0]
            mma_bet_buttons[bb2] = bet_buttons[1]


    for event_info, bet_button in mma_bet_buttons.items():
        print(event_info)


    place_bet(driver, mma_bet_buttons['Tyler Brandt_Bovada_Priscila Cachoeira vs. Sijara Eubanks_moneyline_Priscila Cachoeira_+193'], 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    bet_button.click()
    time.sleep(1)

    if not test:
        driver.find_element(By.ID, "default-input--risk").send_keys(str(bet_amount))
        # TODO: check for limits or lack of funds
        driver.find_element(By.CLASS_NAME, "place-bets").click()
    #TODO: check for success or failure


def bovada_engine():
    driver = webdriver.Chrome()
    login(driver)
    get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    bovada_engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
