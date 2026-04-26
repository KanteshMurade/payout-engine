from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Merchant, Payout


@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get("merchant_id")
    amount = request.data.get("amount_paise")

    if not merchant_id or not amount:
        return Response({"error": "Missing fields"}, status=400)

    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)

    if merchant.balance < amount:
        return Response({"error": "Insufficient balance"}, status=400)

    merchant.balance -= amount
    merchant.save()

    payout = Payout.objects.create(
        merchant=merchant,
        amount=amount,
        status="pending"
    )

    return Response({
        "payout_id": payout.id,
        "status": payout.status
    })


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


@api_view(['GET'])
def merchant_detail(request, merchant_id):
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    return Response({
        "id": merchant.id,
        "name": merchant.name,
        "balance": merchant.balance
    })