from django.urls import path
from .views import (
    wallet_connect, wallet_profile, wallet_donations,
    wallet_users_list, wallet_user_detail, wallet_user_activities,
    wallet_role,
)

urlpatterns = [
    path('users/', wallet_users_list, name='wallet-users-list'),
    path('users/connect/', wallet_connect, name='wallet-connect'),
    path('users/<int:pk>/', wallet_user_detail, name='wallet-user-detail'),
    path('users/<int:pk>/activities/', wallet_user_activities, name='wallet-user-activities'),
    path('users/<str:wallet_address>/role/', wallet_role, name='wallet-role'),
    path('users/<str:wallet_address>/profile/', wallet_profile, name='wallet-profile'),
    path('users/<str:wallet_address>/donations/', wallet_donations, name='wallet-donations'),
]
