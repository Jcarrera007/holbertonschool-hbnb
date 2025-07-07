import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    
    # API Configuration
    API_TITLE = 'HBnB API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'HBnB Application API'
    
    # Application settings
    JSON_SORT_KEYS = False
    RESTX_MASK_SWAGGER = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_for_hbnb')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds

class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration with optimizations."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'production_secret_key_change_me')

class TestingConfig(Config):
    """Testing configuration for unit tests."""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}