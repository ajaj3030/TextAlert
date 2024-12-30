import schedule
import time
from typing import Callable, List

class Scheduler:
    def __init__(self, schedule_times: List[str], task: Callable):
        self.schedule_times = schedule_times
        self.task = task

    def start(self):
        for time_str in self.schedule_times:
            schedule.every().day.at(time_str).do(self.task)

        while True:
            schedule.run_pending()
            time.sleep(1) 