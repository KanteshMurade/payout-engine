from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import *
from .utils import get_balance
from .tasks import process_single_payout   

@api_view(['POST'])
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)def create_payout(request):
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)    try:
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        merchant_id = request.data.get('merchant_id')
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        amount = request.data.get('amount_paise')
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        key = request.headers.get('Idempotency-Key')
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        # ✅ ADD THIS (VERY IMPORTANT)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        if not merchant_id or not amount:
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            return Response({"error": "Missing merchant_id or amount"}, status=400)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        amount = int(amount)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        merchant = Merchant.objects.get(id=merchant_id)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        cutoff = timezone.now() - timedelta(hours=24)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        existing = IdempotencyKey.objects.filter(
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            key=key,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            merchant=merchant,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            created_at__gte=cutoff
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        ).first()
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        if existing:
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            return Response(existing.response_data)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        with transaction.atomic():
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            merchant_locked = Merchant.objects.select_for_update().get(id=merchant.id)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            balance = get_balance(merchant_locked)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            if balance < amount:
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)                return Response({"error": "Insufficient balance"}, status=400)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            payout = Payout.objects.create(
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)                merchant=merchant_locked,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)                amount_paise=amount,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)                status='pending',
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)                idempotency_key=key
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            )
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        process_single_payout.delay(payout.id)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        response = {
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            "payout_id": payout.id,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            "status": payout.status
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        }
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        IdempotencyKey.objects.create(
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            key=key,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            merchant=merchant,
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)            response_data=response
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        )
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        return Response(response)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)    except Exception as e:
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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
        return Response({"error": str(e)}, status=500)        return Response({"error": str(e)}, status=500)
def create_payout(request):
    try:
        merchant_id = request.data.get('merchant_id')
        amount_val = request.data.get('amount_paise')
        key = request.headers.get('Idempotency-Key')

        # ✅ Validation
        if not merchant_id or not amount_val:
            return Response({"error": "Missing fields"}, status=400)

        try:
            amount = int(amount_val)
        except:
            return Response({"error": "Amount must be number"}, status=400)

        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Invalid merchant"}, status=400)

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

            balance = get_balance(merchant_locked) or 0

            if balance < amount:
                return Response({"error": "Insufficient balance"}, status=400)

            payout = Payout.objects.create(
                merchant=merchant_locked,
                amount_paise=amount,
                status='pending',
                idempotency_key=key
            )

        # async task
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