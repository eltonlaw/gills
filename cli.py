#!/usr/bin/env python3
import os
import argparse
import boto3
from datasets import aws_utils

def upload(bucket, files, force=False):
    s3 = boto3.client('s3')
    aws_utils.upload(s3, bucket, files, force=force)

if __name__ == "__main__":
    # Arg parsing
    parser = argparse.ArgumentParser(description="Uploads file to public S3")
    parser.add_argument('cmd', choices=["upload"])
    parser.add_argument('files', nargs='*')
    parser.add_argument('-b', '--bucket', default="public-data-d0nkrs")
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args()

    if args.cmd == "upload":
        print(f"Uploading: {args.bucket} {args.files} {args.force}")
        upload(args.bucket, args.files, force=args.force)
