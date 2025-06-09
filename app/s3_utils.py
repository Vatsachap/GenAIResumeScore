import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

def upload_to_s3(file_obj, filename):
    s3.upload_fileobj(file_obj, BUCKET_NAME, filename)

def list_resumes_in_s3():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith(".pdf")]

def download_resume_from_s3(key):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return obj['Body'].read()
