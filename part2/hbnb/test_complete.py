#!/usr/bin/env python3

print("=== HBnB Flask Application Test ===")
print()

try:
    from app import create_app
    print("✅ Successfully imported create_app")
    
    app = create_app()
    print("✅ Successfully created Flask app")
    
    print("✅ Setup is complete!")
    print()
    print("To run the application:")
    print("1. Make sure you're in the correct directory:")
    print("   cd /mnt/d/myschoolworkandGithub/holbertonschool-hbnb/part2/hbnb")
    print("2. Activate virtual environment:")
    print("   source ../../hbnb-venv/bin/activate")
    print("3. Run the application:")
    print("   python run.py")
    print()
    print("The app will be available at: http://localhost:5000")
    print("API documentation at: http://localhost:5000/api/v1/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your setup.")
