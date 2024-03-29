import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from util import scroll_til_element_centered

player_name = "Tyler Brandt"
bookie_name = "williamHill"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://www.williamhill.com/us/co/bet/'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "button.Button.account-button")[0].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input#user")[0].send_keys(email)
    driver.find_elements(By.CSS_SELECTOR, "input#password")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#submit").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):
    mma_url = "https://www.williamhill.com/us/co/bet/ufcmma/events/all"

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(1)

    events = driver.find_elements(By.CSS_SELECTOR, "div.Expander.competitionExpander")
    for i in range(len(events)):
        event = events[i]
        driver.execute_script("arguments[0].scrollIntoView();", event)
        if i != 0:
            event.click()

        matches = driver.find_elements(By.CSS_SELECTOR, "div.EventCard")
        for match in matches:
            competitor_one = match.find_elements(By.CSS_SELECTOR, "a.competitor.firstCompetitor")[0]
            competitor_two = match.find_elements(By.CSS_SELECTOR, "a.competitor.lastCompetitor")[0]

            bet_buttons = match.find_elements(By.CSS_SELECTOR, "div.selectionContainer")
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

    # test_bet = "Tyler Brandt_williamHill_Daniel Argueta vs. Isaac Dulgarian_moneyline_Daniel Argueta_-195"
    # test_btn = mma_bet_buttons[test_bet]
    # place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    scroll_til_element_centered(driver, bet_button)
    time.sleep(1)
    bet_button.click()
    time.sleep(1)

    if not test:
        stake_input = driver.find_element(By.CSS_SELECTOR, "input.betslipInputField")
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='place-bet-button']").click()
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
