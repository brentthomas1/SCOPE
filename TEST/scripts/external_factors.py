#!/usr/bin/env python3
# External Factors Analysis
# This script analyzes and creates visualizations for understanding the impact
# of external factors on gun retail sales

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime, timedelta

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))
try:
    from main_config import DATA_DIR, PRODUCT_CATEGORIES
except ImportError:
    print("Warning: Could not import from main_config, using default values")
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_DIR, 'data')
    PRODUCT_CATEGORIES = ['accessories', 'ammunition', 'handgun', 'rifle', 'shotgun']

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

def load_data():
    """Load and prepare the data for external factors analysis"""
    
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
    
    # Merge with external factors
    merged_data = daily_sales.merge(external_factors, left_on='date', right_on=external_factors_date_col, how='left')
    
    return merged_data, external_factors, category_col, external_factors_date_col

def analyze_political_impact(data, category_col):
    """Analyze the impact of political climate on sales"""
    
    # Check if political climate column exists
    political_cols = [col for col in data.columns if 'political' in col.lower()]
    if not political_cols:
        print("Warning: No political climate columns found in the data")
        return
    
    political_col = political_cols[0]
    
    # Group by political climate level and category
    political_impact = data.groupby([political_col, category_col])['quantity_sold'].mean().reset_index()
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=political_col, y='quantity_sold', hue=category_col, data=political_impact)
    
    plt.title('Impact of Political Climate on Daily Sales by Category')
    plt.xlabel('Political Climate Level')
    plt.ylabel('Average Daily Sales')
    plt.legend(title='Category')
    plt.tight_layout()
    
    # Save plot
    output_dir = os.path.join(os.path.dirname(DATA_DIR), 'visualizations')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(os.path.join(output_dir, 'political_impact_analysis.png'))
    plt.close()
    
    print(f"Political impact analysis saved to: {output_dir}/political_impact_analysis.png")
    
    return political_impact

def analyze_legislation_impact(data, category_col):
    """Analyze the impact of legislation risk on sales"""
    
    # Check if legislation risk column exists
    legislation_cols = [col for col in data.columns if 'legislat' in col.lower() or 'law' in col.lower()]
    if not legislation_cols:
        print("Warning: No legislation risk columns found in the data")
        return
    
    legislation_col = legislation_cols[0]
    
    # Group by legislation risk level and category
    legislation_impact = data.groupby([legislation_col, category_col])['quantity_sold'].mean().reset_index()
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=legislation_col, y='quantity_sold', hue=category_col, data=legislation_impact)
    
    plt.title('Impact of Legislation Risk on Daily Sales by Category')
    plt.xlabel('Legislation Risk Level')
    plt.ylabel('Average Daily Sales')
    plt.legend(title='Category')
    plt.tight_layout()
    
    # Save plot
    output_dir = os.path.join(os.path.dirname(DATA_DIR), 'visualizations')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(os.path.join(output_dir, 'legislation_impact_analysis.png'))
    plt.close()
    
    print(f"Legislation impact analysis saved to: {output_dir}/legislation_impact_analysis.png")
    
    return legislation_impact

