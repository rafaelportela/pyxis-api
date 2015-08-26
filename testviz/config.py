import os

database_url = os.getenv('DATABASE_URL', 'mysql://dashboard:password@192.168.33.42/sandbox_test')
SQLALCHEMY_DATABASE_URI = database_url
