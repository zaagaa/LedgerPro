# Generated by Django 4.2.20 on 2025-04-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_country_alter_company_tax_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='mobile',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
