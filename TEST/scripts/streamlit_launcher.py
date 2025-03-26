#!/usr/bin/env python3
# Streamlit Dashboard Launcher

import os
import sys
import subprocess
import platform

def check_dependencies():
    """Check if required packages are installed or set up virtual environment"""
    venv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'venv')
    
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(os.path.dirname(script_dir), 'config')
        req_file = os.path.join(config_dir, "requirements.txt")
        
        if not os.path.exists(req_file):
            print(f"Creating requirements file at {req_file}")
            with open(req_file, "w") as f:
                f.write("pandas>=1.3.0\n")
                f.write("numpy>=1.20.0\n")
                f.write("matplotlib>=3.4.0\n")
                f.write("seaborn>=0.11.0\n")
                f.write("streamlit>=1.25.0\n")
                f.write("scikit-learn>=1.0.0\n")
                f.write("joblib>=1.1.0\n")
                f.write("ipywidgets>=8.0.0\n")
        
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
        
        # Get the absolute path to the requirements file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(os.path.dirname(script_dir), "config")
        req_file = os.path.join(config_dir, "requirements.txt")
        
        if not os.path.exists(req_file):
            print(f"Creating requirements file at {req_file}")
            with open(req_file, "w") as f:
                f.write("pandas>=1.3.0\n")
                f.write("numpy>=1.20.0\n")
                f.write("matplotlib>=3.4.0\n")
                f.write("seaborn>=0.11.0\n")
                f.write("streamlit>=1.25.0\n")
                f.write("scikit-learn>=1.0.0\n")
                f.write("joblib>=1.1.0\n")
                f.write("ipywidgets>=8.0.0\n")
        
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

def setup_dashboard():
    """Set up the dashboard configuration"""
    # Determine the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Determine config directory
    config_dir = os.path.join(os.path.dirname(script_dir), 'config')
    
    # Determine project root and other directories
    if "SCOPE/TEST/scripts" in script_dir:
        project_root = os.path.dirname(script_dir)  # SCOPE/TEST
    else:
        project_root = os.path.join(os.path.dirname(script_dir), '..')  # Assume we're in a scripts directory
    
    # Always look for data in TEST/data first
    data_dir = os.path.join(project_root, 'data')
    if not os.path.exists(data_dir):
        print(f"Warning: Data directory not found at {data_dir}")
        
        # Try to find data directory
        possible_data_dirs = [
            os.path.join(os.path.dirname(project_root), 'TEST', 'data'),  # SCOPE/TEST/data
            os.path.join(project_root, '..', 'data'),  # SCOPE/data
            os.path.join(os.path.dirname(project_root), 'data')  # One level up data
        ]
        
        for possible_dir in possible_data_dirs:
            if os.path.exists(possible_dir):
                data_dir = possible_dir
                print(f"Found data directory at: {data_dir}")
                break
        else:
            print("Could not find data directory automatically.")
            data_dir_input = input("Please enter the full path to your data directory: ")
            if os.path.exists(data_dir_input):
                data_dir = data_dir_input
            else:
                print(f"Error: Directory not found: {data_dir_input}")
                return None
    
    # Look for models directory
    models_dir = os.path.join(os.path.dirname(project_root), 'models')  # SCOPE/models
    if not os.path.exists(models_dir):
        print(f"Warning: Models directory not found at {models_dir}")
        create_models = input("Create models directory? (y/n): ")
        if create_models.lower() == 'y':
            try:
                os.makedirs(models_dir)
                print(f"Created models directory at {models_dir}")
            except Exception as e:
                print(f"Error creating models directory: {e}")
                models_dir = os.path.join(project_root, 'models')
                try:
                    os.makedirs(models_dir)
                    print(f"Created alternative models directory at {models_dir}")
                except Exception as e:
                    print(f"Error creating alternative models directory: {e}")
    
    # Create config file in the config directory
    config_path = os.path.join(config_dir, 'dashboard_config.py')
    with open(config_path, 'w') as f:
        f.write(f"PROJECT_ROOT = '{project_root}'\n")
        f.write(f"DATA_DIR = '{data_dir}'\n")
        f.write(f"MODELS_DIR = '{models_dir}'\n")
    
    print(f"Dashboard configuration written to: {config_path}")
    print(f"Project root: {project_root}")
    print(f"Data directory: {data_dir}")
    print(f"Models directory: {models_dir}")
    
    return script_dir

def launch_dashboard(script_dir):
    """Launch the Streamlit dashboard"""
    dashboard_script = os.path.join(script_dir, 'streamlit_dashboard.py')
    
    if not os.path.exists(dashboard_script):
        print(f"Dashboard script not found at {dashboard_script}")
        return False
    
    print("Launching Streamlit dashboard...")
    
    # Run the Streamlit app
    try:
        # Change to the script directory to ensure relative paths work
        os.chdir(script_dir)
        
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
        script_dir = setup_dashboard()
        if script_dir:
            launch_dashboard(script_dir)
        else:
            print("Failed to set up dashboard configuration.")
    else:
        print("Failed to start dashboard due to missing dependencies.")