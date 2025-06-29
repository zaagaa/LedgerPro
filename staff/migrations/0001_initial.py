# Generated by Django 4.2.22 on 2025-06-17 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import staff.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('staff_name', models.CharField(max_length=50)),
                ('join_date', models.DateField(blank=True, default=None, null=True)),
                ('exit_date', models.DateField(blank=True, default=None, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('mobile', models.BigIntegerField(default=None, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('salary', models.FloatField(default=None, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('discontinued', models.IntegerField(blank=True, default=0, null=True)),
                ('biometric_code', models.CharField(blank=True, max_length=50, null=True)),
                ('sync_offline', models.BigIntegerField(blank=True, default=staff.models.initial_sync_offline, null=True)),
                ('sync_online', models.BigIntegerField(blank=True, default=staff.models.initial_sync_online, null=True)),
                ('epf_number', models.CharField(blank=True, max_length=50, null=True)),
                ('epf_salary', models.FloatField(blank=True, default=None, null=True)),
                ('esi_number', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhar_number', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='Staff_Credit',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField(default=staff.models.current_time)),
                ('notes', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.FloatField()),
                ('sync_offline', models.BigIntegerField(blank=True, default=staff.models.initial_sync_offline, null=True)),
                ('sync_online', models.BigIntegerField(blank=True, default=staff.models.initial_sync_online, null=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('reason', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='StaffLeave',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_date', models.DateField()),
                ('leave_type', models.CharField(choices=[('FULL', 'Full Day'), ('HALF_MORNING', 'Half Day - Morning'), ('HALF_AFTERNOON', 'Half Day - Afternoon')], default='FULL', max_length=20)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('WAITING', 'Waiting')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sync_offline', models.BigIntegerField(blank=True, default=staff.models.initial_sync_offline, null=True)),
                ('sync_online', models.BigIntegerField(blank=True, default=staff.models.initial_sync_online, null=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='staff.staff')),
            ],
            options={
                'db_table': 'staff_leave',
                'ordering': ['-leave_date'],
                'unique_together': {('staff', 'leave_date')},
            },
        ),
        migrations.CreateModel(
            name='Attendance_Entry',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('date', models.DateField(blank=True, default=None, null=True)),
                ('in_time', models.IntegerField(blank=True, default=None, null=True)),
                ('out_time', models.IntegerField(blank=True, default=None, null=True)),
                ('sync_offline', models.BigIntegerField(blank=True, default=staff.models.initial_sync_offline, null=True)),
                ('sync_online', models.BigIntegerField(blank=True, default=staff.models.initial_sync_online, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
            options={
                'unique_together': {('company', 'date', 'staff')},
            },
        ),
    ]
