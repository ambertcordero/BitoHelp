from django.urls import path
from . import views

urlpatterns = [
    path('payouts/approve/<str:token>/', views.gmail_approve, name='gmail-approve'),
    path('payouts/', views.list_approvals, name='payout-list'),
    path('payouts/request/', views.request_approval, name='payout-request'),
    path('payouts/<int:pk>/', views.approval_status, name='payout-status'),
    path('payouts/<int:pk>/audit/', views.approval_audit_log, name='payout-audit'),
    path('payouts/<int:pk>/execute/', views.report_execution, name='payout-execute'),
    path('payouts/<int:pk>/trigger/', views.trigger_approval, name='payout-trigger'),
]
