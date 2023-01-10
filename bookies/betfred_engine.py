import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

player_name = "Tyler Brandt"
bookie_name = "betfred"


def login(driver):
    email = "tnapathy@gmail.com"
    username = "Napageneral"
    password = "Brodee99!1"

    login_url = 'https://co.betfredsports.com/sports/'
    driver.get(login_url)

    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "a.button.logged_out")[0].click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, "input.text.email.required")[1].send_keys(email)
    driver.find_elements(By.CSS_SELECTOR, "input.text.password.required")[1].send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button#id_login_submit").click()
    time.sleep(1)

def get_mma_bet_buttons(driver):
    mma_url = "https://co.betfredsports.com/sports/sports/competition/483/mma/mma/mma/matches"

    mma_bet_buttons = {}
    driver.get(mma_url)
    time.sleep(3)

    try:
        #Load More
        driver.find_element(By.CSS_SELECTOR, "a.content-loader__load-more-link").click()
        time.sleep(1)
    except:
        pass

    matches = driver.find_elements(By.CSS_SELECTOR, "li.event-list__item")
    for match in matches:
        competitor_one_name = match.find_element(By.CSS_SELECTOR, "div.event-card__body__name__home").text
        competitor_two_name = match.find_element(By.CSS_SELECTOR, "div.event-card__body__name__away").text
        bet_buttons = match.find_elements(By.CSS_SELECTOR, "span.button--outcome__price")
        event_name = competitor_one_name + " vs. " + competitor_two_name
        market_name = "moneyline"
        bb1 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_one_name, bet_buttons[0].text))
        bb2 = '_'.join((player_name, bookie_name, event_name, market_name, competitor_two_name, bet_buttons[1].text))
        print(bb1)
        print(bb2)
        mma_bet_buttons[bb1] = bet_buttons[0]
        mma_bet_buttons[bb2] = bet_buttons[1]

    test_bet = "Tyler Brandt_barstool_Terrance McKinney vs. Ismael Bonfim_moneyline_Ismael Bonfim_+100"
    test_btn = mma_bet_buttons[test_bet]
    place_bet(driver, test_btn, 1)

    return mma_bet_buttons

def place_bet(driver, bet_button, bet_amount, test=False):
    bet_button.click()
    time.sleep(1)

    if not test:
        driver.find_element(By.CSS_SELECTOR, "input.form-control.stake.ob-betting-stake-input").send_keys(str(bet_amount))
        time.sleep(1)
        # TODO: check for limits or lack of funds
        driver.find_element(By.CSS_SELECTOR, "button.button--place-betslip").click()
        #TODO: check for success or failure


def engine():
    driver = webdriver.Chrome()
    #login(driver)
    get_mma_bet_buttons(driver)
    time.sleep(60)


if __name__ == '__main__':
    engine()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
