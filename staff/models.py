from django.db import models

from company.models import Company
from django.utils import timezone


class Staff(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
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

    # New fields
    epf_number = models.CharField(max_length=50, null=True, blank=True)
    esi_number = models.CharField(max_length=50, null=True, blank=True)
    aadhar_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.staff_name


class Attendance_Entry(models.Model):
    sync = models.DateTimeField(default=timezone.now, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=None, null=True, blank=True)
    staff= models.ForeignKey('Staff', on_delete=models.CASCADE, null=True)
    in_time=models.IntegerField(default=None, null=True, blank=True)
    out_time = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ('company', 'date', 'staff')

def current_time():
    return timezone.now().time()

from django.conf import settings

class Staff_Credit(models.Model):
    date = models.DateField(null=False)
    time = models.TimeField(default=current_time)
    notes = models.CharField(max_length=100, null=True, blank=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, null=False)
    amount = models.FloatField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)



###AFTER IMPORT RUN THIS CODE ON PGADMIN
# SELECT setval(
#   pg_get_serial_sequence('staff_staff_credit', 'id'),
#   COALESCE((SELECT MAX(id) FROM staff_staff_credit), 1)
# );