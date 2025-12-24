from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import re

class Scheduler:
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def add_recurring_job(self, job_id: str, trigger: str, **kwargs):
        self.sched.add_job(id=job_id, trigger=trigger, **kwargs)

    def parse_and_schedule(self, text: str):
        # naive parse: "in 10 minutes <msg>"
        m = re.match(r"in\s+(\d+)\s+(seconds?|minutes?|hours?)\s+(.*)", text, re.I)
        if not m:
            raise ValueError("Try: in 10 minutes drink water")
        amount, unit, msg = int(m.group(1)), m.group(2).lower(), m.group(3)
        if unit.startswith("second"):
            delta = timedelta(seconds=amount)
        elif unit.startswith("minute"):
            delta = timedelta(minutes=amount)
        else:
            delta = timedelta(hours=amount)
        when = datetime.now() + delta
        self.sched.add_job(func=lambda: print(f"\n[Reminder] {msg} @ {datetime.now().strftime('%H:%M:%S')}"),
                           trigger="date", run_date=when)
        return when.strftime("%Y-%m-%d %H:%M:%S")
