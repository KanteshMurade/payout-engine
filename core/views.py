from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum

from .models import Merchant, Payout, LedgerEntry, IdempotencyKey


# ------------------ Helper ------------------
def get_balance(merchant):
    credit = LedgerEntry.objects.filter(
        merchant=merchant, type="credit"
    ).aggregate(total=Sum("amount"))["total"] or 0

    debit = LedgerEntry.objects.filter(
        merchant=merchant, type="debit"
    ).aggregate(total=Sum("amount"))["total"] or 0

    return credit - debit


# ------------------ Create Payout ------------------
@api_view(["POST"])
def create_payout(request):
    merchant_id = request.data.get("merchant_id")
    amount = request.data.get("amount_paise")
    idem_key = request.headers.get("Idempotency-Key")

    if not merchant_id or not amount:
        return Response({"error": "Missing fields"}, status=400)

    amount = int(amount)

    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)

    # Idempotency check
    if idem_key:
        existing = IdempotencyKey.objects.filter(key=idem_key).first()
        if existing:
            return Response({
                "payout_id": existing.payout.id,
                "status": existing.payout.status
            })

    with transaction.atomic():
        balance = get_balance(merchant)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        payout = Payout.objects.create(
            merchant=merchant,
            amount=amount,
            status="pending"
        )

        # Debit ledger
        LedgerEntry.objects.create(
            merchant=merchant,
            amount=amount,
            type="debit"
        )

        if idem_key:
            IdempotencyKey.objects.create(
                key=idem_key,
                payout=payout
            )

    return Response({
        "payout_id": payout.id,
        "status": payout.status
    })


# ------------------ Payout History ------------------
@api_view(["GET"])
def payout_list(request):
    payouts = Payout.objects.all().order_by("-id")

    data = [
        {
            "id": p.id,
            "amount": p.amount,
            "status": p.status
        }
        for p in payouts
    ]

    return Response(data)


# ------------------ Balance ------------------
@api_view(["GET"])
def get_balance_view(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"balance": 0})

    balance = get_balance(merchant)
    return Response({"balance": balance})


# ------------------ Add Credit ------------------
@api_view(["POST"])
def add_credit(request):
    merchant_id = request.data.get("merchant_id")
    amount = request.data.get("amount")

    if not merchant_id or not amount:
        return Response({"error": "Missing fields"}, status=400)

    merchant, _ = Merchant.objects.get_or_create(
        id=merchant_id,
        defaults={"name": f"Merchant {merchant_id}"}
    )

    LedgerEntry.objects.create(
        merchant=merchant,
        amount=int(amount),
        type="credit"
    )

    return Response({"message": "Balance added"})