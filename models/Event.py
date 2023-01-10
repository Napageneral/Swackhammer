from datetime import date
import string
import random


class Event:
    def __init__(self, event_name, event_date, event_location, event_time, promotion):
        self.event_id = self.id_generator()
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        self.event_time = event_time
        self.promotion = promotion
        self.timestamp = date.today()

    def __init__(self, event_id, event_name, event_date, event_location, event_time, promotion):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        self.event_time = event_time
        self.promotion = promotion
        self.timestamp = date.today()

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))