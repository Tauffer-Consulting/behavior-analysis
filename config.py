import random
import string


class ConfigDev:
    """Set Flask configuration for development"""

    # General Config
    SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    # FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ConfigProduction:
    """Set Flask configuration for production"""

    # General Config
    SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    # FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = 'production'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
