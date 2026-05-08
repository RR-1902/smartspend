import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Entertainment', 'Entertainment'), ('Shopping', 'Shopping'), ('Bills', 'Bills'), ('Health', 'Health'), ('Education', 'Education'), ('Savings', 'Savings'), ('Other', 'Other')], default='Other', max_length=40)),
                ('date', models.DateField(default=django.utils.timezone.localdate)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_color', models.CharField(default='#8CC8FF', max_length=20)),
                ('monthly_budget', models.DecimalField(decimal_places=2, default=25000, max_digits=10)),
                ('savings_goal', models.DecimalField(decimal_places=2, default=10000, max_digits=10)),
                ('current_savings', models.DecimalField(decimal_places=2, default=4500, max_digits=10)),
                ('xp_points', models.PositiveIntegerField(default=1240)),
                ('saving_streak', models.PositiveIntegerField(default=8)),
                ('level', models.PositiveIntegerField(default=4)),
                ('dark_mode', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=180)),
                ('icon', models.CharField(default='star', max_length=40)),
                ('unlocked', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='tracker.userprofile')),
            ],
        ),
    ]
