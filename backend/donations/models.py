from django.db import models

class Donation(models.Model):
    txid = models.CharField(max_length=255, unique=True, db_index=True)
    recipient = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=16, decimal_places=8)
    coin = models.CharField(max_length=20, default='BCH')
    cause = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    donor_name = models.CharField(max_length=255, blank=True)
    donor_email = models.EmailField(blank=True)
    donor_contact = models.CharField(max_length=50, blank=True)
    explorer_url = models.URLField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    nonprofit = models.ForeignKey('nonprofits.Nonprofit', on_delete=models.CASCADE, related_name='donations', null=True, blank=True)
    contract = models.CharField(max_length=255, blank=True)
    interval = models.CharField(max_length=50, blank=True)
    payout_mode = models.CharField(max_length=20, default='smart', blank=True,
                                   help_text='smart = auto-withdraw, inbox_approval = email approval required')
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['txid']),
        ]
    
    def __str__(self):
        nonprofit_name = self.nonprofit.name if self.nonprofit else self.cause
        return f"{self.donor_name or 'Anonymous'} - {self.amount} {self.coin} to {nonprofit_name}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update nonprofit stats after saving - disabled to prevent database locks
        # TODO: Move to async task or post_save signal
        # if self.nonprofit:
        #     self.nonprofit.update_donation_stats()