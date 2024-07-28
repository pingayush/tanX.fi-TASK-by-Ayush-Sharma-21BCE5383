from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        # Add more cryptocurrencies as needed
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('triggered', 'Triggered'),
        ('deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    target_price = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    def __str__(self):
        return f'{self.user.username} - {self.crypto} - {self.target_price}'
