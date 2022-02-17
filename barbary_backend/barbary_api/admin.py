from django.contrib import admin
from .models import Bar, Notification, Account


class BarAdmin(admin.ModelAdmin):
    list_display = ['beginning', 'destination', 'owner_bar', 'date', 'driver', 'isSpecial', 'isTopShow']


admin.site.register(Bar, BarAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Notification, NotificationAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'isAuthenticated', 'name', 'position']


admin.site.register(Account, AccountAdmin)
