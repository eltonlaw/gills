#!/usr/bin/env python3
import os
import sys
import boto3
import botocore
from botocore.config import Config

def is_key_in_bucket(s3, bucket, key):
    try:
        res = s3.head_object(Bucket=bucket_name, Key=key)
        assert res["ResponseMetadata"]["HTTPStatusCode"] == 200, "if request didn't error out with 404, 200 should have been received"
    except botocore.exceptions.ClientError as err:
        assert err.response["Error"]["Code"] == "404", err.response
        return False
    else:
        return True

def init_s3():
    return boto3.client("s3", config=Config(signature_version=botocore.UNSIGNED))

def upload(s3, bucket, files, force=False):
    try:
        assert bucket in [b["Name"] for b in s3.list_buckets()['Buckets']],\
                f"`{bucket}` not in list of available buckets"
    except botocore.exceptions.NoCredentialsError as err:
        print("E:", err)
        sys.exit(0)
    for f in files:
        print(f"Uploading {f} to {bucket_name}...".ljust(80, "."), end='')
        # Use filename as key
        filename = os.path.basename(f)
        if is_key_in_bucket(s3, bucket, filename) and not force:
            print("Skipped.")
        else:
            s3.upload_file(f, bucket_name, os.path.basename(f))
            print("Done.")

def download(s3, bucket, key, output_dir):
    fp = os.path.join(output_dir, key)

    if os.path.exists(fp):
        print(f"{key} skipped - already exists on filesystem")
    else:
        obj_metadata = s3.head_object(Bucket=bucket, Key=key)
        s3.download_file(bucket, key, fp)
        print(f"{key} downloaded - last modified={obj_metadata['LastModified']}")

def download_all(s3, bucket, keys, output_dir):
    for key in keys:
        download(s3, bucket, key, output_dir)
