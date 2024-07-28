from django.db import models
from django.contrib.auth.models import User

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='CREATED')

    def __str__(self):
        return f"{self.user.username} - {self.coin} - {self.target_price}"
