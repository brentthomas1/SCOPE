"""
Data utility functions for the SCOPE project.
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np
from .file_utils import find_file

def find_column_by_pattern(df, patterns):
    """
    Find a column name that contains any of the specified patterns.
    
    Args:
        df (pandas.DataFrame): The dataframe to search in
        patterns (list): List of patterns to search for
        
    Returns:
        str: Name of the matching column or the first column if no match
    """
    for pattern in patterns:
        matching_cols = [col for col in df.columns if pattern.lower() in col.lower()]
        if matching_cols:
            return matching_cols[0]
    
    # If no match found, return the first column as a fallback
    print(f"Warning: Could not find column matching patterns {patterns}, using first column")
    return df.columns[0]

def load_datasets(data_dir):
    """
    Load and prepare all datasets needed for analysis.
    
    Args:
        data_dir (str): Path to the data directory
        
    Returns:
        tuple: (transactions, transaction_items, products, external_factors, 
                key_columns dictionary)
    """
    # Find dataset files
    transactions_file = find_file('gun_retail_transactions.csv', data_dir)
    transaction_items_file = find_file('gun_retail_transaction_items.csv', data_dir)
    products_file = find_file('gun_retail_products.csv', data_dir)
    external_factors_file = find_file('gun_retail_external_factors.csv', data_dir)
    
    print(f"Loading data from: {data_dir}")
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
    line_total_col = find_column_by_pattern(transaction_items, ['total', 'price', 'amount'])
    
    # Convert date columns to datetime
    transactions[transactions_date_col] = pd.to_datetime(transactions[transactions_date_col])
    transactions['date'] = transactions[transactions_date_col].dt.date
    transactions['date'] = pd.to_datetime(transactions['date'])
    
    external_factors[external_factors_date_col] = pd.to_datetime(external_factors[external_factors_date_col])
    
    # Store key columns in a dictionary for easy access
    key_columns = {
        'transactions_date_col': transactions_date_col,
        'external_factors_date_col': external_factors_date_col,
        'category_col': category_col,
        'product_id_col': product_id_col,
        'transaction_id_col': transaction_id_col,
        'quantity_col': quantity_col,
        'line_total_col': line_total_col
    }
    
    return transactions, transaction_items, products, external_factors, key_columns

def prepare_sales_data(transactions, transaction_items, products, key_columns):
    """
    Prepare sales data by merging and aggregating datasets.
    
    Args:
        transactions (pandas.DataFrame): Transactions data
        transaction_items (pandas.DataFrame): Transaction items data
        products (pandas.DataFrame): Products data
        key_columns (dict): Dictionary of key column names
        
    Returns:
        tuple: (daily_sales, sales_pivot)
    """
    # Extract column names
    category_col = key_columns['category_col']
    product_id_col = key_columns['product_id_col']
    transaction_id_col = key_columns['transaction_id_col']
    quantity_col = key_columns['quantity_col']
    line_total_col = key_columns['line_total_col']
    
    # Create sales data by merging datasets
    sales_data = transaction_items.merge(transactions, on=transaction_id_col)
    sales_data = sales_data.merge(products[[product_id_col, category_col]], on=product_id_col)
    
    # Aggregate by date and category
    daily_sales = sales_data.groupby(['date', category_col]).agg(
        quantity_sold=(quantity_col, 'sum'),
        sales_amount=(line_total_col, 'sum')
    ).reset_index()
    
    # Create pivot table
    sales_pivot = daily_sales.pivot_table(
        index='date', 
        columns=category_col,
        values='quantity_sold',
        fill_value=0
    ).reset_index()
    
    return daily_sales, sales_pivot

def load_forecast_data(data_dir, product_categories):
    """
    Load forecast data or create a placeholder if not available.
    
    Args:
        data_dir (str): Path to the data directory
        product_categories (list): List of product categories
        
    Returns:
        pandas.DataFrame: Forecast data
    """
    forecast_path = os.path.join(data_dir, 'sales_forecast_next_90_days.csv')
    
    if os.path.exists(forecast_path):
        forecast_data = pd.read_csv(forecast_path)
        forecast_data['date'] = pd.to_datetime(forecast_data['date'])
        print("Successfully loaded forecast data")
    else:
        # Create empty forecast data as a placeholder
        print("Forecast data not found, creating placeholder")
        forecast_data = pd.DataFrame({
            'date': pd.date_range(start=datetime.now(), periods=90),
            **{category: np.zeros(90) for category in product_categories}
        })
    
    return forecast_data
