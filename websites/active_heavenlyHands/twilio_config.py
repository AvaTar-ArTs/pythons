# Twilio Configuration for Heavenly Hands
# Live credentials for avatararts.org

# Twilio Account Credentials
TWILIO_ACCOUNT_SID = "AC607a77ee54a4dddf63034fe4b3713fb9"
TWILIO_AUTH_TOKEN = "yI6ZMK7hHgDZt1UzkZsSpAfD2S10laJB"

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
SECRET_KEY = "heavenly-hands-secret-key-2024"

# Call tracking settings
CALL_DURATION_LIMIT = 3600  # 1 hour in seconds
MAX_CALLS_PER_DAY = 100

# Email settings (configure with your email service)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "heavenly_hands.log"