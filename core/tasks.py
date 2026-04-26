from celery import shared_task
from .models import Payout
import time


@shared_task
def process_single_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)

    time.sleep(5)  # simulate processing

    payout.status = "success"
    payout.save()