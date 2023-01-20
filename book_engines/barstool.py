import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

player_name = "Tyler Brandt"
bookie_name = "barstool"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://www.barstoolsportsbook.com/'
    driver.get(login_url)

    time.sleep(5)
    driver.find_elements(By.CLASS_NAME, "logged-out")[0].click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "input[data-qa-username]").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "input[data-qa-password]").send_keys(password)
    driver.find_element(By.CLASS_NAME, "sign-in-btn").click()
    time.sleep(20)

def get_mma_bet_buttons(driver):
    mma_url = "https://www.barstoolsportsbook.com/sports/ufc_mma/ufc"

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(5)

    matches = driver.find_elements(By.CSS_SELECTOR, "div.container.wrap.event-row.match-row")
    for match in matches:
        match_date = match.find_element(By.CSS_SELECTOR, "p.start-display.strongbody2")
        competitor_one_name = match.find_element(By.CSS_SELECTOR, "div.participant").text
        competitor_two_name = match.find_element(By.CSS_SELECTOR, "div.participant.second-participant").text
        bet_buttons = match.find_elements(By.CSS_SELECTOR, "label.outcome-card.label.event-chip-wrapper")
        odds = match.find_elements(By.CSS_SELECTOR, "div.odds")
        event_name = competitor_one_name + " vs. " + competitor_two_name
        market_name = "moneyline"
        bb1 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_one_name, odds[0].text))
        bb2 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_two_name, odds[1].text))
        print(bb1)
        print(bb2)
        mma_bet_buttons[bb1] = bet_buttons[0]
        mma_bet_buttons[bb2] = bet_buttons[1]


    # test_bet = "Tyler Brandt_barstool_Makhachev, Islam vs. Volkanovski, Alex_moneyline_Volkanovski, Alex_+265"
    # test_btn = mma_bet_buttons[test_bet]
    # place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    bet_button.click()
    time.sleep(1)

    if not test:
        driver.find_element(By.CSS_SELECTOR, "input[aria-label='Enter your wager']").send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button.wager-button").click()
        #TODO: check for success or failure


def engine():
    driver = webdriver.Chrome()
    login(driver)
    get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
