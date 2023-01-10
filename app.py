from __init__ import app

from scrape import scrape_best_fight_odds, scrape_odds_portal


@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/scrape')
def scrape():
    scrape_best_fight_odds()
    scrape_odds_portal()
    return '<h1>Hello from Flask & Docker</h2>'


if __name__ == "__main__":
    app.run(debug=True, port=5001)