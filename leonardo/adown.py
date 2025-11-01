"""
Adown

This module provides functionality for adown.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import paramiko

import logging

logger = logging.getLogger(__name__)


# SSH Configuration
hostname = "access981577610.webspace-data.io"
username = "u114071855"
password = "A^p1yT@AHn*akbhs"
local_dir = Path("/Users/steven/AvaTarArTs")
remote_dirs = [
    Path("/2025"),
    Path("/Users"),
    Path("/all"),
    Path("/audio-texts"),
    Path("/blog"),
    Path("/build"),
    Path("/card"),
    Path("/city"),
    Path("/clickandbuilds"),
    Path("/convo"),
    Path("/covers"),
    Path("/covers-bak"),
    Path("/css"),
    Path("/csv"),
    Path("/dad"),
    Path("/dalle"),
    Path("/disco"),
    Path("/docs"),
    Path("/etsy"),
    Path("/flow"),
    Path("/follow"),
    Path("/gdrive"),
    Path("/html"),
    Path("/images"),
    Path("/img"),
    Path("/leo"),
    Path("/leoai"),
    Path("/leonardo"),
    Path("/march"),
    Path("/md"),
    Path("/melody"),
    Path("/mp4"),
    Path("/music"),
    Path("/mydesigns"),
    Path("/number"),
    Path("/ny"),
    Path("/oct"),
    Path("/og"),
    Path("/pdf"),
    Path("/python"),
    Path("/repo"),
    Path("/seamless"),
    Path("/test"),
    Path("/trashy"),
    Path("/uploads"),
    Path("/vids"),
    Path("/xmas"),
    Path("/chat.html"),
    Path("/dalle.html"),
    Path("/dallechat.html"),
    Path("/form.html"),
    Path("/index.html"),
    Path("/mush.html"),
    Path("/pod.html"),
    Path("/privacy.html"),
    Path("/seamless.htm"),
]


def list_remote_files(sftp, remote_path):
    """list_remote_files function."""

    try:
        return {f.filename: f.st_mtime for f in sftp.listdir_attr(remote_path)}
    except FileNotFoundError:
        logger.info(f"Remote directory not found: {remote_path}")
        return {}

    """list_local_files function."""


def list_local_files(local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    return set(os.listdir(local_path))

    """download_missing_files function."""


def download_missing_files(sftp, remote_path, local_path):
    os.makedirs(local_path, exist_ok=True)
    remote_files = list_remote_files(sftp, remote_path)
    local_files = list_local_files(local_path)

    for file in remote_files.keys():
        if file not in local_files:
            logger.info(f"Downloading missing file: {file}")
            sftp.get(os.path.join(remote_path, file), os.path.join(local_path, file))
        else:
            logger.info(f"{file} already exists, skipping...")


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

sftp = ssh.open_sftp()

for remote_dir in remote_dirs:
    local_path = os.path.join(local_dir, os.path.basename(remote_dir))
    logger.info(f"Checking for missing files in {remote_dir}...")
    download_missing_files(sftp, remote_dir, local_path)

sftp.close()
ssh.close()
