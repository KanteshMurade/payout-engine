from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import *
from .utils import get_balance
import random
import time


@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount_paise"))
    key = request.headers.get("Idempotency-Key")

    merchant = Merchant.objects.get(id=merchant_id)

    # IDEMPOTENCY
    existing = IdempotencyKey.objects.filter(
        key=key, merchant=merchant
    ).first()

    if existing:
        return Response(existing.response)

    # CONCURRENCY
    with transaction.atomic():
        merchant_locked = Merchant.objects.select_for_update().get(id=merchant.id)

        balance = get_balance(merchant_locked)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        LedgerEntry.objects.create(
            merchant=merchant_locked,
            amount=-amount,
            type="hold"
        )

        payout = Payout.objects.create(
            merchant=merchant_locked,
            amount=amount,
            status="pending",
            idempotency_key=key
        )

    process_payout(payout.id)

    response = {
        "payout_id": payout.id,
        "status": payout.status
    }

    IdempotencyKey.objects.create(
        key=key,
        merchant=merchant,
        response=response
    )

    return Response(response)


def process_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)

    payout.status = "processing"
    payout.save()

    time.sleep(2)

    r = random.randint(1, 100)

    if r <= 70:
        payout.status = "completed"
    else:
        payout.status = "failed"

        LedgerEntry.objects.create(
            merchant=payout.merchant,
            amount=payout.amount,
            type="refund"
        )

    payout.save()


@api_view(['GET'])
def payout_list(request):
    merchant_id = request.GET.get("merchant_id")

    payouts = Payout.objects.filter(merchant_id=merchant_id)

    data = [
        {
            "id": p.id,
            "amount": p.amount,
            "status": p.status
        }
        for p in payouts
    ]

    return Response(data)


@api_view(['POST'])
def add_credit(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount"))

<<<<<<< HEAD
    merchant = Merchant.objects.get(id=merchant_id)

    LedgerEntry.objects.create(
        merchant=merchant,
        amount=amount,
        type="credit"
    )

    return Response({"message": "credit added"})
=======
    return Response({
        "id": merchant.id,
        "name": merchant.name,
        "balance": merchant.balance
    })

@api_view(['POST'])
def add_balance(request):
    merchant_id = request.data.get("merchant_id")
    amount = request.data.get("amount")

    if not merchant_id or not amount:
        return Response({"error": "Missing fields"}, status=400)

    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)

    merchant.balance += int(amount)
    merchant.save()

    return Response({
        "message": "Balance added",
        "balance": merchant.balance
    })
>>>>>>> 189d1be0b906f5b486987d26560ad3d988ef0f42
