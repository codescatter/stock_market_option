from project_engine import yaml_data

SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
SQLALCHEMY_DATABASE_URI = yaml_data['db_connector']['db'] + "://" + yaml_data['db_connector']['user'] + ":" \
                          + yaml_data['db_connector']['password'] + "@" + yaml_data['db_connector']['host'] + "/" \
                          + yaml_data['db_connector']['database']

SQLALCHEMY_BINDS = {
    'db1': SQLALCHEMY_DATABASE_URI,
}

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Redis Configuration
ACTIVITY_LOGGER = yaml_data['activity_logger']
COUNT = yaml_data['count']