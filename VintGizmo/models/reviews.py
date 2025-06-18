from django.db import models
from django.utils import timezone
from django.conf import settings
from .variation import Variation
from .models import CustomUser


class RatingReview(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # Ratings from 1 to 5

    product = models.ForeignKey('Variation', on_delete=models.CASCADE, related_name='ratings_reviews')
    
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')  # Ensure a user can only leave one review per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"
