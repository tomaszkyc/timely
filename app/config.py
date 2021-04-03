import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'nSxMSmFUPUlCaG='
    SECRET_KEY = 'nSxMSmFUPUlCaG='
    # recaptcha settings start
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
    # recaptcha settings end
    # sql db start
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_CHARSET = 'utf8mb4'
    # sql db end
    # mail settings start
    MAIL_DEFAULT_SENDER = "Timely support (support@domain.com)"
    MAIL_SERVER = "localhost"
    MAIL_ADDRESS = "support@domain.com"
    MAIL_PORT = 1025
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    # mail settings end
    # test user settings start
    TEST_USER_EMAIL = "user@domain.com"
    TEST_USER_NAME = "John"
    TEST_USER_PASSWORD = "password"
    # test user settings end
    SUPPORT_CONTACT_EMAIL = os.getenv('SUPPORT_CONTACT_EMAIL')
    PRODUCTION = False


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = False


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    # mail settings start
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # mail settings end
    PRODUCTION = True


class TestingConfig(Config):
    """Configurations for Testing."""
    DEBUG = False
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = False
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/db_test'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
