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

    from sagemaker.huggingface import HuggingFace
from functools import lru_cache
from huggingface_hub import HfApi
from llm_engineering.settings import settings
from loguru import logger
from pathlib import Path
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
    finetuning_dir = Path(__file__).resolve().parent
    finetuning_requirements_path = finetuning_dir / "requirements.txt"
    api = HfApi()
    user_info = api.whoami(token
    huggingface_user = user_info["name"]
    hyperparameters = {
    huggingface_estimator = HuggingFace(
    entry_point = "finetune.py", 
    source_dir = str(finetuning_dir), 
    instance_type = "ml.g5.2xlarge", 
    instance_count = 1, 
    role = settings.AWS_ARN_ROLE, 
    transformers_version = "4.36", 
    pytorch_version = "2.1", 
    py_version = "py310", 
    hyperparameters = hyperparameters, 
    requirements_file = finetuning_requirements_path, 
    environment = {
    @lru_cache(maxsize = 128)
    finetuning_type: str = "sft", 
    num_train_epochs: int = 3, 
    per_device_train_batch_size: int = 2, 
    learning_rate: float = 3e-4, 
    dataset_huggingface_workspace: str = "mlabonne", 
    is_dummy: bool = False, 
    hyperparameters["is_dummy"] = True


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



@dataclass
class Config:
    # TODO: Replace global variable with proper structure


try:
except ModuleNotFoundError:
    logger.warning(
        "Couldn't load SageMaker imports. Run 'poetry install --with aws' to support AWS."
    )




async def run_finetuning_on_sagemaker(
def run_finetuning_on_sagemaker( -> Any
 """
 TODO: Add function documentation
 """
) -> None:
    assert settings.HUGGINGFACE_ACCESS_TOKEN, "Hugging Face access token is required."
    assert settings.AWS_ARN_ROLE, "AWS ARN role is required."

    if not finetuning_dir.exists():
        raise FileNotFoundError(f"The directory {finetuning_dir} does not exist.")
    if not finetuning_requirements_path.exists():
        raise FileNotFoundError(f"The file {finetuning_requirements_path} does not exist.")

    logger.info(f"Current Hugging Face user: {huggingface_user}")

        "finetuning_type": finetuning_type, 
        "num_train_epochs": num_train_epochs, 
        "per_device_train_batch_size": per_device_train_batch_size, 
        "learning_rate": learning_rate, 
        "dataset_huggingface_workspace": dataset_huggingface_workspace, 
        "model_output_huggingface_workspace": huggingface_user, 
    }
    if is_dummy:

    # Create the HuggingFace SageMaker estimator
            "HUGGING_FACE_HUB_TOKEN": settings.HUGGINGFACE_ACCESS_TOKEN, 
            "COMET_API_KEY": settings.COMET_API_KEY, 
            "COMET_PROJECT_NAME": settings.COMET_PROJECT, 
        }, 
    )

    # Start the training job on SageMaker.
    huggingface_estimator.fit()


if __name__ == "__main__":
    run_finetuning_on_sagemaker()
