#!/usr/bin/env python

import os
from   app               import create_app, db, models
from   flask.ext.script  import Manager, Shell
from   flask.ext.migrate import Migrate, MigrateCommand


app     = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, models=models)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',    MigrateCommand)


@manager.command
def deploy():
    """
    Creates and upgrades the DB
    """
    from flask.ext.migrate import upgrade
    upgrade()


@manager.command
def test():
    """
    Runs through User and Group unit tests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
