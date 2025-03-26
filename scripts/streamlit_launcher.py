#!/usr/bin/env python3
"""
Streamlit Dashboard Launcher

This script sets up the environment and launches the Streamlit dashboard.
"""

import os
import sys
import subprocess
import platform

# Add parent directory to path to import from config and scope
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

try:
    from config.main_config import PROJECT_DIR, DATA_DIR, MODELS_DIR, VISUALIZATIONS_DIR
except ImportError:
    print("Warning: Could not import from config.main_config")
    PROJECT_DIR = project_root
    DATA_DIR = os.path.join(PROJECT_DIR, 'scope', 'data')
    MODELS_DIR = os.path.join(PROJECT_DIR, 'scope', 'models')
    VISUALIZATIONS_DIR = os.path.join(PROJECT_DIR, 'scope', 'visualizations')


def check_dependencies():
    """Check if required packages are installed or set up virtual environment"""
    venv_dir = os.path.join(PROJECT_DIR, 'venv')
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        # We're not in a virtual environment, we need to create one
        print("No virtual environment detected. Setting up a virtual environment...")
        if not os.path.exists(venv_dir):
            print(f"Creating virtual environment at {venv_dir}")
            # Create the virtual environment
            try:
                subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
                print("Virtual environment created successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error creating virtual environment: {e}")
                return False
        
        # Get the activate script path
        if platform.system() == 'Windows':
            activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
            activate_cmd = f"call \"{activate_script}\""
        else:  # macOS and Linux
            activate_script = os.path.join(venv_dir, 'bin', 'activate')
            activate_cmd = f"source {activate_script}"
        
        print(f"To activate the virtual environment manually, run:\n{activate_cmd}")
        print("\nThen run this script again within the activated environment.")
        
        # Get the path to the Python interpreter in the virtual environment
        if platform.system() == 'Windows':
            venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')
        else:  # macOS and Linux
            venv_python = os.path.join(venv_dir, 'bin', 'python')
        
        # Check for requirements file
        req_file = os.path.join(PROJECT_DIR, "requirements.txt")
        
        if not os.path.exists(req_file):
            print(f"Error: requirements.txt not found at {req_file}")
            return False
        
        # Install dependencies within the virtual environment
        print("Installing required packages in the virtual environment...")
        try:
            if platform.system() == 'Windows':
                subprocess.check_call([venv_python, '-m', 'pip', 'install', '-r', req_file])
            else:  # For macOS and Linux - use a subshell with source command
                install_cmd = f"source {activate_script} && python -m pip install -r {req_file}"
                subprocess.check_call(install_cmd, shell=True, executable='/bin/bash')
            print("Packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            print("Please manually activate the virtual environment and install the dependencies:")
            print(f"\n{activate_cmd}")
            print(f"pip install -r {req_file}")
            return False
        
        # Re-launch this script within the virtual environment
        print("\nLaunching the dashboard within the virtual environment...")
        try:
            if platform.system() == 'Windows':
                # For Windows, use the venv Python directly
                subprocess.Popen([venv_python, os.path.abspath(__file__)])
            else:  # For macOS and Linux
                # Use bash to source the activate script and then run the script
                cmd = f"source {activate_script} && python {os.path.abspath(__file__)}"
                subprocess.Popen(cmd, shell=True, executable='/bin/bash')
            print("\nDashboard starting in a new process with the virtual environment.")
            sys.exit(0)  # Exit this instance of the script
        except Exception as e:
            print(f"Error launching script in virtual environment: {e}")
            return False
    
    # If we reach here, we're running inside the virtual environment or bypassing the check
    try:
        import streamlit
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import joblib
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing required package: {e.name}")
        
        # Get the path to the requirements file
        req_file = os.path.join(PROJECT_DIR, "requirements.txt")
        
        if not os.path.exists(req_file):
            print(f"Error: requirements.txt not found at {req_file}")
            return False
        
        install = input("Install missing packages from requirements.txt? (y/n): ")
        if install.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
                print("Packages installed successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error installing packages: {e}")
                return False
        else:
            print("Please install the required packages and try again.")
            return False

def setup_directories():
    """Ensure required directories exist"""
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created data directory: {DATA_DIR}")
    
    # Create models directory if it doesn't exist
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"Created models directory: {MODELS_DIR}")
    
    # Create visualizations directory if it doesn't exist
    if not os.path.exists(VISUALIZATIONS_DIR):
        os.makedirs(VISUALIZATIONS_DIR)
        print(f"Created visualizations directory: {VISUALIZATIONS_DIR}")

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    dashboard_script = os.path.join(script_dir, 'streamlit_dashboard.py')
    
    if not os.path.exists(dashboard_script):
        print(f"Dashboard script not found at {dashboard_script}")
        return False
    
    print("Launching Streamlit dashboard...")
    
    # Run the Streamlit app
    try:
        # Launch the Streamlit app using the current Python interpreter (which should be the venv one)
        subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', dashboard_script])
        
        print("\nDashboard is starting in your browser.")
        print("If it doesn't open automatically, go to: http://localhost:8501")
        return True
    
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        return False

if __name__ == "__main__":
    print("Gun Retail Sales Dashboard Launcher")
    print("===================================")
    
    if check_dependencies():
        setup_directories()
        launch_dashboard()
    else:
        print("Failed to start dashboard due to missing dependencies.")
