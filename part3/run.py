import os
from app import create_app

# Get configuration name from environment variable or default to 'development'
config_name = os.getenv('FLASK_ENV', 'development')

# Create the Flask application with the specified configuration
app = create_app(config_name)

if __name__ == '__main__':
    # The debug mode is now controlled by the configuration object
    app.run(host='127.0.0.1', port=5000)