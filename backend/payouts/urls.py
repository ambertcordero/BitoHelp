from django.urls import path
from . import views

urlpatterns = [
    path('payouts/approve/<str:token>/', views.gmail_approve, name='gmail-approve'),
    path('payouts/missing-txids/', views.list_missing_txids, name='payout-missing-txids'),
    path('payouts/', views.list_approvals, name='payout-list'),
    path('payouts/request/', views.request_approval, name='payout-request'),
    path('payouts/record/', views.record_smart_withdrawal, name='payout-record'),
    path('payouts/reclaim-warning/', views.notify_reclaim_warning, name='payout-reclaim-warning'),
    path('payouts/<int:pk>/', views.approval_status, name='payout-status'),
    path('payouts/<int:pk>/audit/', views.approval_audit_log, name='payout-audit'),
    path('payouts/<int:pk>/execute/', views.report_execution, name='payout-execute'),
    path('payouts/execute-by-vault/', views.report_execution_by_vault, name='payout-execute-by-vault'),
    path('payouts/<int:pk>/trigger/', views.trigger_approval, name='payout-trigger'),
]
