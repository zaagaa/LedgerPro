# Generated by Django 4.2.17 on 2025-05-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_rename_credit_staff_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
