# Generated by Django 3.2 on 2022-02-17 17:10

from django.db import migrations, models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0021_account_lastotptimeset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='lastOtpTimeSet',
            field=models.DateTimeField(blank=True, default=jdatetime.datetime.now),
        ),
    ]