from datetime import datetime, timedelta


class Timer:

    def __init__(self, rewind: timedelta = None, forward: timedelta = None):
        self.start_time = datetime.now()
        if rewind:
            self.start_time = self.start_time - rewind
        if forward:
            self.start_time = self.start_time + forward

    @property
    def current_time(self):
        return datetime.now()

    @property
    def elapsed_time(self):
        return self.current_time - self.start_time

    def is_new_since_start_time(self, time_string: str) -> bool:
        number = int("".join([c for c in time_string if c.isdigit()]))
        time_difference = None
        if "hour" in time_string.lower():
            time_difference = timedelta(hours=number)
        if "min" in time_string.lower():
            time_difference = timedelta(minutes=number)
        if "day" in time_string.lower():
            time_difference = timedelta(days=number)
        return self.elapsed_time > time_difference
