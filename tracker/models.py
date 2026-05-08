from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone

CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Travel', 'Travel'),
    ('Entertainment', 'Entertainment'),
    ('Shopping', 'Shopping'),
    ('Bills', 'Bills'),
    ('Health', 'Health'),
    ('Education', 'Education'),
    ('Savings', 'Savings'),
    ('Other', 'Other'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar_color = models.CharField(max_length=20, default='#8CC8FF')
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=25000)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    current_savings = models.DecimalField(max_digits=10, decimal_places=2, default=4500)
    xp_points = models.PositiveIntegerField(default=1240)
    saving_streak = models.PositiveIntegerField(default=8)
    level = models.PositiveIntegerField(default=4)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def savings_progress(self):
        if not self.savings_goal:
            return 0
        return min(100, round((float(self.current_savings) / float(self.savings_goal)) * 100))


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField(default=timezone.localdate)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.amount}'


class Achievement(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=180)
    icon = models.CharField(max_length=40, default='star')
    unlocked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def monthly_total(user):
    today = timezone.localdate()
    return Expense.objects.filter(user=user, date__year=today.year, date__month=today.month).aggregate(
        total=Sum('amount')
    )['total'] or 0
