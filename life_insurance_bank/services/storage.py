import base64
import boto3

from botocore.config import Config

from django.conf import settings


class StorageService:

    def __init__(self):
        self.bucket_name = settings.STORAGE_BUCKET_NAME
        config = Config(s3={'addressing_style': 'path'}, signature_version='s3')
        self.client = boto3.client('s3',
                                   endpoint_url=settings.STORAGE_URL,
                                   aws_access_key_id=settings.STORAGE_USERNAME,
                                   aws_secret_access_key=settings.STORAGE_PASSWORD,
                                   config=config)

    def upload(self, key: str, buffer: str):
        bytes_file = bytes(buffer, encoding='utf-8')
        with open('file.csv', 'wb') as file:
            file.write(base64.decodebytes(bytes_file))
        with open('file.csv', 'rb') as file:
            self.client.upload_fileobj(
                Bucket=self.bucket_name, Key=key, Fileobj=file, ExtraArgs={'ACL': 'public-read'})
        return key, file

    def delete(self, key: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=key)
