import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By

from util import scroll_til_element_centered

player_name = "Tyler Brandt"
bookie_name = "maverick"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://www.playmavericksports.com/sports'
    driver.get(login_url)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, "span#qa-login_btn").click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input#username")[0].send_keys(username)
    driver.find_elements(By.CSS_SELECTOR, "input#password")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#login_btn_dialog").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):

    mma_bet_buttons = {}
    mma_url = 'https://www.playmavericksports.com/sports/navigation/10940.1/10941.1'
    driver.get(mma_url)
    time.sleep(1)

    matches = driver.find_elements(By.CSS_SELECTOR, "div.event")
    for match in matches:
        competitor_one = match.find_elements(By.CSS_SELECTOR, "div.eventTitle.away")[0]
        competitor_two = match.find_elements(By.CSS_SELECTOR, "div.eventTitle.home")[0]

        bet_button_container = match.find_element(By.CSS_SELECTOR, "div.market.money")
        bet_buttons = bet_button_container.find_elements(By.CSS_SELECTOR, "div.flex")
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


    # test_bet = "Tyler Brandt_maverick_Imavov, Nassourdine vs. Strickland, Sean_moneyline_Strickland, Sean_-105"
    # test_btn = mma_bet_buttons[test_bet]
    # place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    scroll_til_element_centered(driver, bet_button)
    time.sleep(1)
    bet_button.click()
    time.sleep(2)

    if not test:
        stake_input = driver.find_elements(By.CSS_SELECTOR, "input#wagerBetSlipIdPerSelection")[0]
        # ActionChains(driver).move_to_element(stake_input).click(stake_input).perform()
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button.placebetbtn").click()
        #TODO: check for success or failure


def engine():
    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    driver = webdriver.Chrome(options=opts)
    login(driver)
    get_mma_bet_buttons(driver)
    #return driver
    #time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
