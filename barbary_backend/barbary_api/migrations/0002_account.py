# Generated by Django 3.2 on 2022-02-11 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('barbary_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to='images')),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('home_number', models.CharField(blank=True, max_length=11, null=True)),
                ('expertise_area', models.CharField(blank=True, max_length=256, null=True)),
                ('terminal_type', models.CharField(blank=True, choices=[('d', 'Dedicated terminal'), ('p', 'Publicly owned public terminal'), ('o', 'Out of the terminal'), ('s', 'special owned public terminal')], max_length=1, null=True)),
                ('Cargo_pickup_license', models.BooleanField(blank=True, default=False, null=True)),
                ('International_license', models.BooleanField(blank=True, default=False, null=True)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
                ('id_card', models.FileField(blank=True, null=True, upload_to='images')),
                ('license_image', models.FileField(blank=True, null=True, upload_to='images')),
                ('isAuthenticated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]