def analyze_seasonal_impact(data, category_col):
    """Analyze the impact of seasonality on sales"""
    
    # Add month name column
    data['month_name'] = data['date'].dt.strftime('%b')
    data['season'] = data['date'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    
    # Group by month and category
    monthly_sales = data.groupby(['month_name', 'season', category_col])['quantity_sold'].mean().reset_index()
    
    # Sort by month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_sales['month_num'] = monthly_sales['month_name'].map({m: i for i, m in enumerate(month_order)})
    monthly_sales = monthly_sales.sort_values('month_num')
    
    # Create plot
    plt.figure(figsize=(14, 7))
    
    # Plot month-wise trends
    plt.subplot(1, 2, 1)
    sns.barplot(x='month_name', y='quantity_sold', hue=category_col, data=monthly_sales, order=month_order)
    plt.title('Monthly Sales Trends by Category')
    plt.xlabel('Month')
    plt.ylabel('Average Daily Sales')
    plt.legend(title='Category')
    plt.xticks(rotation=45)
    
    # Plot season-wise trends
    plt.subplot(1, 2, 2)
    sns.barplot(x='season', y='quantity_sold', hue=category_col, data=monthly_sales, order=['Winter', 'Spring', 'Summer', 'Fall'])
    plt.title('Seasonal Sales Trends by Category')
    plt.xlabel('Season')
    plt.ylabel('Average Daily Sales')
    plt.legend(title='Category')
    
    plt.tight_layout()
    
    # Save plot
    output_dir = os.path.join(os.path.dirname(DATA_DIR), 'visualizations')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(os.path.join(output_dir, 'seasonal_impact_analysis.png'))
    plt.close()
    
    print(f"Seasonal impact analysis saved to: {output_dir}/seasonal_impact_analysis.png")
    
    return monthly_sales

def analyze_correlation(data, external_factors_date_col, category_col):
    """Analyze correlation between external factors and sales"""
    
    # Pivot data to have categories as columns
    sales_pivot = data.pivot_table(
        index=external_factors_date_col, 
        columns=category_col,
        values='quantity_sold',
        fill_value=0
    ).reset_index()
    
    # Get external factor columns
    ext_cols = [col for col in data.columns if col not in 
               ['date', external_factors_date_col, category_col, 'quantity_sold', 'month_name', 'season', 'month_num']]
    
    # Merge external factors with sales pivot
    corr_data = sales_pivot.merge(
        data[ext_cols + [external_factors_date_col]].drop_duplicates(external_factors_date_col),
        on=external_factors_date_col
    )
    
    # Calculate correlation matrix
    corr_matrix = corr_data.drop(external_factors_date_col, axis=1).corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.2f')
    
    plt.title('Correlation Between Sales and External Factors')
    plt.tight_layout()
    
    # Save plot
    output_dir = os.path.join(os.path.dirname(DATA_DIR), 'visualizations')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plt.savefig(os.path.join(output_dir, 'correlation_analysis.png'))
    plt.close()
    
    print(f"Correlation analysis saved to: {output_dir}/correlation_analysis.png")
    
    return corr_matrix

def analyze_events_impact(data, category_col):
    """Analyze the impact of events (promotional, hunting seasons, etc.) on sales"""
    
    # Check for event-related columns
    event_patterns = ['event', 'promot', 'hunt', 'season', 'holiday']
    event_cols = []
    
    for pattern in event_patterns:
        event_cols.extend([col for col in data.columns if pattern in col.lower()])
    
    if not event_cols:
        print("Warning: No event-related columns found in the data")
        return
    
    # For each event type, analyze its impact
    event_impacts = {}
    
    for event_col in event_cols:
        # Check if column is binary (0/1) or has multiple levels
        if data[event_col].nunique() <= 2:
            # Binary event
            event_impact = data.groupby([event_col, category_col])['quantity_sold'].mean().reset_index()
            
            # Create plot
            plt.figure(figsize=(10, 6))
            sns.barplot(x=category_col, y='quantity_sold', hue=event_col, data=event_impact)
            
            plt.title(f'Impact of {event_col} on Daily Sales by Category')
            plt.xlabel('Category')
            plt.ylabel('Average Daily Sales')
            plt.legend(title=event_col)
            
        else:
            # Multi-level event
            event_impact = data.groupby([event_col, category_col])['quantity_sold'].mean().reset_index()
            
            # Create plot
            plt.figure(figsize=(12, 6))
            sns.barplot(x=event_col, y='quantity_sold', hue=category_col, data=event_impact)
            
            plt.title(f'Impact of {event_col} on Daily Sales by Category')
            plt.xlabel(event_col)
            plt.ylabel('Average Daily Sales')
            plt.legend(title='Category')
        
        plt.tight_layout()
        
        # Save plot
        output_dir = os.path.join(os.path.dirname(DATA_DIR), 'visualizations')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plot_filename = f'{event_col}_impact_analysis.png'
        plt.savefig(os.path.join(output_dir, plot_filename))
        plt.close()
        
        print(f"{event_col} impact analysis saved to: {output_dir}/{plot_filename}")
        
        event_impacts[event_col] = event_impact
    
    return event_impacts

def main():
    """Main function to run all external factors analyses"""
    print("Starting external factors analysis")
    
    # Load data
    data, external_factors, category_col, external_factors_date_col = load_data()
    
    # Run analyses
    political_impact = analyze_political_impact(data, category_col)
    legislation_impact = analyze_legislation_impact(data, category_col)
    seasonal_impact = analyze_seasonal_impact(data, category_col)
    correlation = analyze_correlation(data, external_factors_date_col, category_col)
    event_impacts = analyze_events_impact(data, category_col)
    
    print("External factors analysis complete!")

if __name__ == "__main__":
    main()
