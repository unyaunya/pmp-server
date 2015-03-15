#!flask/bin/python
from pmpserver import app
from migrate.versioning import api
database_uri = app.config['SQLALCHEMY_DATABASE_URI']
migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
v = api.db_version(database_uri, migrate_repo)
api.downgrade(database_uri, migrate_repo, v - 1)
v = api.db_version(database_uri, migrate_repo)
print('Current database version: ' + str(v))