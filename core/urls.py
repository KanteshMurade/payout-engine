from django.urls import path
<<<<<<< HEAD
from .views import create_payout, payout_list, add_credit
=======
from .views import create_payout, payout_list, merchant_detail, add_balance
>>>>>>> 189d1be0b906f5b486987d26560ad3d988ef0f42

urlpatterns = [
    path('payouts', create_payout),
    path('payouts/list/', payout_list),
<<<<<<< HEAD
    path('credit', add_credit),
]
=======
    path('merchant/<int:merchant_id>/', merchant_detail),
    path('add-balance', add_balance),
]
>>>>>>> 189d1be0b906f5b486987d26560ad3d988ef0f42
