from django.urls import path
from .views import create_payout, payout_list, get_balance_view, add_credit

urlpatterns = [
    path('payouts', create_payout),
    path('payouts/list/', payout_list),
    path('balance/<int:merchant_id>', get_balance_view),
    path('credit', add_credit),
]
