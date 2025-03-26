#!/usr/bin/env python3
# Sales Prediction Model
# This script trains and evaluates the Random Forest regression models for sales prediction

import pandas as pd
import numpy as np
import os
import sys
import joblib
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))
try:
    from main_config import PROJECT_DIR, DATA_DIR, MODELS_DIR, PRODUCT_CATEGORIES, DEFAULT_MODEL_PARAMS
except ImportError:
    print("Warning: Could not import from main_config, using default values")
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_DIR, 'data')
    MODELS_DIR = os.path.join(os.path.dirname(PROJECT_DIR), 'models')
    PRODUCT_CATEGORIES = ['accessories', 'ammunition', 'handgun', 'rifle', 'shotgun']
    DEFAULT_MODEL_PARAMS = {
        'n_estimators': 100,
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'random_state': 42
    }

def find_file(filename, directory):
    """Find a file in directory, checking for lowercase and uppercase variants"""
    
    # Check for exact match
    exact_path = os.path.join(directory, filename)
    if os.path.exists(exact_path):
        return exact_path
    
    # Check for lowercase variant
    lowercase_path = os.path.join(directory, f"lowercase_{filename}")
    if os.path.exists(lowercase_path):
        return lowercase_path
    
    # Check for capitalized variant
    capitalized_path = os.path.join(directory, filename.capitalize())
    if os.path.exists(capitalized_path):
        return capitalized_path
    
    # If we couldn't find any variant, return the default path
    print(f"Warning: Could not find {filename} in {directory}, defaulting to the standard path")
    return exact_path

def find_column_by_pattern(df, patterns):
    """Find a column name that contains any of the specified patterns"""
    for pattern in patterns:
        matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
        if matching_cols:
            return matching_cols[0]
    
    # If no match found, return the first column as a fallback
    print(f"Warning: Could not find column matching patterns {patterns}, using first column")
    return df.columns[0]

def load_and_prepare_data():
    """Load and prepare the data for model training"""
    
    # Load datasets
    transactions_file = find_file('gun_retail_transactions.csv', DATA_DIR)
    transaction_items_file = find_file('gun_retail_transaction_items.csv', DATA_DIR)
    products_file = find_file('gun_retail_products.csv', DATA_DIR)
    external_factors_file = find_file('gun_retail_external_factors.csv', DATA_DIR)
    
    print(f"Loading data from: {DATA_DIR}")
    print(f"  Transactions: {transactions_file}")
    print(f"  Transaction items: {transaction_items_file}")
    print(f"  Products: {products_file}")
    print(f"  External factors: {external_factors_file}")
    
    # Load the files
    transactions = pd.read_csv(transactions_file)
    transaction_items = pd.read_csv(transaction_items_file)
    products = pd.read_csv(products_file)
    external_factors = pd.read_csv(external_factors_file)
    
    # Identify key columns
    transactions_date_col = find_column_by_pattern(transactions, ['date', 'time'])
    external_factors_date_col = find_column_by_pattern(external_factors, ['date'])
    category_col = find_column_by_pattern(products, ['categ'])
    product_id_col = find_column_by_pattern(transaction_items, ['product', 'id'])
    transaction_id_col = find_column_by_pattern(transaction_items, ['transaction', 'id'])
    quantity_col = find_column_by_pattern(transaction_items, ['quant'])
    
    # Convert date columns to datetime
    transactions[transactions_date_col] = pd.to_datetime(transactions[transactions_date_col])
    transactions['date'] = transactions[transactions_date_col].dt.date
    transactions['date'] = pd.to_datetime(transactions['date'])
    
    external_factors[external_factors_date_col] = pd.to_datetime(external_factors[external_factors_date_col])
    
    # Create sales data by merging datasets
    sales_data = transaction_items.merge(transactions, on=transaction_id_col)
    sales_data = sales_data.merge(products[[product_id_col, category_col]], on=product_id_col)
    
    # Aggregate by date and category
    daily_sales = sales_data.groupby(['date', category_col]).agg({
        quantity_col: 'sum'
    }).reset_index()
    
    # Rename columns for clarity
    daily_sales = daily_sales.rename(columns={quantity_col: 'quantity_sold'})
    
    # Create a date range covering all days in the data
    min_date = daily_sales['date'].min()
    max_date = daily_sales['date'].max()
    all_dates = pd.date_range(min_date, max_date, freq='D')
    
    # Create a cross product of all dates and categories
    date_category = pd.MultiIndex.from_product([all_dates, daily_sales[category_col].unique()], 
                                              names=['date', category_col])
    date_category_df = pd.DataFrame(index=date_category).reset_index()
    
    # Merge with sales data to fill in missing days
    complete_sales = date_category_df.merge(daily_sales, on=['date', category_col], how='left')
    complete_sales['quantity_sold'] = complete_sales['quantity_sold'].fillna(0)
    
    # Add time-based features
    complete_sales['dayofweek'] = complete_sales['date'].dt.dayofweek
    complete_sales['month'] = complete_sales['date'].dt.month
    complete_sales['day'] = complete_sales['date'].dt.day
    complete_sales['year'] = complete_sales['date'].dt.year
    complete_sales['quarter'] = complete_sales['date'].dt.quarter
    complete_sales['is_weekend'] = (complete_sales['dayofweek'] >= 5).astype(int)
    
    # Merge with external factors data
    complete_sales = complete_sales.merge(external_factors, left_on='date', right_on=external_factors_date_col, how='left')
    
    # Forward fill missing external factors (use previous day's values)
    external_factor_cols = [col for col in external_factors.columns if col != external_factors_date_col]
    complete_sales[external_factor_cols] = complete_sales[external_factor_cols].fillna(method='ffill')
    
    return complete_sales, category_col

