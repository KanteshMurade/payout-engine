from django.urls import path
from .views import *

urlpatterns = [
    path('payouts', create_payout),
    path('list', payout_list),
    path('balance', balance),
    path('credit', add_credit),
]