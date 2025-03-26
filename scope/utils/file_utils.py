"""
File utility functions for the SCOPE project.
"""

import os
import pandas as pd

def find_file(filename, directory):
    """
    Find a file in directory, checking for lowercase and uppercase variants.
    
    Args:
        filename (str): The target filename
        directory (str): The directory to search in
        
    Returns:
        str: Path to the found file or the default path if not found
    """
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
