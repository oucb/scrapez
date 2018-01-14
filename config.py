import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Config(object):
    SECRET_KEY = 'super_long_key_that_noone_really_cares_about'
    DOWNLOAD_FOLDER = os.environ['DOWNLOAD_FOLDER']

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'default': Config,
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
