import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

player_name = "Tyler Brandt"
bookie_name = "bet365"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://www.co.bet365.com/#/HO/'
    driver.get(login_url)

    while driver.current_url == login_url:
        WebDriverWait(driver, timeout=180, poll_frequency=1)

    # time.sleep(3)
    # driver.find_element(By.CLASS_NAME, "hm-MainHeaderRHSLoggedOutWide_Login").click()
    # time.sleep(1)
    # driver.find_element(By.CLASS_NAME, "lms-StandardLogin_Username").send_keys(username)
    # driver.find_element(By.CLASS_NAME, "lms-StandardLogin_Password").send_keys(password)
    #driver.find_element(By.CLASS_NAME, "lms-LoginButton_Text").click()
    print('testing driverwait')

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

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    bet_button.click()
    time.sleep(1)

    if not test:
        driver.find_element(By.ID, "default-input--risk").send_keys(str(bet_amount))
        # TODO: check for limits or lack of funds
        driver.find_element(By.CLASS_NAME, "place-bets").click()
    #TODO: check for success or failure


def engine():
    driver = webdriver.Chrome()
    login(driver)
    #get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
