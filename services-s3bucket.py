"""
Cloud Services Aws S3Bucket 1

This module provides functionality for cloud services aws s3bucket 1.

Author: Auto-generated
Date: 2025-11-01
"""

import boto3
from botocore.config import Config
from utilities.const import AWS_ACCESS_KEY, AWS_SEC_KEY, get_current_date

import logging

logger = logging.getLogger(__name__)


my_config = Config(
    region_name="ap-south-1",
    signature_version="v4",
    retries={"max_attempts": 3, "mode": "standard"},
)
s3 = boto3.client(
    "s3",
    config=my_config,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SEC_KEY,
)


def audio_down(s3_name, audio_book_topic, aws_filename, filename_to_save_local):
    """audio_down function."""

    str_get_current_date = get_current_date()
    s3.download_file(
        s3_name,
        str_get_current_date + "/" + audio_book_topic + "." + aws_filename,
        filename_to_save_local,
    )
    logger.info("file saved: " + filename_to_save_local)

    """get_audio_link function."""


def get_audio_link(bucket_name, audio_book_topic, polly_file_name, topic_type):
    str_get_current_date = get_current_date()
    path_to_file = (
        topic_type
        + "/"
        + str_get_current_date
        + "/"
        + audio_book_topic
        + "."
        + polly_file_name
    )
    location = s3.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
    # Generate the public URL
    url = f"https://{bucket_name}.s3.{location}.amazonaws.com/{path_to_file}"
    return url

    """set_public_access function."""


def set_public_access(bucket_name, audio_book_topic, polly_file_name, topic_type):
    str_get_current_date = get_current_date()
    path_to_file = (
        topic_type
        + "/"
        + str_get_current_date
        + "/"
        + audio_book_topic
        + "."
        + polly_file_name
    )
    response = s3.put_object_acl(
        ACL="public-read", Bucket=bucket_name, Key=path_to_file
    )
    return response
