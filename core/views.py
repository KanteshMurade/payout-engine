from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Merchant, Payout, LedgerEntry, IdempotencyKey
from django.shortcuts import get_object_or_404
from .utils import get_balance

@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount_paise", 0))
    key = request.headers.get("Idempotency-Key")

    merchant, _ = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )

    if IdempotencyKey.objects.filter(key=key).exists():
        payout = IdempotencyKey.objects.get(key=key).payout
        return Response({"payout_id": payout.id, "status": payout.status})

    balance = get_balance(merchant)

    if balance < amount:
        return Response({"error": "Insufficient balance"}, status=400)

    payout = Payout.objects.create(
        merchant=merchant,
        amount=amount,
        status="pending"
    )

    LedgerEntry.objects.create(
        merchant=merchant,
        amount=-amount,
        type="debit"
    )

    IdempotencyKey.objects.create(key=key, payout=payout)

    return Response({"payout_id": payout.id, "status": payout.status})


@api_view(['GET'])
def payout_list(request):
    payouts = Payout.objects.all().values()
    return Response(list(payouts))


@api_view(['GET'])
def get_balance_view(request, merchant_id):
    merchant, _ = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )
    balance = get_balance(merchant)
    return Response({"balance": balance})


@api_view(['POST'])
def add_credit(request):
    merchant_id = request.data.get("merchant_id")
    amount = int(request.data.get("amount", 0))

    merchant, _ = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )

    LedgerEntry.objects.create(
        merchant=merchant,
        amount=amount,
        type="credit"
    )

    return Response({"status": "credited"})