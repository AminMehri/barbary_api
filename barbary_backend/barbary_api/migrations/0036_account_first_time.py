# Generated by Django 3.2 on 2022-02-17 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0035_alter_account_lastotptimeset'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_time',
            field=models.BooleanField(default=True),
        ),
    ]
