from django.urls import path
from .views import create_payout, payout_list, merchant_detail

urlpatterns = [
    path('payouts', create_payout),
    path('payouts/list/', payout_list),
    path('merchant/<int:merchant_id>/', merchant_detail),
]