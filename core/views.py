@api_view(['POST'])
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ ADD THIS (VERY IMPORTANT)
        if not merchant_id or not amount:
            return Response({"error": "Missing merchant_id or amount"}, status=400)

        amount = int(amount)

        merchant = Merchant.objects.get(id=merchant_id)

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
        return Response({"error": str(e)}, status=500)