def prepare_features(df, category_col, selected_category):
    """Prepare features for a specific category"""
    
    # Filter data for the selected category
    category_data = df[df[category_col] == selected_category].copy()
    
    # Drop non-feature columns
    feature_data = category_data.drop(['date', category_col], axis=1)
    
    # Check for and handle any remaining missing values
    for col in feature_data.columns:
        if feature_data[col].isna().any():
            # For numeric columns, fill with mean
            if pd.api.types.is_numeric_dtype(feature_data[col]):
                feature_data[col] = feature_data[col].fillna(feature_data[col].mean())
            else:
                # For categorical columns, fill with mode
                feature_data[col] = feature_data[col].fillna(feature_data[col].mode()[0])
    
    # Get features and target
    X = feature_data.drop('quantity_sold', axis=1)
    y = feature_data['quantity_sold']
    
    return X, y

def evaluate_model(model, X, y):
    """Evaluate the model using cross-validation and test set performance"""
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation score
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return {
        'model': model,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'cv_r2': cv_scores.mean(),
        'feature_importance': feature_importance
    }

def train_model(category, data, category_col):
    """Train and save a model for a specific category"""
    print(f"Training model for category: {category}")
    
    # Prepare features
    X, y = prepare_features(data, category_col, category)
    
    # Create and train model
    model = RandomForestRegressor(**DEFAULT_MODEL_PARAMS)
    
    # Evaluate model
    results = evaluate_model(model, X, y)
    
    # Print evaluation metrics
    print(f"  RMSE: {results['rmse']:.2f}")
    print(f"  MAE: {results['mae']:.2f}")
    print(f"  R^2: {results['r2']:.2f}")
    print(f"  Cross-validated R^2: {results['cv_r2']:.2f}")
    print(f"  Top 5 important features:")
    for i, row in results['feature_importance'].head(5).iterrows():
        print(f"    {row['Feature']}: {row['Importance']:.3f}")
    
    # Save model
    output_dir = MODELS_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    model_path = os.path.join(output_dir, f'sales_forecast_{category}.pkl')
    joblib.dump(model, model_path)
    print(f"  Model saved to: {model_path}")
    
    return results

def generate_forecast(models, data, category_col, days=90):
    """Generate forecasts for all categories"""
    print(f"Generating {days}-day forecast")
    
    # Get the last date in the data
    last_date = data['date'].max()
    
    # Create date range for forecast
    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({'date': forecast_dates})
    
    # Add date-based features
    forecast_df['dayofweek'] = forecast_df['date'].dt.dayofweek
    forecast_df['month'] = forecast_df['date'].dt.month
    forecast_df['day'] = forecast_df['date'].dt.day
    forecast_df['year'] = forecast_df['date'].dt.year
    forecast_df['quarter'] = forecast_df['date'].dt.quarter
    forecast_df['is_weekend'] = (forecast_df['dayofweek'] >= 5).astype(int)
    
    # Get the latest external factors
    last_external_factors = {}
    external_factor_cols = [col for col in data.columns if col not in 
                           ['date', category_col, 'quantity_sold', 'dayofweek', 'month', 'day', 'year', 'quarter', 'is_weekend']]
    
    for col in external_factor_cols:
        # Get the last non-null value
        last_val = data[col].dropna().iloc[-1] if not data[col].dropna().empty else 0
        last_external_factors[col] = last_val
        forecast_df[col] = last_val
    
    # Make predictions for each category
    for category, model in models.items():
        # Prepare input features for prediction
        X_forecast = forecast_df.drop('date', axis=1)
        
        # Make prediction
        y_forecast = model.predict(X_forecast)
        
        # Add predictions to forecast df
        forecast_df[category] = y_forecast
    
    # Save forecast to CSV
    forecast_path = os.path.join(DATA_DIR, 'sales_forecast_next_90_days.csv')
    forecast_df.to_csv(forecast_path, index=False)
    print(f"Forecast saved to: {forecast_path}")
    
    return forecast_df

def main():
    """Main function to train models and generate forecasts"""
    print("Starting sales prediction model training")
    
    # Check if models directory exists
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"Created models directory: {MODELS_DIR}")
    
    # Load and prepare data
    data, category_col = load_and_prepare_data()
    
    # Train models for each category
    models = {}
    for category in PRODUCT_CATEGORIES:
        result = train_model(category, data, category_col)
        models[category] = result['model']
    
    # Generate forecast
    forecast = generate_forecast(models, data, category_col)
    
    print("Model training and forecast generation complete!")

if __name__ == "__main__":
    main()
