import os
from app import create_app

try:
    # Get configuration from environment variable, default to 'development'
    config_name = os.getenv('FLASK_ENV', 'development')

    # Create the application using the Application Factory pattern
    app = create_app(config_name)
except Exception:
    import traceback, sys
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    # Get host and port from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Run the application
    app.run(host=host, port=port, debug=app.config['DEBUG'])