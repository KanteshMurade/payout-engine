from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import *
from .utils import get_balance


@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount_paise"))
    idem_key = request.headers.get("Idempotency-Key")

    if not idem_key:
        return Response({"error": "Missing Idempotency-Key"}, status=400)

    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Invalid merchant"}, status=400)

    # ✅ Idempotency check
    existing = IdempotencyKey.objects.filter(key=idem_key, merchant=merchant).first()
    if existing:
        return Response({
            "payout_id": existing.payout.id,
            "status": existing.payout.status
        })

    # ✅ Concurrency-safe block
    with transaction.atomic():
        merchant_locked = Merchant.objects.select_for_update().get(id=merchant_id)

        balance = get_balance(merchant_locked)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        payout = Payout.objects.create(
            merchant=merchant_locked,
            amount=amount,
            status="pending"
        )

        # hold funds
        LedgerEntry.objects.create(
            merchant=merchant_locked,
            amount=amount,
            type="debit"
        )

        IdempotencyKey.objects.create(
            key=idem_key,
            merchant=merchant_locked,
            payout=payout
        )

    return Response({
        "payout_id": payout.id,
        "status": payout.status
    })


@api_view(['GET'])
def payout_list(request):
    payouts = Payout.objects.all().order_by('-id')
    data = []

    for p in payouts:
        data.append({
            "id": p.id,
            "amount": p.amount,
            "status": p.status
        })

    return Response(data)


@api_view(['GET'])
def balance(request):
    merchant_id = request.GET.get("merchant_id")
    merchant = Merchant.objects.get(id=merchant_id)

    return Response({
        "balance": get_balance(merchant)
    })


@api_view(['POST'])
def add_credit(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount"))

    merchant = Merchant.objects.get(id=merchant_id)

    LedgerEntry.objects.create(
        merchant=merchant,
        amount=amount,
        type="credit"
    )

    return Response({"message": "credited"})