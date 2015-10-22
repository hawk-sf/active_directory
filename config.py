import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY                    = os.environ.get('SECRET_KEY') or \
                                    'welcome to your planet'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG                   = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PLANET_DEV_DB_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data_dev.sqlite')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PLANET_PROD_DB_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data_test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PLANET_PROD_DB_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data_prod.sqlite')

config = {
          'development': DevelopmentConfig,
          'production':  ProductionConfig,
          'testing':     TestingConfig,
          'default':     DevelopmentConfig,
         }
