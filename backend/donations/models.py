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
    explorer_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
    
    def __str__(self):
        return f"{self.donor_name or 'Anonymous'} - {self.amount} {self.coin} to {self.cause}"
