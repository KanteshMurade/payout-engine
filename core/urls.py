from django.urls import path
from .views import create_payout, payout_list, add_credit

urlpatterns = [
    path('payouts', create_payout),
    path('payouts/list/', payout_list),
    path('credit', add_credit),
]