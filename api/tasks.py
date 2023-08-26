"""
Task celery from api enerbit
"""

from api.celery_config import app


@app.task(queue="queue_enerbit")
def add_event(data):
    print(data)
