import os
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

from huggingface_hub import HfApi
from loguru import logger

try:
    from sagemaker.huggingface import HuggingFaceProcessor
except ModuleNotFoundError:
    logger.warning(
        "Couldn't load SageMaker imports. Run 'poetry install --with aws' to support AWS."
    )

from llm_engineering import settings

evaluation_dir = Path(__file__).resolve().parent
evaluation_requirements_path = evaluation_dir / "requirements.txt"


def run_evaluation_on_sagemaker(is_dummy: bool = True) -> None:
    """run_evaluation_on_sagemaker function."""

    assert settings.HUGGINGFACE_ACCESS_TOKEN, "Hugging Face access token is required."
    assert settings.OPENAI_API_KEY, "OpenAI API key is required."
    assert settings.AWS_ARN_ROLE, "AWS ARN role is required."

    if not evaluation_dir.exists():
        raise FileNotFoundError(f"The directory {evaluation_dir} does not exist.")
    if not evaluation_requirements_path.exists():
        raise FileNotFoundError(
            f"The file {evaluation_requirements_path} does not exist."
        )

    api = HfApi()
    user_info = api.whoami(token=settings.HUGGINGFACE_ACCESS_TOKEN)
    huggingface_user = user_info["name"]
    logger.info(f"Current Hugging Face user: {huggingface_user}")

    env = {
        "HUGGING_FACE_HUB_TOKEN": settings.HUGGINGFACE_ACCESS_TOKEN,
        "OPENAI_API_KEY": settings.OPENAI_API_KEY,
        "DATASET_HUGGINGFACE_WORKSPACE": huggingface_user,
        "MODEL_HUGGINGFACE_WORKSPACE": huggingface_user,
    }
    if is_dummy:
        env["IS_DUMMY"] = "True"

    # Initialize the HuggingFaceProcessor
    hfp = HuggingFaceProcessor(
        role=settings.AWS_ARN_ROLE,
        instance_count=1,
        instance_type="ml.g5.2xlarge",
        transformers_version="4.36",
        pytorch_version="2.1",
        py_version="py310",
        base_job_name="evaluate-llm-twin",
        env=env,
    )

    # Run the processing job
    hfp.run(
        code="evaluate.py",
        source_dir=str(evaluation_dir),
    )


if __name__ == "__main__":
    run_evaluation_on_sagemaker()
