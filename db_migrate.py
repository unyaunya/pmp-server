#!flask/bin/python
import imp
from migrate.versioning import api
from pmpserver import app, db

database_uri = app.config['SQLALCHEMY_DATABASE_URI']
migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
v = api.db_version(database_uri, migrate_repo)
migration = migrate_repo + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(database_uri, migrate_repo)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(database_uri, migrate_repo, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(database_uri, migrate_repo)
v = api.db_version(database_uri, migrate_repo)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))