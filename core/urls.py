from django.contrib import admin
from django.urls import path
from core.views import create_payout, payout_list, get_balance_api

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/payouts', create_payout),
    path('api/v1/payouts/list', payout_list),
    path('api/v1/balance/<int:merchant_id>', get_balance_api),
]