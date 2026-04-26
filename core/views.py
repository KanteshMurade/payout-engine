from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from .models import Merchant, Payout, IdempotencyKey
from .utils import get_balance
from .tasks import process_single_payout


@api_view(['POST'])
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant does not exist"}, status=400)

        cutoff = timezone.now() - timedelta(hours=24)

        existing = IdempotencyKey.objects.filter(
            key=key,
            merchant=merchant,
            created_at__gte=cutoff
        ).first()

        if existing:
            return Response(existing.response_data)

        with transaction.atomic():
            merchant_locked = Merchant.objects.select_for_update().get(id=merchant.id)

            balance = get_balance(merchant_locked)

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        process_single_payout.delay(payout.id)

        response = {
            "payout_id": payout.id,
            "status": payout.status
        }

        IdempotencyKey.objects.create(
            key=key,
            merchant=merchant,
            response_data=response
        )

        return Response(response)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def payout_list(request):
    payouts = Payout.objects.all().order_by('-id')[:20]

    data = []
    for p in payouts:
        data.append({
            "id": p.id,
            "amount": p.amount_paise,
            "status": p.status,
            "merchant": p.merchant.id
        })

    return Response(data)


@api_view(['GET'])
def get_balance_api(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        return Response({"balance": merchant.balance})
    except:
        return Response({"error": "Invalid merchant"}, status=400)