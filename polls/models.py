from django.db import models
from django.contrib.auth.models import User

DAY_OF_WEEK_CHOICES = (
    (0, '월요일'),
    (1, '화요일'),
    (2, '수요일'),
    (3, '목요일'),
    (4, '금요일'),
    (5, '토요일'),
    (6, '일요일'),
)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES)
    completed = models.BooleanField(default=False)
    reflection = models.TextField(blank=True)
    image = models.ImageField(upload_to='goal_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)