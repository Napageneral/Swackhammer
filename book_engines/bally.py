import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

player_name = "Tyler Brandt"
bookie_name = "bally"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://co.ballybet.com/sports/home.sbk'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CLASS_NAME, "login-text")[1].click()
    time.sleep(1)
    driver.find_element(By.ID, "CRM_form_username").send_keys(username)
    driver.find_element(By.ID, "CRM_form_password").send_keys(password)
    driver.find_element(By.ID, "CRM_btn_login").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):
    mma_url = "https://co.ballybet.com/sports/mma-betting/mma-odds.sbk"

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(1)

    matches = driver.find_elements(By.CLASS_NAME, "col-sm-12")
    print(matches)
    for match in matches:
        try:
            match_date = match.find_element(By.ID, "time")
            competitor_one_name = match.find_element(By.ID, "firstTeamName").text
            competitor_two_name = match.find_element(By.ID, "secondTeamName").text
            bet_buttons = match.find_elements(By.CLASS_NAME, "market")
            event_name = competitor_one_name + " vs. " + competitor_two_name
            market_name = "moneyline"
            bb1 = '_'.join(
                (player_name, bookie_name, event_name, market_name, competitor_one_name, bet_buttons[2].text))
            bb2 = '_'.join(
                (player_name, bookie_name, event_name, market_name, competitor_two_name, bet_buttons[5].text))
            mma_bet_buttons[bb1] = bet_buttons[2]
            mma_bet_buttons[bb2] = bet_buttons[5]
        except:
            continue

    for event_info, bet_button in mma_bet_buttons.items():
        print(event_info)

    test_bet = "Tyler Brandt_bally_Isaac Dulgarian vs. Daniel Argueta_moneyline_Daniel Argueta_-215"
    test_btn = mma_bet_buttons[test_bet]
    place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    bet_button.click()
    time.sleep(1)

    if not test:
        driver.find_element(By.CSS_SELECTOR, "input[id*='betAmount']").send_keys(str(bet_amount))
        time.sleep(3)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button[id*='cBtn']").click()
        #TODO: check for success or failure


def engine():
    driver = webdriver.Chrome()
    login(driver)
    get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
