from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

from app.__init__ import create_app
from app.models import db
from app.views_user import mail
from config import Config

if __name__ == '__main__':
    new_app = create_app(Config)
    mail.init_app(new_app)
    manager = Manager(new_app)
    migrate = Migrate(new_app, db)
    manager.add_command('db', MigrateCommand)
    manager.run()