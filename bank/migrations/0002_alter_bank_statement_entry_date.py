# Generated by Django 4.2.17 on 2025-05-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_statement',
            name='entry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
