#!/usr/bin/env python3
"""
Script to copy data files from the old structure to the new structure
"""

import os
import sys
import shutil

# Add parent directory to path to import from config and scope
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from config.main_config import DATA_DIR, MODELS_DIR, VISUALIZATIONS_DIR

# Paths to old structure
old_data_dir = '/Users/brentthomas1/Desktop/Mac_Mini/SCOPE/TEST/data'
old_models_dir = '/Users/brentthomas1/Desktop/Mac_Mini/SCOPE/models'

def copy_data_files():
    """Copy CSV files from old data directory to new data directory"""
    if not os.path.exists(old_data_dir):
        print(f"Error: Old data directory not found at {old_data_dir}")
        return
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")
    
    # Copy CSV files
    copied_count = 0
    for filename in os.listdir(old_data_dir):
        if filename.endswith('.csv'):
            src_path = os.path.join(old_data_dir, filename)
            dst_path = os.path.join(DATA_DIR, filename)
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Copied: {filename}")
                copied_count += 1
            except Exception as e:
                print(f"Error copying {filename}: {str(e)}")
    
    print(f"Copied {copied_count} CSV files to {DATA_DIR}")

def copy_model_files():
    """Copy model files from old models directory to new models directory"""
    if not os.path.exists(old_models_dir):
        print(f"Error: Old models directory not found at {old_models_dir}")
        return
    
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"Created directory: {MODELS_DIR}")
    
    # Copy model files
    copied_count = 0
    for filename in os.listdir(old_models_dir):
        if filename.endswith('.pkl'):
            src_path = os.path.join(old_models_dir, filename)
            dst_path = os.path.join(MODELS_DIR, filename)
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Copied: {filename}")
                copied_count += 1
            except Exception as e:
                print(f"Error copying {filename}: {str(e)}")
    
    print(f"Copied {copied_count} model files to {MODELS_DIR}")

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [DATA_DIR, MODELS_DIR, VISUALIZATIONS_DIR]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main function"""
    print("Starting data migration process...")
    
    # Ensure directories exist
    ensure_directories()
    
    # Copy files
    print("\nCopying data files...")
    copy_data_files()
    
    print("\nCopying model files...")
    copy_model_files()
    
    print("\nMigration complete!")

if __name__ == "__main__":
    main()
