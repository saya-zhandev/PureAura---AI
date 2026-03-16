import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_air_quality_data(PureAura-AI\PureAura---AI\Raw_data):
    """
    Analyze the air quality data structure
    """Ra
    df = pd.read_excel("C:\Users\apo22\PureAura-AI\PureAura---AI\Raw_data")
    
    print("=== Data Overview ===")
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nBasic Statistics:\n{df.describe()}")
    
    return df

def preprocess_air_quality_data(df):
    """
    Clean and prepare data for modeling
    """
    # Handle missing timestamps
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values('Time')
    
    # Handle missing value
    
    # Interpolate for medium gaps
    df = df.interpolate(method='time', limit_direction='both')
    
    # Create time-based features
    df['Hour'] = df['Time'].dt.hour
    df['Day'] = df['Time'].dt.day
    df['Month'] = df['Time'].dt.month
    df['DayOfWeek'] = df['Time'].dt.dayofweek
    
    return df

