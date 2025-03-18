import os
import boto3
from botocore.exceptions import NoCredentialError, PartialCredentialsError
from dotenv import load_dotenv

load_dotenv()

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

def get_file_from_bucket(s3_client,
                         bucket_name: str,
                         object_key: str,
                         download_path: str):
    """Download a file from an OVH Object Storage bucket using Boto3."""
    try:
        s3_client.download_file(bucket_name, object_key, download_path)
        print(f"File downloaded successfully: {download_path}")
        return True

    except NoCredentialsError:
        print("Error: Credentials not provided or invalid.")

    except PartialCredentialsError:
        print("Error: Incomplete credentials provided.")

    except Exception as e:
        print(f"Error downloading file: {e}")

    return False


def upload_file_to_bucket(file_path, bucket_name, object_key):
    """
    Upload a file to an OVH Object Storage bucket using Boto3.
    """
    try:

        s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded successfully: {file_path}")
        return True

    except NoCredentialsError:
        print("Error: Credentials not provided or invalid.")
    except PartialCredentialsError:
        print("Error: Incomplete credentials provided.")
    except Exception as e:
        print(f"Error uploading file: {e}")

    return False
