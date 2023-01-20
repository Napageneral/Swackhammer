import time

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

player_name = "Tyler Brandt"
bookie_name = "betmgm"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://sports.co.betmgm.com/en/sports'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "span.menu-item-txt")[1].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input#userId")[0].send_keys(email)
    driver.find_elements(By.CSS_SELECTOR, "input[name='password']")[0].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.login.w-100.btn.btn-primary").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):
    mma_url = "https://sports.co.betmgm.com/en/sports/mma-45/betting/usa-9"

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(1)

    matches = driver.find_elements(By.CSS_SELECTOR, "ms-event.grid-event")
    for match in matches:
        competitors = match.find_elements(By.CSS_SELECTOR, "div.participant")
        competitor_names = []
        #Clean span out of name
        for competitor in competitors:
            span = competitor.find_element(By.CSS_SELECTOR, "span")
            competitor_name = competitor.text.replace(span.text, "")
            competitor_name = competitor_name.replace('\n', ' ').replace('\r', '').strip()
            competitor_names.append(competitor_name)

        bet_buttons = match.find_elements(By.CSS_SELECTOR, "ms-option.grid-option")
        event_name = competitor_names[0] + " vs. " + competitor_names[1]
        market_name = "moneyline"
        bb1 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_names[0], bet_buttons[0].text))
        bb2 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_names[1], bet_buttons[1].text))
        print(bb1)
        print(bb2)
        mma_bet_buttons[bb1] = bet_buttons[0]
        mma_bet_buttons[bb2] = bet_buttons[1]

    test_bet = "Tyler Brandt_betmgm_Nick Fiore vs. Mateusz Rebecki_moneyline_Mateusz Rebecki_-700"
    test_btn = mma_bet_buttons[test_bet]
    place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    driver.execute_script("arguments[0].scrollIntoView();", bet_button)
    bet_button.click()
    time.sleep(1)

    if not test:
        stake_input = driver.find_element(By.CSS_SELECTOR, "input.stake-input-value")
        stake_input.clear()
        stake_input.send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button.betslip-place-button").click()
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
