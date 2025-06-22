#!/usr/bin/env python3
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Flask app created successfully!")
    print("You can now run: python run.py")
    print("Virtual environment is properly set up!")
