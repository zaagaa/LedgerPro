from django.db import models
from django.conf import settings
from company.models import Company
from django.utils import timezone
import uuid

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None

def current_time():
    return timezone.now().time()



class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    staff_name = models.CharField(max_length=50)
    join_date = models.DateField(default=None, null=True, blank=True)
    exit_date = models.DateField(default=None, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.BigIntegerField(default=None, null=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    salary = models.FloatField(default=None, null=True)
    dob = models.DateField(null=True, blank=True)
    discontinued = models.IntegerField(default=0, null=True, blank=True)
    biometric_code = models.CharField(max_length=50, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    # New fields
    epf_number = models.CharField(max_length=50, null=True, blank=True)
    epf_salary = models.FloatField(default=None, null=True, blank=True)
    esi_number = models.CharField(max_length=50, null=True, blank=True)
    aadhar_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.staff_name


# in models.py
class StaffLeave(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WAITING', 'Waiting'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('FULL', 'Full Day'),
        ('HALF_MORNING', 'Half Day - Morning'),
        ('HALF_AFTERNOON', 'Half Day - Afternoon'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leaves', db_index=True)
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='FULL')  #  ADD THIS
    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    class Meta:
        db_table = 'staff_leave'
        ordering = ['-leave_date']
        unique_together = ('staff', 'leave_date')  # Optional: prevent duplicates

    def __str__(self):
        return f"{self.staff.staff_name} - {self.leave_date} - {self.status}"



class Attendance_Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, db_index=True)
    date = models.DateField(default=None, null=True, blank=True)
    staff= models.ForeignKey('Staff', on_delete=models.CASCADE, null=True, db_index=True)
    in_time=models.IntegerField(default=None, null=True, blank=True)
    out_time = models.IntegerField(default=None, null=True, blank=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)

    class Meta:
        unique_together = ('company', 'date', 'staff')



class Holiday(models.Model):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.reason}"

class Staff_Credit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date = models.DateField(null=False)
    time = models.TimeField(default=current_time)
    notes = models.CharField(max_length=100, null=True, blank=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, null=False, db_index=True)
    amount = models.FloatField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, db_index=True)
    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)



###AFTER IMPORT RUN THIS CODE ON PGADMIN
# SELECT setval(
#   pg_get_serial_sequence('staff_staff_credit', 'id'),
#   COALESCE((SELECT MAX(id) FROM staff_staff_credit), 1)
# );
