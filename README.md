# SCOPE - Gun Retail Sales Prediction Dashboard

This project provides an interactive dashboard for analyzing historical sales data and visualizing sales predictions for a gun retail business.

## Features

- **Historical Sales Analysis**: View sales data by category, date range, and aggregation level
- **Sales Forecasting**: View forecasted sales for different product categories up to 90 days
- **Category Comparison**: Compare performance across product categories
- **Feature Importance**: Understand what factors influence sales for each category
- **What-If Analysis**: Adjust external factors to see how they might impact future sales

## Project Structure

```
SCOPE/
├── config/             # Configuration files
├── scope/              # Core package
│   ├── utils/          # Utility functions
│   ├── data/           # Data files
│   ├── models/         # Trained models
│   └── visualizations/ # Generated visualizations
├── scripts/            # Executable scripts
└── tests/              # Test files
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- The launcher will handle virtual environment creation and package installation

### Installation

1. Clone or download this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the dashboard launcher:
   ```bash
   python scripts/streamlit_launcher.py
   ```

The launcher will:
- Set up the dashboard configuration
- Launch the Streamlit dashboard in your web browser

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

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Troubleshooting

- If the dashboard doesn't launch automatically, navigate to http://localhost:8501 in your web browser
- If you encounter any issues with missing data or models, check the console output for error messages
