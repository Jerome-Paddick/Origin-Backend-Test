import os

class DefaultConfig(object):
    DEBUG=True

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DB_PREFIX = "postgresql+psycopg2"
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    DB_SERVER = os.getenv('DB_SERVER')  # 'postgres:5432'

    SQLALCHEMY_DATABASE_URI = "{db_prefix}://{user}:{passwd}@{server}/{db}".format(
        db_prefix=SQLALCHEMY_DB_PREFIX,
        user=POSTGRES_USER,
        passwd=POSTGRES_PASSWORD,
        server=DB_SERVER,
        db=POSTGRES_DB)

    SECRET_KEY = ""
    SECURITY_PASSWORD_SALT = ""

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_CHANGEABLE = True

class TestConfig(object):
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DB_PREFIX = "postgresql+psycopg2"
    POSTGRES_USER = os.getenv('TEST_POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('TEST_POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('TEST_POSTGRES_DB')
    DB_SERVER = os.getenv('TEST_DB_SERVER')

    SQLALCHEMY_DATABASE_URI = "{db_prefix}://{user}:{passwd}@{server}/{db}".format(
        db_prefix=SQLALCHEMY_DB_PREFIX,
        user=POSTGRES_USER,
        passwd=POSTGRES_PASSWORD,
        server=DB_SERVER,
        db=POSTGRES_DB)

    SQLALCHEMY_TRACK_MODIFICATIONS=False



