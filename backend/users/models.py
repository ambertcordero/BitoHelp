from django.db import models


class WalletUser(models.Model):
    """
    Each unique wallet address is a user profile.
    BCH addresses are stored lowercase for case-insensitive matching.
    """
    wallet_address = models.CharField(max_length=255, unique=True, db_index=True)

    # Original fields (current/default value)
    display_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, default='')
    contact = models.CharField(max_length=50, blank=True, default='')

    # History fields (append-only lists of all values ever used)
    names_history = models.JSONField(default=list, blank=True,
        help_text='All display names used, first entry is default')
    emails_history = models.JSONField(default=list, blank=True,
        help_text='All emails used, first entry is default')
    contacts_history = models.JSONField(default=list, blank=True,
        help_text='All contact numbers used, first entry is default')

    avatar_url = models.URLField(blank=True)
    chain = models.CharField(max_length=50, blank=True, default='')
    namespace = models.CharField(max_length=20, blank=True, default='')
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    symbol = models.CharField(max_length=10, blank=True, default='')
    last_connected_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wallet User'
        verbose_name_plural = 'Wallet Users'

    def __str__(self):
        return self.display_name or self.wallet_address

    def save(self, *args, **kwargs):
        self.wallet_address = self.wallet_address.lower().strip()
        super().save(*args, **kwargs)
