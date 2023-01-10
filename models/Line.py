from datetime import date


class Line:
    def __init__(self, match_id, bookmaker, odd_1, odd_2):
        self.match_id = match_id
        self.bookmaker = bookmaker
        self.odd_1 = odd_1
        self.odd_2 = odd_2
        self.payout = self.calculate_payout()
        self.timestamp = date.today()

    def decimal_odds(self, american_odds):
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / american_odds) + 1

    def calculate_payout(self):
        return (100 * self.decimal_odds(self.odd_1) + 100 * self.decimal_odds(self.odd_2)) - 200
