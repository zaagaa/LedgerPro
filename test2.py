import os
import sys
import django
from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Q

# ===============================
# DJANGO SETUP (FIRST!)
# ===============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

# ===============================
# IMPORTS AFTER SETUP
# ===============================


from zk import ZK
from staff.models import Attendance_Entry, Staff, Company


# =========================
# DEVICE SETTINGS
# =========================

DEVICE_IP = "192.168.1.201"

zk = ZK(
    DEVICE_IP,
    port=4370,
    timeout=5,
    password=0
)





try:

    conn = zk.connect()

    print("Connected:", conn)

    logs = conn.get_attendance()

    today = date.today()

    for log in logs:

        punch_datetime = log.timestamp


        # only today
        if punch_datetime.date() != today:
            continue


        print(
            log.user_id,
            punch_datetime
        )


        # find staff

        try:

            staff = Staff.objects.get(
                biometric_code=log.user_id
            )

        except Staff.DoesNotExist:

            print(
                "Skip user:",
                log.user_id
            )

            continue



        # ============================
        # CONVERT TO UNIX TIMESTAMP
        # ============================

        punch_timestamp = int(
            punch_datetime.timestamp()
        )


        entry, created = Attendance_Entry.objects.get_or_create(

            company=staff.company,

            staff=staff,

            date=today,


            defaults={

                "in_time": punch_timestamp,

                "out_time": punch_timestamp

            }

        )



        if created:

            print(
                "Created IN:",
                staff.staff_name,
                punch_timestamp
            )


        else:

            # latest punch becomes OUT

            if punch_timestamp > entry.out_time:

                entry.out_time = punch_timestamp

                entry.save()


                print(
                    "Updated OUT:",
                    staff.staff_name,
                    punch_timestamp
                )



    conn.disconnect()

    print("Sync Completed")


except Exception as e:

    print(
        "Error:",
        e
    )