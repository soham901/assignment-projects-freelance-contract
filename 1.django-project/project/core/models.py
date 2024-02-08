from django.db import models


class Stock(models.Model):
    base = models.CharField(max_length=10, default="BTC") # We can use choices here in future
    currency = models.CharField(max_length=10, default="USD") # We can use choices here in future
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base}-{self.currency} {self.amount}"
    
    class Meta:
        ordering = ["-created_at"]
