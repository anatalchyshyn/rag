import os
import boto3
from botocore.exceptions import NoCredentialError

OVH_BUCKET = ""
OVH_REGION = ""
OVH_ACCESS_KEY = ""
OVH_SECRET_KEY = ""

VECTOR_DB = "./chroma_db"

s3_client = boto3.client(
        "s3",
        region_name = OVH_REGION,
        aws_access_key_id = OVH_ACCESS_KEY,
        aws_secret_access_key = OVH_SECRET_KEY,
        )

def bucket_exists(s3_client):
    try:
        s3_client.head_object(Bucket=OVH_BUCKET)
        print("Successfully connected.")
        return True
    except NoCredentialsError:
        print("No credentials error.")
        return False
    except:
        print("Other error.")
        return False

def create_bucket(s3_client, bucket_name: str):
    """OVH bucket creation process"""
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket created")
        return True
    except:
        print("Cannot create a bucket")
        return False
