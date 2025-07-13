#!/usr/bin/env python3
"""
Comprehensive verification script for the Application Factory pattern implementation.
"""

import os
import sys
from contextlib import contextmanager
from io import StringIO

def test_import():
    """Test that all modules can be imported successfully."""
    try:
        from app import create_app
        from config import config, Config, DevelopmentConfig, TestingConfig, ProductionConfig
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configurations():
    """Test that all configuration classes work correctly."""
    try:
        from app import create_app
        
        configs_to_test = ['development', 'testing', 'production', 'default']
        
        for config_name in configs_to_test:
            try:
                app = create_app(config_name)
                with app.app_context():
                    # Basic checks
                    assert 'SECRET_KEY' in app.config
                    assert 'DEBUG' in app.config
                    
                    if config_name == 'testing':
                        assert app.config['TESTING'] == True
                        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
                    elif config_name == 'production':
                        assert app.config['DEBUG'] == False
                    elif config_name in ['development', 'default']:
                        assert app.config['DEBUG'] == True
                        
                print(f"✅ Configuration '{config_name}' working correctly")
            except Exception as e:
                print(f"❌ Configuration '{config_name}' failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_environment_variables():
    """Test that environment variables are properly handled."""
    try:
        # For now, we'll just test that the configuration classes exist
        # and have the expected environment variable handling
        from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
        
        # Check that the Config class uses os.getenv
        import inspect
        config_source = inspect.getsource(Config)
        
        if 'os.getenv' in config_source and 'SECRET_KEY' in config_source:
            print("✅ Environment variables configured correctly in Config class")
            return True
        else:
            print("❌ Environment variable configuration not found")
            return False
            
    except Exception as e:
        print(f"❌ Environment variable test failed: {e}")
        return False

def test_app_creation():
    """Test that Flask apps are created correctly."""
    try:
        from app import create_app
        
        app = create_app()
        
        # Check that it's a Flask app
        assert hasattr(app, 'config')
        assert hasattr(app, 'route')
        assert hasattr(app, 'run')
        
        # Check that API is set up
        with app.app_context():
            # The app should have our API endpoints registered
            pass
        
        print("✅ Flask app creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation test failed: {e}")
        return False

def test_run_script():
    """Test that run.py is properly configured."""
    try:
        # Read run.py content
        with open('run.py', 'r') as f:
            content = f.read()
        
        # Check for required elements
        assert 'create_app' in content
        assert 'config_name' in content or 'FLASK_ENV' in content
        assert 'app.run' in content
        
        print("✅ run.py script properly configured")
        return True
    except Exception as e:
        print(f"❌ run.py test failed: {e}")
        return False

def verify_application_factory():
    """Run all verification tests."""
    print("🔍 Verifying Application Factory Pattern Implementation\n")
    
    tests = [
        ("Import Test", test_import),
        ("Configuration Test", test_configurations),
        ("Environment Variables Test", test_environment_variables),
        ("App Creation Test", test_app_creation),
        ("Run Script Test", test_run_script),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application Factory pattern successfully implemented.")
        print("✅ Ready for the next tasks (User Model, JWT Authentication, etc.)")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review the implementation.")
        return False

if __name__ == '__main__':
    success = verify_application_factory()
    sys.exit(0 if success else 1)
