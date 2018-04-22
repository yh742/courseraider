class Config(object):
    pass


class DevelopmentConfig(object):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(object):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

