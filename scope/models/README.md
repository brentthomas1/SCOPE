# Models Directory

This directory contains the trained machine learning models for the SCOPE project.

## Expected Files

The application expects the following model files:

- `sales_forecast_accessories.pkl`: Random Forest model for accessories sales forecasting
- `sales_forecast_ammunition.pkl`: Random Forest model for ammunition sales forecasting
- `sales_forecast_handgun.pkl`: Random Forest model for handgun sales forecasting
- `sales_forecast_rifle.pkl`: Random Forest model for rifle sales forecasting
- `sales_forecast_shotgun.pkl`: Random Forest model for shotgun sales forecasting

## Model Training

These models are trained using the sales prediction model script:

```bash
python scripts/sales_prediction_model.py
```

## Model Format

Models are saved using joblib, which is more efficient than pickle for large NumPy arrays.
