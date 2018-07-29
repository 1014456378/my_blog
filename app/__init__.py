import redis
from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

from app.models import db
from app.views_detail import detail_blueprint
from app.views_index import index_blueprint
from app.views_user import user_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    CSRFProtect(app)
    Session(app)
    app.redis_cli = redis.StrictRedis(config.REDIS_HOST,config.REDIS_PORT,config.REDIS_DB)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(detail_blueprint)
    return app

