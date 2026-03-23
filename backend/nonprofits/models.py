from django.db import models

class Nonprofit(models.Model):
    CATEGORY_CHOICES = [
        ('animals', 'Animals'),
        ('poverty', 'Poverty Alleviation'),
        ('children_youth', 'Children & Youth'),
        ('housing_humanitarian', 'Housing & Community Humanitarian Aid'),
        ('environment', 'Environment & Conservation'),
    ]

    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField()
    bch_address = models.CharField(max_length=255, unique=True, db_index=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    logo_url = models.URLField(blank=True)

    # Status
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Statistics
    total_donations = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    donation_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Nonprofit Organization'
        verbose_name_plural = 'Nonprofit Organizations'

    def __str__(self):
        return self.name

    def update_donation_stats(self):
        from donations.models import Donation
        from django.db.models import Sum, Count
        
        stats = Donation.objects.filter(nonprofit=self).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
   
        Nonprofit.objects.filter(pk=self.pk).update(
            donation_count=stats['count'] or 0,
            total_donations=stats['total'] or 0
        ) 