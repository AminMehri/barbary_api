# Generated by Django 3.2 on 2022-02-12 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0005_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
