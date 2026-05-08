from django.contrib import admin

from .models import Achievement, Expense, UserProfile

admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(Achievement)
