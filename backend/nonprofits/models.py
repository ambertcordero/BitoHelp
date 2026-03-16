from django.db import models
class Nonprofit(models.Model):
  
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('health', 'Health'),
        ('environment', 'Environment'),
        ('poverty', 'Poverty Alleviation'),
        ('animal_welfare', 'Animal Welfare'),
        ('arts_culture', 'Arts & Culture'),
        ('human_rights', 'Human Rights'),
        ('disaster_relief', 'Disaster Relief'),
        ('other', 'Other'),
    ]

  
    name = models.CharField(max_length=255)
    description = models.TextField()
    bch_address = models.CharField(max_length=255, unique=True, db_index=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    logo_url = models.URLField(blank=True)

  
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        donations = Donation.objects.filter(nonprofit=self)
        self.donation_count = donations.count()
        self.total_donations = donations.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        self.save() 
