from django.conf import settings
from django.db import models


# Create your models here.
class Match(models.Model):
    """The `Match` model represents a found match based on the keywords chosen by the user."""

    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(max_length=350)
    coupon = models.CharField(max_length=128, blank=True, null=True)
    date_match_found = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True)
    # is_cheap -> compare it with found zoom prices
    # zoom_best_price -> decimal price containing zoom best prices

    def __str__(self):
        return self.name + " - " + self.price

