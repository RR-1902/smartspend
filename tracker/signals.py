from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Achievement, UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = UserProfile.objects.create(user=instance)
    Achievement.objects.bulk_create([
        Achievement(profile=profile, title='First Budget', description='Created your first monthly money plan.', icon='target'),
        Achievement(profile=profile, title='Streak Starter', description='Tracked expenses for a full week.', icon='flame'),
        Achievement(profile=profile, title='Smart Saver', description='Reached 40% of the savings goal.', icon='sparkles'),
    ])
