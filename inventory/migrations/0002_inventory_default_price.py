# Generated by Django 4.2.17 on 2025-04-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='default_price',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
