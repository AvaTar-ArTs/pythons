# test_environment.py
import sys

import librosa
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

print(f"Python version: {sys.version}")
print(f"Pandas version: {pd.__version__}")
print(f"Librosa version: {librosa.__version__}")

# Test audio analysis
y, sr = librosa.load(librosa.ex("trumpet"))
print(f"Audio sample loaded: {len(y)} samples at {sr}Hz")
