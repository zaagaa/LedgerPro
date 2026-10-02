from BusinessApp import settings
from setting.models import Image, Setting
import os
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


def upload_into_s3(local_path, s3_key):
    image_name = os.path.basename(s3_key)
    directory_name = os.path.dirname(s3_key).replace("\\", "/")

    # ✅ Check or create Image entry
    image_log, created = Image.objects.get_or_create(
        image_name=image_name,
        directory_name=directory_name,
        defaults={"uploaded_to_s3": False}
    )

    # Skip if already marked as uploaded
    if image_log.uploaded_to_s3:
        print(f"✅ Already logged as uploaded: {s3_key}")
        return

    # Load AWS config
    def get(key):
        setting = Setting.objects.filter(company__isnull=True, setting=key).first()
        return setting.value if setting else ""

    aws_access_key = get('AWS_ACCESS_KEY_ID')
    aws_secret_key = get('AWS_SECRET_ACCESS_KEY')
    bucket = get('AWS_STORAGE_BUCKET_NAME')
    region = get('AWS_S3_REGION_NAME') or 'ap-south-1'

    if not all([aws_access_key, aws_secret_key, bucket]):
        print("⚠️ Missing AWS config, skipping upload.")
        return

    try:
        s3 = boto3.client('s3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        try:
            s3.head_object(Bucket=bucket, Key=s3_key)
            print("⏩ Already exists in S3:", s3_key)
            image_log.uploaded_to_s3 = True

        except ClientError:
            s3.upload_file(local_path, bucket, s3_key)
            print("✅ Uploaded to S3:", s3_key)
            image_log.uploaded_to_s3 = True

    except EndpointConnectionError:
        print("❌ No internet. Could not connect.")
    except Exception as e:
        print(f"❌ Upload failed for {s3_key}: {e}")

    image_log.save()

def retry_failed_s3_uploads():
    failed_images = Image.objects.filter(uploaded_to_s3=False)
    print(f"🔁 Retrying {failed_images.count()} failed uploads...")

    for img in failed_images:
        local_path = os.path.join(settings.MEDIA_ROOT, img.directory_name, img.image_name)
        s3_key = os.path.join(img.directory_name, img.image_name).replace("\\", "/")

        if os.path.exists(local_path):
            upload_into_s3(local_path, s3_key)
        else:
            print(f"❌ Missing local file: {s3_key}")

def delete_from_s3(s3_key):
    def get(key):
        setting = Setting.objects.filter(company__isnull=True, setting=key).first()
        return setting.value if setting else ""

    aws_access_key = get('AWS_ACCESS_KEY_ID')
    aws_secret_key = get('AWS_SECRET_ACCESS_KEY')
    bucket = get('AWS_STORAGE_BUCKET_NAME')
    region = get('AWS_S3_REGION_NAME') or 'ap-south-1'

    if not all([aws_access_key, aws_secret_key, bucket]):
        print("⚠️ Missing AWS config. Skipping S3 deletion.")
        return False

    try:
        s3 = boto3.client('s3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        s3.delete_object(Bucket=bucket, Key=s3_key)
        print(f"🗑️ Deleted from S3: {s3_key}")
        return True
    except EndpointConnectionError:
        print("❌ No internet. Could not delete from S3.")
    except ClientError as e:
        print(f"❌ S3 deletion failed: {e}")
    return False


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

