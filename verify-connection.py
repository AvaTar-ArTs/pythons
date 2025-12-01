# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

from pathlib import Path
import os

import paramiko
from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Load environment variables from .env (ensure your OPENAI_API_KEY is stored here)
env_path = Path(str(Path.home()) + "/.env")
load_dotenv(dotenv_path=env_path)

hostname = os.getenv("HOSTNAME")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
remote_dir = Path("/repo/zip")  # Adjust this path if needed


def verify_ssh_connection():
    """Run a simple command (like 'who') to verify an SSH connection."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command("who")
        output = stdout.read().decode()
        client.close()
        return output.strip() or "No active users found (or command output is empty)."
    except Exception as e:
        return f"SSH connection failed: {e}"


def list_repo_contents():
    """List the files in the repository directory via SFTP."""
    try:
        transport = paramiko.Transport((hostname, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        files = sftp.listdir(remote_dir)
        sftp.close()
        transport.close()
        return files
    except Exception as e:
        return f"SFTP listing failed: {e}"


if __name__ == "__main__":
    logger.info("Verifying SSH connection (using 'who'):")
    ssh_output = verify_ssh_connection()
    logger.info(ssh_output)

    logger.info("\nListing repository contents:")
    repo_files = list_repo_contents()
    logger.info(repo_files)
