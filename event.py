class Event:
    def __init__(self, event_type, event_time):
        self.event_type = event_type
        self.event_time = event_time

    def __lt__(self, other):
        return self.event_time < other.event_time
