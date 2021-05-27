import boto3
import argparse
import os
import sys


BASE_URL = "https://s3.amazonaws.com/"


def upload(**kwargs):
    AWS_ACCESS_KEY_ID = kwargs.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = kwargs.get('AWS_SECRET_ACCESS_KEY')
    FILENAME = kwargs.get('FILENAME')
    S3_BUCKET_NAME = kwargs.get('S3_BUCKET_NAME')
    S3_PATH = kwargs.get('S3_PATH')
    s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # filename = "filename"
    with open(FILENAME, "rb") as ifile:
        s3.Object(S3_BUCKET_NAME, S3_PATH +
                  FILENAME).put(Body=ifile)

    file_size = s3.Bucket(S3_BUCKET_NAME).Object(
        S3_PATH + FILENAME).content_length
    file_size = round(int(file_size) / (2**20), 2)

    print(".........File Uploaded ........")
    print("File Name : "+BASE_URL+S3_BUCKET_NAME +
          S3_PATH+FILENAME)
    print('File Size :'+file_size)


if __name__ == '__main__':
    try:
        # parsing commmand line arguments

        arguments_parser = argparse.ArgumentParser()

        arguments_parser.add_argument(
            '-a', '--accesskey', type=str, help="Your S3 ACCESS KEY", required=True)

        arguments_parser.add_argument(
            '-s', '--secretkey', type=str, help="Your S3 SECRET ACCESS KEY", required=True)

        arguments_parser.add_argument(
            '-b', '--bucket', type=str, help="Your S3 Bucket Name to upload file", required=True)

        arguments_parser.add_argument(
            '-p', '--path', type=str, help="S3 Path with ending '/' ", required=True)

        arguments_parser.add_argument(
            '-f', '--file', type=str, help="File Name to be Uploaded", required=True)

        args = arguments_parser.parse_args()
        accesskey = args.accesskey
        secretkey = args.secretkey
        bucket_name = args.bucket
        s3_path = args.path
        filename = args.file

        print('File : ' + args.file+' Uploading into S3 Bucket : ' +
              bucket_name+'. Please wait..........')

        # Calling upload function with arguments
        upload(AWS_ACCESS_KEY_ID=accesskey, AWS_SECRET_ACCESS_KEY=secretkey,
               S3_BUCKET_NAME=bucket_name, S3_PATH=s3_path, FILENAME=filename)

    except Exception as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
