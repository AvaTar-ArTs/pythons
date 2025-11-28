import sys

import librosa
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

import logging

logger = logging.getLogger(__name__)


logger.info(f"Python version: {sys.version}")
logger.info(f"Pandas version: {pd.__version__}")
logger.info(f"Librosa version: {librosa.__version__}")

# Test audio analysis
y, sr = librosa.load(librosa.ex("trumpet"))
logger.info(f"Audio sample loaded: {len(y)} samples at {sr}Hz")
