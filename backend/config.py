import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'root')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'iamzain')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'kryptonite')
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '69a4a424b71c68ab389328ba828f71f2')
# TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_ecom')