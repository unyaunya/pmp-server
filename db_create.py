#!flask/bin/python
from migrate.versioning import api
from pmpserver import app, db
import os.path

db.create_all()
database_uri = app.config['SQLALCHEMY_DATABASE_URI']
migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
if not os.path.exists(migrate_repo):
    api.create(migrate_repo, 'database repository')
    api.version_control(database_uri, migrate_repo)
else:
    api.version_control(database_uri, migrate_repo, api.version(migrate_repo))