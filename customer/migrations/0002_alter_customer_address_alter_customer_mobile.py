# Generated by Django 4.2.17 on 2025-04-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
