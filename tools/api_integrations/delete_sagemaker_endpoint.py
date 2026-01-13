# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    from botocore.exceptions import ClientError
    import boto3
from functools import lru_cache
from llm_engineering.settings import settings
from loguru import logger
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    @lru_cache(maxsize = 128)
    sagemaker_client = boto3.client(
    region_name = settings.AWS_REGION, 
    aws_access_key_id = settings.AWS_ACCESS_KEY, 
    aws_secret_access_key = settings.AWS_SECRET_KEY, 
    response = sagemaker_client.describe_endpoint(EndpointName
    config_name = response["EndpointConfigName"]
    sagemaker_client.delete_endpoint(EndpointName = endpoint_name)
    response = sagemaker_client.describe_endpoint_config(EndpointConfigName
    model_name = response["ProductionVariants"][0]["ModelName"]
    sagemaker_client.delete_endpoint_config(EndpointConfigName = config_name)
    sagemaker_client.delete_model(ModelName = model_name)
    endpoint_name = settings.SAGEMAKER_ENDPOINT_INFERENCE
    delete_endpoint_and_config(endpoint_name = endpoint_name)


# Constants



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


try:
except ModuleNotFoundError:
    logger.warning(
        "Couldn't load AWS or SageMaker imports. Run 'poetry install --with aws' to support AWS."
    )




async def delete_endpoint_and_config(endpoint_name) -> None:
def delete_endpoint_and_config(endpoint_name) -> None:
    """
    Deletes an AWS SageMaker endpoint and its associated configuration.
    Args:
    endpoint_name (str): The name of the SageMaker endpoint to delete.
    Returns:
    None
    """

    try:
            "sagemaker", 
        )
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        logger.exception("Error creating SageMaker client")

        return

    # Get the endpoint configuration name
    try:
    except ClientError:
        logger.error("Error getting endpoint configuration and modelname.")

        return

    # Delete the endpoint
    try:
        logger.info(f"Endpoint '{endpoint_name}' deletion initiated.")
    except ClientError:
        logger.error("Error deleting endpoint")

    try:
    except ClientError:
        logger.error("Error getting model name.")

    # Delete the endpoint configuration
    try:
        logger.info(f"Endpoint configuration '{config_name}' deleted.")
    except ClientError:
        logger.error("Error deleting endpoint configuration.")

    # Delete models
    try:
        logger.info(f"Model '{model_name}' deleted.")
    except ClientError:
        logger.error("Error deleting model.")


if __name__ == "__main__":
    logger.info(f"Attempting to delete endpoint: {endpoint_name}")
