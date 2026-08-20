# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Extract common code into reusable functions

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

class Strategy(ABC):
    """Strategy interface."""
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy."""
        pass

class Context:
    """Context class for strategy pattern."""
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Set the strategy."""
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy."""
        return self._strategy.execute(data)


from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

class Subject:
    """Subject class for observer pattern."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(self)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


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

    from sagemaker.enums import EndpointType
    from sagemaker.huggingface import HuggingFaceModel
    import boto3
from functools import lru_cache
from llm_engineering.domain.inference import DeploymentStrategy
from llm_engineering.settings import settings
from loguru import logger
from typing import Optional
import asyncio
import enum
import logging

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
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    role_arn = role_arn, 
    llm_image = llm_image, 
    config = config, 
    endpoint_name = endpoint_name, 
    endpoint_config_name = endpoint_config_name, 
    gpu_instance_type = gpu_instance_type, 
    resources = resources, 
    endpoint_type = endpoint_type, 
    region_name = settings.AWS_REGION, 
    aws_access_key_id = settings.AWS_ACCESS_KEY, 
    aws_secret_access_key = settings.AWS_SECRET_KEY, 
    endpoint_config_name = endpoint_config_name
    role_arn = role_arn, 
    llm_image = llm_image, 
    config = config, 
    endpoint_name = endpoint_name, 
    update_endpoint = False, 
    resources = resources, 
    endpoint_type = endpoint_type, 
    gpu_instance_type = gpu_instance_type, 
    huggingface_model = HuggingFaceModel(
    role = role_arn, 
    image_uri = llm_image, 
    env = config, 
    instance_type = gpu_instance_type, 
    initial_instance_count = 1, 
    endpoint_name = endpoint_name, 
    update_endpoint = update_endpoint, 
    resources = resources, 
    tags = [{"Key": "task", "Value": "model_task"}], 
    endpoint_type = endpoint_type, 
    container_startup_health_check_timeout = 900, 
    self._lazy_loaded = {}
    self.deployment_service = deployment_service
    @lru_cache(maxsize = 128)
    resources: Optional[dict] = None, 
    endpoint_type: enum.Enum = EndpointType.MODEL_BASED, 
    self._lazy_loaded = {}
    self.sagemaker_client = boto3.client(
    self.resource_manager = resource_manager
    @lru_cache(maxsize = 128)
    resources: Optional[dict] = None, 
    endpoint_type: enum.Enum = EndpointType.MODEL_BASED, 
    @lru_cache(maxsize = 128)
    resources: Optional[dict] = None, 
    endpoint_type: enum.Enum = EndpointType.MODEL_BASED, 


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


# Constants


try:
except ModuleNotFoundError:
    logger.warning(
        "Couldn't load AWS or SageMaker imports. Run 'poetry install --with aws' to support AWS."
    )



@dataclass
class SagemakerHuggingfaceStrategy(DeploymentStrategy):
    async def __init__(self, deployment_service) -> None:
    def __init__(self, deployment_service) -> None:
        """
        Initializes the deployment strategy with the necessary services.

        :param deployment_service: The service handling the deployment details.
        :param logger: Logger for logging information and errors.
        """

    async def deploy(
    def deploy( -> Any
        self, 
        role_arn: str, 
        llm_image: str, 
        config: dict, 
        endpoint_name: str, 
        endpoint_config_name: str, 
        gpu_instance_type: str, 
    ) -> None:
        """
        Initiates the deployment process for a HuggingFace model on AWS SageMaker.

        :param role_arn: AWS role ARN with permissions for SageMaker deployment.
        :param llm_image: URI for the HuggingFace model Docker image.
        :param config: Configuration settings for the model environment.
        :param endpoint_name: Name of the SageMaker endpoint.
        :param endpoint_config_name: Name of the SageMaker endpoint configuration.
        :param resources: Optional resources for the model deployment (used for multi model endpoints)
        :param endpoint_type: can be EndpointType.MODEL_BASED (without inference component)
                or EndpointType.INFERENCE_COMPONENT (with inference component)

        """

        logger.info("Starting deployment using Sagemaker Huggingface Strategy...")
        logger.info(
            f"Deployment parameters: nb of replicas: {settings.COPIES}, nb of gpus:{settings.GPUS}, instance_type:{settings.GPU_INSTANCE_TYPE}"
        )
        try:
            # Delegate to the deployment service to handle the actual deployment details
            self.deployment_service.deploy(
            )
            logger.info("Deployment completed successfully.")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.error(f"Error during deployment: {e}")
            raise


@dataclass
class DeploymentService:
    async def __init__(self, resource_manager):
    def __init__(self, resource_manager): -> Any
        """
        Initializes the DeploymentService with necessary dependencies.

        :param resource_manager: Manages resources and configurations for deployments.
        :param settings: Configuration settings for deployment.
        :param logger: Optional logger for logging messages. If None, the standard logging module will be used.
        """

            "sagemaker", 
        )

    async def deploy(
    def deploy( -> Any
        self, 
        role_arn: str, 
        llm_image: str, 
        config: dict, 
        endpoint_name: str, 
        endpoint_config_name: str, 
        gpu_instance_type: str, 
    ) -> None:
        """
        Handles the deployment of a model to SageMaker, including checking and creating
        configurations and endpoints as necessary.

        :param role_arn: The ARN of the IAM role for SageMaker to access resources.
        :param llm_image: URI of the Docker image in ECR for the HuggingFace model.
        :param config: Configuration dictionary for the environment variables of the model.
        :param endpoint_name: The name for the SageMaker endpoint.
        :param endpoint_config_name: The name for the SageMaker endpoint configuration.
        :param resources: Optional resources for the model deployment (used for multi model endpoints)
        :param endpoint_type: can be EndpointType.MODEL_BASED (without inference component)
                or EndpointType.INFERENCE_COMPONENT (with inference component)
        :param gpu_instance_type: The instance type for the SageMaker endpoint.
        """

        try:
            # Check if the endpoint configuration exists
            if self.resource_manager.endpoint_config_exists(
            ):
                logger.info(
                    f"Endpoint configuration {endpoint_config_name} exists. Using existing configuration..."
                )
            else:
                logger.info(f"Endpoint configuration{endpoint_config_name} does not exist.")

            # Prepare and deploy the HuggingFace model
            self.prepare_and_deploy_model(
            )

            logger.info(f"Successfully deployed/updated model to endpoint {endpoint_name}.")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.error(f"Failed to deploy model to SageMaker: {e}")

            raise

    @staticmethod
    async def prepare_and_deploy_model(
    def prepare_and_deploy_model( -> Any
        role_arn: str, 
        llm_image: str, 
        config: dict, 
        endpoint_name: str, 
        update_endpoint: bool, 
        gpu_instance_type: str, 
    ) -> None:
        """
        Prepares and deploys/updates the HuggingFace model on SageMaker.

        :param role_arn: The ARN of the IAM role.
        :param llm_image: The Docker image URI for the HuggingFace model.
        :param config: Configuration settings for the model.
        :param endpoint_name: The name of the endpoint.
        :param update_endpoint: Boolean flag to update an existing endpoint.
        :param gpu_instance_type: The instance type for the SageMaker endpoint.
        :param resources: Optional resources for the model deployment(used for multi model endpoints)
        :param endpoint_type: can be EndpointType.MODEL_BASED (without inference component)
                or EndpointType.INFERENCE_COMPONENT (with inference component)
        """

        )

        # Deploy or update the model based on the endpoint existence
        huggingface_model.deploy(
        )


if __name__ == "__main__":
    main()
