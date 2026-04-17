from django.urls import path
from .views import vault_list_create, vault_detail, vault_by_donation_id, vault_record_cycle

urlpatterns = [
    path('vaults/', vault_list_create, name='vault-list-create'),
    path('vaults/<int:pk>/', vault_detail, name='vault-detail'),
    path('vaults/<int:pk>/cycles/', vault_record_cycle, name='vault-record-cycle'),
    path('vaults/by-donation/<str:donation_id_ref>/', vault_by_donation_id, name='vault-by-donation'),
]
