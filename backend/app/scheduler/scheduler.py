import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started.")

    def stop(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped.")

    def add_job(self, func, job_id: str, minutes: int = 15, **kwargs):
        self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(minutes=minutes),
            id=job_id,
            replace_existing=True,
            kwargs=kwargs
        )
        logger.info(f"Added job {job_id} to run every {minutes} minutes.")

scheduler_service = SchedulerService()
