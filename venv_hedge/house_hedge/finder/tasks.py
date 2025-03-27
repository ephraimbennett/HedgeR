from celery import shared_task
from .services import update_bets

@shared_task
def test_task():
    print("Initializing...")
    update_bets()
