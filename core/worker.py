import time
import random
from django.utils import timezone
from core.models import *
from django.db import transaction

def run_worker():
    while True:
        payouts = Payout.objects.filter(status='pending')

        for p in payouts:
            with transaction.atomic():
                p.status = 'processing'
                p.save()

            time.sleep(2)

            outcome = random.choices(
                ['success', 'fail', 'hang'],
                weights=[70, 20, 10]
            )[0]

            if outcome == 'success':
                p.status = 'completed'
                p.save()

            elif outcome == 'fail':
                with transaction.atomic():
                    p.status = 'failed'
                    p.save()

                    # refund
                    LedgerEntry.objects.create(
                        merchant=p.merchant,
                        amount=p.amount,
                        type='credit'
                    )

            else:
                # simulate retry later
                p.attempts += 1
                p.save()

        time.sleep(5)