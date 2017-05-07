import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heshangbuxitou'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}