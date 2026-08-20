import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Application configuration
class Config:
    # Database configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{os.getenv('DB_USER', 'u365102102_gptjunkie')}:{os.getenv('DB_PASSWORD', '0t90e75@c#YVwlZ0')}@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DB_NAME', 'u365102102_gptjunkie')}",
    )

    # Application settings
    APP_NAME = os.getenv("APP_NAME", "nocTurneMeLoDieS API")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

    # API settings
    API_V1_STR = "/api/v1"
    PROJECT_NAME = os.getenv("PROJECT_NAME", "nocTurneMeLoDieS")

    # CORS settings
    BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")

    # File upload settings
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50"))  # in MB
    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "mp3,wav,flac,png,jpg,jpeg,txt,pdf").split(",")


# Create config instance
config = Config()
