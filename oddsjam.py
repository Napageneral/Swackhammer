import json
import webbrowser
from collections import defaultdict

import requests
import pandas as pd
import sportsbooks
import time
import util
from sys import getsizeof


api_key = "f156bb5b-79c0-48ee-802d-d69676a8ed39"
def get_games():
    api_url = 'https://api-external.oddsjam.com/api/v2/games?key={}'.format(api_key)
    params = []
    # params.append(["sport", "mma"])

    response = requests.get(api_url, params=params)

    response_json = response.json()
    data = response_json['data']
    num_odds = 0
    size_odds = 0
    for item in data:
        # print(item)
        num, size = get_odds(item['id'])
        num_odds += num
        size_odds += size

    print(num_odds)
    print(size_odds)

def new_market_stats(market_dict, market_name):
    mean_odds = defaultdict(lambda: 0)
    odds_counter = defaultdict(lambda: 0)
    max_odds = defaultdict(lambda: float('-inf'))
    market_dict[market_name] = [mean_odds, max_odds, odds_counter]

def update_market_stats(market_dict, market_name, bet_name, price):
    mean_odds, max_odds, odds_counter = market_dict[market_name]
    odds_counter[bet_name] += 1
    mean_odds[bet_name] += util.american_to_decimal(price)
    if price > max_odds[bet_name]:
        max_odds[bet_name] = price

def calculate_mean_market_stats(market_dict):
    for market in market_dict:
        mean_odds, max_odds, odds_counter = market_dict[market]
        for bet_name in mean_odds:
            mean_odds[bet_name] = round(util.decimal_to_american(mean_odds[bet_name] / odds_counter[bet_name]), 1)

def print_market_dict(market_dict):
    for market in market_dict:
        mean_odds, max_odds, odds_counter = market_dict[market]
        print("Market Name: ", market)
        print("Mean Odds: ", dict(mean_odds))
        print("Best Odds: ", dict(max_odds))
        print("Number of Odds: ", dict(odds_counter))
        print("")

def get_odds(game_id):
    api_url = 'https://api-external.oddsjam.com/api/v2/game-odds?key={}'.format(api_key)
    params = []
    params.append(["game_id", game_id])
    for book in sportsbooks.sportsbooks:
        params.append(["sportsbook", book])

    response = requests.get(api_url, params=params)
    response_json = response.json()

    num_odds = 0
    size_odds = 0

    data = response_json['data']
    for item in data:
        sport = item['sport']
        league = item['league']
        start_date = item['start_date']
        home_team = item['home_team']
        away_team = item['away_team']
        is_live = item['is_live']
        odds = item['odds']
        num_odds = len(odds)
        size_odds = getsizeof(odds)
        market_dict = {}
        print(f"Sport: {sport}. Match: {home_team} vs. {away_team}. Start Date: {start_date}")
        for line in odds:
            team_name = line['name']
            price = line['price']
            market_name = line['market_name']
            if market_name not in market_dict:
                new_market_stats(market_dict, market_name)
            update_market_stats(market_dict, market_name, team_name, price)

        calculate_mean_market_stats(market_dict)
        print_market_dict(market_dict)

    return num_odds, size_odds


def run():
    start_time = time.time()
    get_games()
    print("--- %s seconds ---" % (time.time() - start_time))
    # get_odds('97531-21212-2023-01')

if __name__ == '__main__':
    run()