# Generated by Django 4.2.17 on 2025-03-07 06:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tax_code', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('inventory_name', models.CharField(max_length=200)),
                ('shortcode', models.CharField(blank=True, max_length=10, null=True)),
                ('unit_enabled', models.IntegerField(default=0)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('tax_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tax_code.tax_code')),
            ],
            options={
                'unique_together': {('company', 'inventory_name', 'tax_code')},
            },
        ),
    ]
