# Virtual Environment Setup Instructions for HBnB Project

## Problem Solved
The "externally-managed-environment" error has been resolved by creating a Python virtual environment.

## What We Did
1. **Created a virtual environment**: `python3 -m venv hbnb-venv`
2. **Activated the virtual environment**: `source hbnb-venv/bin/activate`
3. **Installed required packages**: Flask and Flask-RESTx
4. **Verified the setup**: Successfully imported and tested the Flask application

## How to Use Going Forward

### On Windows (WSL):
1. Open WSL terminal
2. Navigate to your project: `cd /mnt/d/myschoolworkandGithub/holbertonschool-hbnb`
3. Activate the virtual environment: `source hbnb-venv/bin/activate`
4. Navigate to the app directory: `cd part2/hbnb`
5. Run the application: `python run.py`

### Important Notes:
- Always activate the virtual environment before working on the project
- The virtual environment prompt will show `(hbnb-venv)` when active
- To deactivate the virtual environment, simply run: `deactivate`
- To install new packages, make sure the virtual environment is active first

### Packages Installed:
- Flask 3.1.1
- Flask-RESTx 1.3.0
- All required dependencies

## Testing the Setup:
Run: `python test_setup.py` to verify everything is working correctly.

## Next Steps:
You can now visit `http://localhost:5000/api/v1/` when the Flask app is running to see the Swagger documentation interface.
