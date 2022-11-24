import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db
from app.main.model import user
from app.main.model import blacklist
from app import blueprint

app = create_app(os.getenv("APP_ENV") or "dev")
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

# We use this line to expose all the database migration commands through Flask-Script.
manager.add_command("db", MigrateCommand)


# @manager.command marks that these functions as executable from the command line.
# We can run this program by flask run
@manager.command
def run():
    app.run()


# We can run this program by flask test
@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
