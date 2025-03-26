# SCOPE - Gun Retail Sales Prediction Dashboard

This project provides an interactive dashboard for analyzing historical sales data and visualizing sales predictions for a gun retail business.

## Features

- **Historical Sales Analysis**: View sales data by category, date range, and aggregation level
- **Sales Forecasting**: View forecasted sales for different product categories up to 90 days
- **Category Comparison**: Compare performance across product categories
- **Feature Importance**: Understand what factors influence sales for each category
- **What-If Analysis**: Adjust external factors to see how they might impact future sales

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- The launcher will handle virtual environment creation and package installation

### Installation

1. Clone or download this repository
2. Navigate to the scripts directory:
   ```
   cd TEST/scripts
   ```
3. Run the dashboard launcher:
   ```
   python3 streamlit_launcher.py
   ```
   
The launcher will:
- Create a virtual environment in the `TEST/venv` directory
- Install required dependencies in the virtual environment
- Set up the dashboard configuration
- Launch the Streamlit dashboard in your web browser

### Using an Existing Virtual Environment

If you prefer to manage your own virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv ./venv
source ./venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install requirements
pip install -r config/requirements.txt

# Run the dashboard
python3 scripts/streamlit_launcher.py
```

## Dashboard Tabs

### 1. Historical Sales
Analyze historical sales data with filters for:
- Product category
- Date range
- Time aggregation (daily, weekly, monthly)

### 2. Forecast
View sales forecasts with:
- Category selection
- Forecast horizon adjustment
- Confidence intervals

### 3. Category Comparison
Compare sales performance across product categories:
- Different time periods (30 days, 90 days, 6 months, etc.)
- Various metrics (total quantity, total revenue, daily averages)

### 4. Feature Importance
Understand factors driving sales:
- Feature importance graphs for each product category
- Detailed importance rankings

### 5. What-If Analysis
Simulate sales scenarios by adjusting factors:
- Political climate
- Legislation risk
- Seasonal factors
- Economic conditions
- Promotional events

## About the Model

The sales prediction model uses Random Forest regression to forecast sales by product category. Models are trained separately for each category (accessories, ammunition, handguns, rifles, shotguns).

The models consider:
- Temporal patterns (day of week, month, seasonality)
- External factors (political events, legislation, economic indicators)
- Hunting seasons and holidays
- Sales promotions

## Project Structure

- `config/`: Configuration files and requirements
- `data/`: Contains sales transaction data and external factors
- `models/`: Trained prediction models
- `notebooks/`: Jupyter notebooks for data exploration
- `scripts/`: Dashboard and launcher scripts
- `visualizations/`: Charts and visualizations

### Key Files
- `scripts/sales_prediction_model.py`: Model training script
- `scripts/streamlit_dashboard.py`: Interactive dashboard code
- `scripts/streamlit_launcher.py`: Setup and launcher for the dashboard

## Troubleshooting

- If the dashboard doesn't launch automatically, navigate to http://localhost:8501 in your web browser
- If you encounter any issues with missing data or models, check the console output for error messages
- Make sure your directory structure matches the expected layout (see Project Structure)