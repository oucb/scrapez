import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

APP_TYPE = os.environ.get('FLASK_APP', 'ui')

class Config(object):
    APP_TYPE = APP_TYPE
    DEBUG = False
    SECRET_KEY = 'super_long_key_that_noone_really_cares_about'
    DOWNLOAD_FOLDER = os.environ['DOWNLOAD_FOLDER']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': 'redis://localhost'
    }
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'default': Config,
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
