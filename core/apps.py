from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Merchant, LedgerEntry

        if not Merchant.objects.exists():
            m = Merchant.objects.create(name="Auto Merchant")
            LedgerEntry.objects.create(
                merchant=m,
                amount_paise=10000,
                type='credit'
            )