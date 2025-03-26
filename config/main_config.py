"""
Main configuration settings for the SCOPE project.
"""

import os

# Base directory structure
PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'scope', 'data')
MODELS_DIR = os.path.join(PROJECT_DIR, 'scope', 'models')
VISUALIZATIONS_DIR = os.path.join(PROJECT_DIR, 'scope', 'visualizations')

# Default model configuration
DEFAULT_MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': None,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'random_state': 42
}

# Product categories
PRODUCT_CATEGORIES = [
    'accessories',
    'ammunition',
    'handgun',
    'rifle',
    'shotgun'
]

# Forecast settings
DEFAULT_FORECAST_HORIZON = 90  # days
CONFIDENCE_INTERVAL = 0.9  # 90% confidence interval

# External factors influence weights
EXTERNAL_FACTOR_WEIGHTS = {
    'political_climate': 0.3,
    'legislation_risk': 0.25,
    'economic_indicators': 0.15,
    'seasonal_factors': 0.2,
    'promotional_events': 0.1
}
