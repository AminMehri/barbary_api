# Generated by Django 3.2 on 2022-02-10 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning', models.CharField(max_length=256)),
                ('destination', models.CharField(max_length=256)),
                ('price', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('weight', models.FloatField()),
                ('product_Type', models.CharField(max_length=256)),
                ('product_packaging', models.CharField(max_length=256)),
                ('fleet_type', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=512)),
                ('phone_number', models.CharField(max_length=11)),
                ('isFinish', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to=settings.AUTH_USER_MODEL)),
                ('owner_bar', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
