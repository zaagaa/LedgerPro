# Generated by Django 4.2.17 on 2025-04-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='mobile',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]
