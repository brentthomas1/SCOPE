#!/usr/bin/env python3
"""
Tests for utility functions in the SCOPE project.
"""

import os
import sys
import unittest
import pandas as pd
from unittest.mock import patch, mock_open

# Add parent directory to path to import from scope
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import functions to test
from scope.utils.file_utils import find_file
from scope.utils.data_utils import find_column_by_pattern


class TestFileUtils(unittest.TestCase):
    """Tests for file utility functions."""
    
    @patch('os.path.exists')
    def test_find_file_exact_match(self, mock_exists):
        """Test finding a file when an exact match exists."""
        # Set up the mock to return True for exact match
        mock_exists.side_effect = lambda path: path.endswith('test.csv')
        
        # Test the function
        result = find_file('test.csv', '/fake/dir')
        
        # Verify the result
        self.assertEqual(result, '/fake/dir/test.csv')
    
    @patch('os.path.exists')
    def test_find_file_lowercase_match(self, mock_exists):
        """Test finding a file when only a lowercase variant exists."""
        # Set up the mock to return True only for lowercase variant
        mock_exists.side_effect = lambda path: path.endswith('lowercase_test.csv')
        
        # Test the function
        result = find_file('test.csv', '/fake/dir')
        
        # Verify the result
        self.assertEqual(result, '/fake/dir/lowercase_test.csv')
    
    @patch('os.path.exists')
    def test_find_file_no_match(self, mock_exists):
        """Test finding a file when no match exists."""
        # Set up the mock to return False for all paths
        mock_exists.return_value = False
        
        # Test the function
        result = find_file('test.csv', '/fake/dir')
        
        # Verify the result (should return the default path)
        self.assertEqual(result, '/fake/dir/test.csv')


class TestDataUtils(unittest.TestCase):
    """Tests for data utility functions."""
    
    def test_find_column_by_pattern_match(self):
        """Test finding a column that matches a pattern."""
        # Create a test dataframe
        df = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'transaction_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'product_category': ['handgun', 'rifle', 'ammunition']
        })
        
        # Test the function
        result = find_column_by_pattern(df, ['date', 'time'])
        
        # Verify the result
        self.assertEqual(result, 'transaction_date')
    
    def test_find_column_by_pattern_no_match(self):
        """Test finding a column when no match exists."""
        # Create a test dataframe
        df = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'transaction_id': [101, 102, 103],
            'product_category': ['handgun', 'rifle', 'ammunition']
        })
        
        # Test the function
        result = find_column_by_pattern(df, ['date', 'time'])
        
        # Verify the result (should return the first column)
        self.assertEqual(result, 'customer_id')
    
    def test_find_column_by_pattern_multiple_matches(self):
        """Test finding a column when multiple matches exist."""
        # Create a test dataframe
        df = pd.DataFrame({
            'transaction_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'delivery_date': ['2023-01-03', '2023-01-04', '2023-01-05'],
            'product_category': ['handgun', 'rifle', 'ammunition']
        })
        
        # Test the function - it should return the first match
        result = find_column_by_pattern(df, ['date'])
        
        # Verify the result
        self.assertEqual(result, 'transaction_date')


if __name__ == '__main__':
    unittest.main()
