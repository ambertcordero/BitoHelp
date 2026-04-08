from django.db import models


class WalletUser(models.Model):
    """
    Each unique wallet address is a user profile.
    BCH addresses are stored lowercase for case-insensitive matching.
    """
    wallet_address = models.CharField(max_length=255, unique=True, db_index=True)
    display_name = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(blank=True)
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
