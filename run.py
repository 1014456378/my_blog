from app.models import db
from app.__init__ import create_app
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import Config
from app.views_user import mail
if __name__ == '__main__':
    new_app = create_app(Config)
    mail.init_app(new_app)
    manager = Manager(new_app)
    migrate = Migrate(new_app, db)
    manager.add_command('db', MigrateCommand)
    manager.run()