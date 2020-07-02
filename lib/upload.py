#!/usr/bin/env python3
import os
import argparse
import boto3
import botocore

# Arg parsing
parser = argparse.ArgumentParser(description="Uploads file to public S3")
parser.add_argument('files', nargs='+')
parser.add_argument('-b', '--bucket-name', default="public-data-d0nkrs")
parser.add_argument('-f', '--force', action='store_true')
args = parser.parse_args()

bucket_name = args.bucket_name
files = args.files

s3  = boto3.resource('s3')
s3_client = s3.meta.client
assert bucket_name in [b["Name"] for b in s3_client.list_buckets()['Buckets']],\
        f"`{bucket_name}` not in list of available buckets"

def is_key_in_bucket(key):
    try:
        s3.Object(bucket_name, key).load()
    except botocore.exceptions.ClientError:
        return False
    else:
        return True

for f in files:
    print(f"Uploading {f} to {bucket_name}...".ljust(80, "."), end='')
    if is_key_in_bucket and not args.force:
        print("Skipped.")
    else:
        s3.upload_file(f, bucket_name, os.path.basename(f))
        print("Done.")
