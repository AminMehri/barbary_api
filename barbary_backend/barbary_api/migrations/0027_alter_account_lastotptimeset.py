# Generated by Django 3.2 on 2022-02-17 17:16

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0026_alter_account_lastotptimeset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='lastOtpTimeSet',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
