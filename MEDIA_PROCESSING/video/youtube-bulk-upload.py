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
                            value = value.strip().strip("'").strip("'")
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

import os
import platform
import subprocess


def get_os():
    return platform.system()


def get_cpu_architecture():
    # e.g. x86_64, arm64
    return platform.machine()


def extract_app_version():
    result = subprocess.run(
        ["youtube-bulk-upload", "--version"], capture_output=True, text=True
    )
    version = result.stdout.strip().split()[-1]
    return version


def write_to_github_env(vars_key_values_dict):
    github_env_filepath = os.getenv("GITHUB_ENV")
    print(f"Writing values to GITHUB_ENV file {github_env_filepath}:")

    with open(github_env_filepath, "a") as github_env_file:
        for key, value in vars_key_values_dict.items():
            github_env_file.write(f"{key}={value}\n")
            print(f" {key}={value}")


if __name__ == "__main__":
    vars = {
        "APPNAME": "YouTube Bulk Upload",
        "APPVERSION": extract_app_version(),
        "OPERATINGSYSTEM": get_os(),
        "ARCHITECTURE": get_cpu_architecture(),
    }

    vars["APPNAMEWITHDETAILS"] = (
        f"{vars['APPNAME']} v{vars['APPVERSION']} ({vars['OPERATINGSYSTEM']} {vars['ARCHITECTURE']})"
    )

    write_to_github_env(vars)
