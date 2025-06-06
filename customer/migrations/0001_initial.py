# Generated by Django 4.2.17 on 2025-03-07 06:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('customer_name', models.CharField(max_length=50)),
                ('tax_number', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('mobile', models.IntegerField(blank=True, default=None, null=True)),
                ('point', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
    ]
