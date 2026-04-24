from celery import shared_task
import random
from django.utils import timezone
from datetime import timedelta
from .models import Payout, LedgerEntry
from .services import update_status

@shared_task
def process_single_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)

    if payout.status != 'pending':
        return

    update_status(payout, 'processing')

    r = random.random()

    if r < 0.7:
        update_status(payout, 'completed')

    elif r < 0.9:
        update_status(payout, 'failed')

        # refund
        LedgerEntry.objects.create(
            merchant=payout.merchant,
            amount_paise=payout.amount_paise,
            type='credit'
        )

    else:
        # simulate "stuck in processing"
        pass


@shared_task
def retry_stuck_payouts():
    threshold = timezone.now() - timedelta(seconds=30)

    stuck = Payout.objects.filter(
        status='processing',
        created_at__lt=threshold,
        retry_count__lt=3
    )

    for payout in stuck:
        payout.retry_count += 1
        payout.save()

        process_single_payout.delay(payout.id)

    # final fail after retries
    failed = Payout.objects.filter(
        status='processing',
        retry_count__gte=3
    )

    for payout in failed:
        update_status(payout, 'failed')

        LedgerEntry.objects.create(
            merchant=payout.merchant,
            amount_paise=payout.amount_paise,
            type='credit'
        )