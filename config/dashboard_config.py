"""
Configuration settings for the Streamlit dashboard.
"""

import os
from .main_config import PROJECT_DIR, DATA_DIR, MODELS_DIR, VISUALIZATIONS_DIR

# Dashboard settings
DASHBOARD_TITLE = "Gun Retail Sales Dashboard"
DASHBOARD_ICON = "📊"
DASHBOARD_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Chart and visualization settings
DEFAULT_CHART_HEIGHT = 400
DEFAULT_CHART_WIDTH = 800
COLOR_PALETTE = {
    'primary': 'tab:blue',
    'secondary': 'tab:red',
    'tertiary': 'tab:green',
    'background': '#f0f2f6',
    'grid': '#ddd'
}

# Date range default settings
DEFAULT_LOOKBACK_DAYS = 90
DEFAULT_FORECAST_DAYS = 30

# Dashboard tabs
TABS = [
    "Historical Sales",
    "Forecast",
    "Category Comparison",
    "Feature Importance",
    "What-If Analysis"
]
