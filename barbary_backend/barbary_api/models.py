import jdatetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django_jalali.db import models as jmodels


class Account(models.Model):
    STATUS_CHOICES = (
        ('d', 'Dedicated terminal'),
        ('p', 'Publicly owned public terminal'),
        ('o', 'Out of the terminal'),
        ('s', 'special owned public terminal'),
    )
    POSITION_CHOICES = (
        ('driver', 'driver'),
        ('manager', 'manager'),
        ('company', 'company'),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, null=True, blank=True)
    position = models.CharField(max_length=7, choices=POSITION_CHOICES, null=True, blank=True)
    thumbnail = models.FileField(upload_to="images", null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    home_number = models.CharField(max_length=11, null=True, blank=True)
    expertise_area = models.CharField(max_length=256, null=True, blank=True)
    terminal_type = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    id_card = models.FileField(upload_to="images", null=True, blank=True)
    license_image = models.FileField(upload_to="images", null=True, blank=True)
    isAuthenticated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Bar(models.Model):

    beginning = models.CharField(max_length=256)
    destination = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    date = jmodels.jDateField()
    weight = models.FloatField()
    product_type = models.CharField(max_length=256)
    # product_packaging = models.CharField(max_length=256)
    fleet_type = models.CharField(max_length=256)
    owner_bar = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=512, blank=True, default='')
    phone_number = models.CharField(max_length=11)
    isFinish = models.BooleanField(default=False)
    driver = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL, related_name="driver")
    isSpecial = models.BooleanField(default=False)
    isTopShow = models.BooleanField(default=False)

    def __str__(self):
        return self.beginning + ' ---> ' + self.destination


class Notification(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
