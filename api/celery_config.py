"""
Configuration celery
"""

from celery import Celery

from api.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


app = Celery(
    "enerbit", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
)
app.autodiscover_tasks(["api.tasks"])


@app.task(bind=True)
def debug_task(self):
    """
    Function to debug task
    """
    print(f"Request: {self.request!r}")


if __name__ == "__main__":
    app.start()
