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

s3 = boto3.client('s3')
assert bucket_name in [b["Name"] for b in s3.list_buckets()['Buckets']],\
        f"`{bucket_name}` not in list of available buckets"

def is_key_in_bucket(key):
    try:
        res = s3.head_object(Bucket=bucket_name, Key=key)
        assert res["ResponseMetadata"]["HTTPStatusCode"] == 200, "if request didn't error out with 404, 200 should have been received"
    except botocore.exceptions.ClientError as err:
        assert err.response["Error"]["Code"] == "404", err.response
        return False
    else:
        return True

for f in files:
    print(f"Uploading {f} to {bucket_name}...".ljust(80, "."), end='')
    filename = os.path.basename(f)
    if is_key_in_bucket(filename) and not args.force:
        print("Skipped.")
    else:
        s3.upload_file(f, bucket_name, os.path.basename(f))
        print("Done.")
