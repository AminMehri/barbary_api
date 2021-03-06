# Generated by Django 3.2 on 2022-02-17 01:31

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('barbary_api', '0017_alter_notification_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='color',
            field=models.CharField(choices=[('warning', 'warning'), ('success', 'success'), ('danger', 'danger'), ('info', 'info')], default='warning', max_length=8),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
