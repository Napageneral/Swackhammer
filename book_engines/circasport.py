import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from util import scroll_til_element_centered

player_name = "Tyler Brandt"
bookie_name = "circasport"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://co.circasports.com/sports'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "button.login_btn")[0].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input#username")[0].send_keys(email)
    driver.find_elements(By.CSS_SELECTOR, "input#password")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#login_btn_dialog").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):

    home_url = 'https://co.circasports.com'
    driver.get(home_url)
    time.sleep(1)
    ufc_button = driver.find_elements(By.XPATH, "//a[contains(text(), 'UFC')]")[0]
    mma_url = ufc_button.get_attribute('href')

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(1)

    event_tabs = driver.find_elements(By.CSS_SELECTOR, "div.v-tabs__div.tab")
    print(event_tabs)
    for i in range(len(event_tabs)-1):
        event = event_tabs[i]
        driver.execute_script("scrollBy(0,-document.body.scrollTop)")
        time.sleep(1)
        if i != 0:
            event.click()
            time.sleep(1)

        matches = driver.find_elements(By.CSS_SELECTOR, "div.event")
        print(len(matches))
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


    # test_bet = "Tyler Brandt_circasport_DEIVESON FIGUEIREDO vs. BRANDON MORENO_moneyline_BRANDON MORENO_-110"
    # test_btn = mma_bet_buttons[test_bet]
    # place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    scroll_til_element_centered(driver, bet_button)
    time.sleep(1)
    bet_button.click()
    time.sleep(1)

    if not test:
        stake_input = driver.find_element(By.CSS_SELECTOR, "input#wagerBetSlipIdPerSelection")
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button#btnPlaceBet").click()
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
