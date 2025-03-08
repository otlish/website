from django.db import models
from django.conf import settings  # Import your custom user model reference

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Custom user model
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, default="M")
    image=models.CharField(max_length=255)
    

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"