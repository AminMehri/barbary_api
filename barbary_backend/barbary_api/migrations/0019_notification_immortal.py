# Generated by Django 3.2 on 2022-02-17 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0018_auto_20220217_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='immortal',
            field=models.BooleanField(default=False),
        ),
    ]
