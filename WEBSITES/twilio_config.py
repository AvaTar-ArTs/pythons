"""
Summary of twilio_config.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

# Twilio Configuration for Heavenly Hands
# Set these environment variables before running the application:
#   export TWILIO_ACCOUNT_SID="your-account-sid"
#   export TWILIO_AUTH_TOKEN="your-auth-token"
#   export HH_SECRET_KEY="your-secret-key"
#   export HH_EMAIL_PASSWORD="your-app-password"

# Twilio Account Credentials
TWILIO_ACCOUNT_SID = os.environ.get(
    "TWILIO_ACCOUNT_SID",
    ""  # Set via environment - was: "AC607a77ee54a4dddf63034fe4b3713fb9"
)
TWILIO_AUTH_TOKEN = os.environ.get(
    "TWILIO_AUTH_TOKEN",
    ""  # Set via environment - was: "yI6ZMK7hHgDZt1UzkZsSpAfD2S10laJB"
)

# Twilio Phone Numbers (you'll need to add these from your Twilio console)
TWILIO_PHONE_NUMBER = "+1234567890"  # Replace with your actual Twilio number
CALLER_ID = "Heavenly Hands Cleaning"

# Webhook URLs (update these with your actual domain)
WEBHOOK_BASE_URL = "https://heavenlyhands.avatararts.org"
WEBHOOK_URL = f"{WEBHOOK_BASE_URL}/webhook"

# Database configuration
DATABASE_URL = "sqlite:///heavenly_hands.db"

# Application settings
DEBUG = False
SECRET_KEY = os.environ.get(
    "HH_SECRET_KEY",
    ""  # Set via environment - was: "heavenly-hands-secret-key-2024"
)

# Call tracking settings
CALL_DURATION_LIMIT = 3600  # 1 hour in seconds
MAX_CALLS_PER_DAY = 100

# Email settings (configure with your email service)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"
EMAIL_PASSWORD = os.environ.get(
    "HH_EMAIL_PASSWORD",
    ""  # Set via environment - was: "your-app-password"
)

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "heavenly_hands.log"
