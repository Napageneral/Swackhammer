from datetime import date
import string
import random


class Match:
    def __init__(self, status, match_name, match_date, event_name, event_id,
                 fighter_1, fighter_2, average_line_1, average_line_2, best_line_1, best_line_2):
        self.match_id = self.id_generator()
        self.status = status
        self.match_name = match_name
        self.match_date = match_date
        self.event_name = event_name
        self.event_id = event_id
        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2
        self.average_line_1 = average_line_1
        self.average_line_2 = average_line_2
        self.average_payout = self.calculate_payout(average_line_1, average_line_2)
        self.best_line_1 = best_line_1
        self.best_line_2 = best_line_2
        self.best_payout = self.calculate_payout(best_line_1, best_line_2)
        self.timestamp = date.today()

    def __init__(self, match_id, status, match_name, match_date, event_name, event_id,
                 fighter_1, fighter_2, average_line_1, average_line_2, best_line_1, best_line_2):
        self.match_id = match_id
        self.status = status
        self.match_name = match_name
        self.match_date = match_date
        self.event_name = event_name
        self.event_id = event_id
        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2
        self.average_line_1 = average_line_1
        self.average_line_2 = average_line_2
        self.average_payout = self.calculate_payout(average_line_1, average_line_2)
        self.best_line_1 = best_line_1
        self.best_line_2 = best_line_2
        self.best_payout = self.calculate_payout(best_line_1, best_line_2)
        self.timestamp = date.today()

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def decimal_odds(self, american_odds):
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / american_odds) + 1

    def calculate_payout(self, odd_1, odd_2):
        return (100 * self.decimal_odds(odd_1) + 100 * self.decimal_odds(odd_2)) - 200
