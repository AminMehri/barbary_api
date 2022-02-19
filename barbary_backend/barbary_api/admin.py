from django.contrib import admin
from .models import Bar, Notification, Account


def make_authenticate(modeladmin, request, queryset):
    rows_updated = queryset.update(isAuthenticated=True)
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s stories were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as authenticate." % message_bit)
    make_authenticate.short_description = "Mark selected users as authenticate"


def make_not_authenticate(modeladmin, request, queryset):
    rows_updated = queryset.update(isAuthenticated=False)
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s stories were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as not authenticate." % message_bit)
    make_not_authenticate.short_description = "Mark selected users as not authenticate"




def make_see_notification(modeladmin, request, queryset):
    rows_updated = queryset.update(isSeeLastNotif=True)
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s stories were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as see notification." % message_bit)
    make_see_notification.short_description = "Mark selected users as see notification"


def make_dont_see_notification(modeladmin, request, queryset):
    rows_updated = queryset.update(isSeeLastNotif=False)
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s stories were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as dont see notification." % message_bit)
    make_dont_see_notification.short_description = "Mark selected users as dont see notification"



class BarAdmin(admin.ModelAdmin):
    list_display = ['beginning', 'destination', 'owner_bar', 'date', 'driver', 'isSpecial', 'isTopShow']


admin.site.register(Bar, BarAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'color', 'immortal']


admin.site.register(Notification, NotificationAdmin)


class AccountAdmin(admin.ModelAdmin):

    list_display = ['user', 'phone_number', 'isAuthenticated', 'name', 'position', 'isSeeLastNotif', 'first_time']
    actions = [make_authenticate, make_not_authenticate, make_see_notification, make_dont_see_notification]


admin.site.register(Account, AccountAdmin)
