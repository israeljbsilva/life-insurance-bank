import boto3
import logging

from botocore.utils import fix_s3_host
from io import BytesIO


logger = logging.getLogger(__name__)
logger.info(__name__)


class StorageService:

    def __init__(self, url, login, password, bucket, storage_dir):
        self._s3_resource = boto3.resource(
            's3', endpoint_url=url, aws_access_key_id=login, aws_secret_access_key=password)
        self.client = self._s3_resource.meta.client
        self.client.meta.events.unregister('before-sign.s3', fix_s3_host)
        self.bucket = bucket
        self.storage_dir = storage_dir
        self._last_uploaded_keys = []

    def upload(self, filename: str, stream: BytesIO):
        key = f'{self.storage_dir}/{filename}'
        self._last_uploaded_keys.append(key)
        self.client.upload_fileobj(Fileobj=stream, Bucket=self.bucket, Key=key)

    def download(self, filename: str) -> BytesIO:
        buffer = BytesIO()
        self.client.download_fileobj(Bucket=self.bucket, Key=f'{self.storage_dir}/{filename}', Fileobj=buffer)
        buffer.seek(0)
        return buffer

    def rollback(self):
        try:
            for key in self._last_uploaded_keys:
                obj = self._s3_resource.Object(self.bucket, key)
                obj.delete()
        except Exception:
            pass

        self._last_uploaded_keys.clear()
