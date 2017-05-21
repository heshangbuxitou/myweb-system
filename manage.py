import os
from app import create_app, db
from app.models import User, Post, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

def email_hide(args):
    end = args.find('@')
    return args[:end-3]+'***'+args[end:]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

env = app.jinja_env
env.filters['email_hide'] = email_hide

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()