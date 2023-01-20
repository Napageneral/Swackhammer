import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By

from util import scroll_til_element_centered

player_name = "Tyler Brandt"
bookie_name = "foxbet"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://co.foxbet.com/'
    driver.get(login_url)

    time.sleep(3)
    driver.find_elements(By.CSS_SELECTOR, "input#userID")[0].send_keys(username)
    driver.find_elements(By.CSS_SELECTOR, "input#password")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#loginButton").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):

    home_url = 'https://co.foxbet.com/'

    mma_bet_buttons = {}
    # driver.get(home_url)
    # time.sleep(3)
    #
    # sport_icon_header = driver.find_element(By.CSS_SELECTOR, "div.groupHeader")
    # all_sports = sport_icon_header.find_elements(By.CSS_SELECTOR, "li")
    # mma_button = sport_icon_header.find_element(By.CSS_SELECTOR, "button[title='MMA']")
    # mma_button.click()

    mma_url = 'https://co.foxbet.com/#/mma/competitions'
    driver.get(mma_url)
    time.sleep(3)

    mma_event_urls = []
    event_header = driver.find_element(By.CSS_SELECTOR, "div#sideAZRegions")
    events = event_header.find_elements(By.CSS_SELECTOR, "a")
    for event in events:
        mma_event_urls.append(event.get_attribute("href"))

    print(mma_event_urls)

    for mma_event_url in mma_event_urls:
        driver.get(mma_event_url)
        time.sleep(3)

        matches = driver.find_elements(By.CSS_SELECTOR, "li.eventView")
        for match in matches:
            competitors = match.find_elements(By.CSS_SELECTOR, "span.team-name.standard-name")
            competitor_one = competitors[0]
            competitor_two = competitors[1]

            bet_buttons = match.find_elements(By.CSS_SELECTOR, "em.button__bet__odds")
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


    test_bet = "Tyler Brandt_foxbet_Islam Makhachev vs. Alex Volkanovski_moneyline_Alex Volkanovski_+230"
    test_btn = mma_bet_buttons[test_bet]
    place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    scroll_til_element_centered(driver, bet_button)
    time.sleep(1)
    bet_button.click()
    time.sleep(2)

    if not test:
        stake_input = driver.find_elements(By.CSS_SELECTOR, "input.stake__input")[1]
        # ActionChains(driver).move_to_element(stake_input).click(stake_input).perform()
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button#place-bet-button").click()
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
