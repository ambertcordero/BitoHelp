from django.db import models


class Vault(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FUNDED = 'funded', 'Funded'
        WITHDRAWING = 'withdrawing', 'Withdrawing'
        DRAINED = 'drained', 'Drained'
        COMPLETED = 'completed', 'Completed'
        RECLAIMED = 'reclaimed', 'Reclaimed'

    donation_id_ref = models.CharField(max_length=128, unique=True, db_index=True,
                                       help_text='Frontend-generated donationId')
    donation = models.ForeignKey('donations.Donation', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='vaults')
    vault_address = models.CharField(max_length=255, db_index=True)
    recipient_address = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255, blank=True,
                                      help_text='Nonprofit organization name')
    funder_address = models.CharField(max_length=255)
    withdrawal_satoshis = models.BigIntegerField()
    deposit_satoshis = models.BigIntegerField(default=0)
    interval_blocks = models.PositiveIntegerField()
    interval_label = models.CharField(max_length=50, blank=True)
    contract_params = models.JSONField(default=dict, help_text='recipientHash, funderHash')
    payout_mode = models.CharField(max_length=20, default='smart')
    coin = models.CharField(max_length=20, default='BCH')
    network = models.CharField(max_length=20, default='chipnet')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FUNDED)
    cycles_completed = models.PositiveIntegerField(default=0)
    total_cycles = models.PositiveIntegerField(default=1)
    donor_email = models.EmailField(blank=True)
    donor_name = models.CharField(max_length=255, blank=True)
    cause = models.CharField(max_length=255, blank=True)
    funding_txid = models.CharField(max_length=64, blank=True)
    last_withdraw_txid = models.CharField(max_length=64, blank=True)
    last_withdraw_at = models.DateTimeField(null=True, blank=True)
    reclaim_txid = models.CharField(max_length=64, blank=True)
    reclaimed_at = models.DateTimeField(null=True, blank=True)
    reclaimed_amount = models.BigIntegerField(default=0)
    reclaim_warning_sent_at = models.DateTimeField(null=True, blank=True)
    wallet_user = models.ForeignKey('users.WalletUser', on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='vaults')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        donor = self.donor_name or self.funder_address[:12] + '…'
        recipient = self.recipient_name or self.recipient_address[:12] + '…'
        return f'Vault: {donor} → {recipient} ({self.status})'


class WithdrawalCycle(models.Model):
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE, related_name='withdrawal_cycles')
    cycle_number = models.PositiveIntegerField()
    txid = models.CharField(max_length=64)
    amount_satoshis = models.BigIntegerField()
    drained = models.BooleanField(default=False)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['vault', 'cycle_number']
        ordering = ['cycle_number']

    def __str__(self):
        return f'Cycle {self.cycle_number} — {self.txid[:12]}…'
