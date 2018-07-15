from flask import Flask
from app.models import db
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from app.views_index import index_blueprint
import redis

from app.views_user import user_blueprint
from flask_mail import Mail

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    CSRFProtect(app)
    Session(app)
    app.redis_cli = redis.StrictRedis(config.REDIS_HOST,config.REDIS_PORT,config.REDIS_DB)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(user_blueprint)
    return app

