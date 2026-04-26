from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Merchant, Payout, LedgerEntry, IdempotencyKey
from .utils import get_balance


@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get('merchant_id')
    amount = request.data.get('amount_paise')
    idempotency_key = request.headers.get('Idempotency-Key')

    if not merchant_id or not amount:
        return Response({"error": "Missing fields"}, status=400)

    # Auto create merchant if not exists
    merchant, created = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )

    # Give initial balance only once
    if created:
        LedgerEntry.objects.create(
            merchant=merchant,
            amount=100000,
            type="credit"
        )

    # Idempotency check
    if idempotency_key:
        existing = IdempotencyKey.objects.filter(key=idempotency_key).first()
        if existing:
            return Response({
                "payout_id": existing.payout.id,
                "status": existing.payout.status
            })

    # Balance check
    balance = get_balance(merchant)
    if balance < int(amount):
        return Response({"error": "Insufficient balance"}, status=400)

    # Create payout
    payout = Payout.objects.create(
        merchant=merchant,
        amount=int(amount),
        status="pending"
    )

    # Debit entry
    LedgerEntry.objects.create(
        merchant=merchant,
        amount=int(amount),
        type="debit"
    )

    # Save idempotency
    if idempotency_key:
        IdempotencyKey.objects.create(key=idempotency_key, payout=payout)

    return Response({
        "payout_id": payout.id,
        "status": payout.status
    })


@api_view(['GET'])
def payout_list(request):
    payouts = Payout.objects.all().order_by('-id')
    data = [
        {
            "id": p.id,
            "amount": p.amount,
            "status": p.status
        }
        for p in payouts
    ]
    return Response(data)


@api_view(['GET'])
def get_balance_view(request, merchant_id):
    merchant, _ = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )

    balance = get_balance(merchant)
    return Response({"balance": balance})
