import os
import django
from django.conf import settings



# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()
from setting.upload_into_s3 import upload_into_s3, delete_from_s3
import boto3
from setting.models import Setting, Image

def cleanup_deleted_images_from_s3():
    images = Image.objects.filter(deleted=True)
    print(f"🧹 Found {images.count()} images marked as deleted...")

    for img in images:
        s3_key = os.path.join(img.directory_name, img.image_name).replace("\\", "/")

        if delete_from_s3(s3_key):
            print(f"✅ Deleted from S3: {s3_key}")
            img.delete()
        else:
            print(f"❌ Failed to delete from S3: {s3_key}")

cleanup_deleted_images_from_s3()


