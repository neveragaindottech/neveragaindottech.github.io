"""
Configuration Module
Holds all app config
"""
class Config(object):
    """
    Configuration Object
    """

    DEBUG = True

    # DB Vars
    db_user = 'dbuser'
    db_pass = 'dbpassword'
    db_host = 'localhost'
    db_name = 'user'

    # DB Settings
    if DEBUG:
        SQLALCHEMY_DATABASE_URI = 'sqlite://user'
    else:
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        SQLALCHEMY_DATABASE_URI = 'mysql://{db_user}:{db_pass}@{db_host}/{db_name}'.format(
            db_user=db_user,
            db_pass=db_pass,
            db_host=db_host,
            db_name=db_name
        )
        SQLALCHEMY_POOL_SIZE = 10
        SQLALCHEMY_POOL_TIMEOUT = 10
        SQLALCHEMY_POOL_RECYCLE = 500
