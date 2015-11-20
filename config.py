import os

# Deployment options
# APPLICATION_ROOT = '/flagr'
ALLOWED_ORIGIN = 'https://ranisalt.github.io'
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 megabytes

# Amazon S3 options
AWS_BUCKET_NAME = 'flagr'
AWS_EXPIRES_IN = 12 * 60 * 60  # 12 hours

# Development flags
DEBUG = os.getenv('DEBUG', 'OFF').upper() == 'ON'
TESTING = os.getenv('TESTING', 'OFF').upper() == 'ON'
