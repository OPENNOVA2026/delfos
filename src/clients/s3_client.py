import json
import tempfile
from datetime import datetime
from functools import lru_cache
from typing import Any

import boto3
from botocore.exceptions import ClientError

from core.logger import logger
from core.settings import settings
from domain.models import Trend


class S3Client:
    def __init__(self):
        params = {"endpoint_url": settings.aws_s3_endpoint}

        if aws_access_key_id := settings.aws_access_key:
            params["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key := settings.aws_secret_key:
            params["aws_secret_access_key"] = aws_secret_access_key
        if region_name := settings.aws_region:
            params["region_name"] = region_name

        self.client = boto3.client("s3", **params)

    def upload_news(self, infovoids: list[Trend]) -> str:
        logger.info("Uploading news")
        date = datetime.now()
        date_str = date.strftime("%Y/%m/%d")
        hour_str = date.strftime("%H_%M")
        with tempfile.TemporaryFile() as out:
            for trend in infovoids:
                line = trend.model_dump_json() + "\n"
                out.write(line.encode("utf-8"))
            out.seek(0)

            path = f"news/{date_str}/{hour_str}_infovoids_news.jsonl"

            self.client.upload_fileobj(
                out,
                settings.aws_s3_infovoid_bucket,
                path,
            )
            logger.info("News file uploaded")
            return path

    def upload_metadata(self, metadata: dict[str, Any]):
        logger.info("Uploading metadata")
        date = datetime.now()
        date_str = date.strftime("%Y/%m/%d")
        hour_str = date.strftime("%H_%M")
        with tempfile.TemporaryFile() as out:
            metadata = json.dumps(metadata, ensure_ascii=False)
            out.write(metadata.encode("utf-8"))
            out.seek(0)
            self.client.upload_fileobj(
                out,
                settings.aws_s3_infovoid_bucket,
                f"meta/{date_str}/{hour_str}_metadata.jsonl",
            )
        logger.info("Metadata file uploaded")

    def get_raw_config_by_id(self, config_id: int) -> dict[str, Any]:
        bucket = settings.aws_s3_infovoid_bucket
        key = "config.json"

        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code in {"NoSuchKey", "404", "NoSuchBucket"}:
                raise FileNotFoundError(
                    f"Config file not found in S3 bucket: s3://{bucket}/{key}"
                ) from exc

            raise

        raw_body = response["Body"].read().decode("utf-8")
        configs = json.loads(raw_body)

        if not isinstance(configs, dict):
            raise ValueError("Invalid config.json format: expected a dict of configs")

        config = configs.get(config_id)

        if config is not None:
            return config

        raise ValueError(f"Config with id={config_id} not found in config.json")


@lru_cache
def get_s3_client():
    return S3Client()
