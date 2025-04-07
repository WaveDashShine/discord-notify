import datetime
from datetime import timedelta, datetime
from manhwa_checker.timer import Timer


class TestTimer:
    """
    check string parsing is works as intended with timedelta
    """

    def test_newly_available_hours(self):
        timer = Timer(rewind=timedelta(minutes=121))
        assert timer.is_new_since_start_time(time_string="2 hours ago")

    def test_newly_available_minutes(self):
        timer = Timer(rewind=timedelta(seconds=185))
        assert timer.is_new_since_start_time(time_string="3 minutes ago")

    def test_newly_available_days(self):
        timer = Timer(rewind=timedelta(hours=25))
        assert timer.is_new_since_start_time(time_string="1 day ago")

    def test_rewind(self):
        delta = timedelta(seconds=60)
        timer = Timer(rewind=delta)
        assert timer.start_time > datetime.now() - timedelta(seconds=61)
        assert timer.start_time < datetime.now() - timedelta(seconds=59)

    def test_forward(self):
        delta = timedelta(seconds=60)
        timer = Timer(forward=delta)
        assert timer.start_time < datetime.now() + timedelta(seconds=61)
        assert timer.start_time > datetime.now() + timedelta(seconds=59)
