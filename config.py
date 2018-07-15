import redis
import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql@localhost:3306/my_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #redis配置
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 6
    #session
    SECRET_KEY = 'this is my blog'
    #flask_session的配置
    SESSION_TYPE = 'redis'          #session保存到redis里
    SESSION_USE_SIGNER = True       #cookie的session的id签名处理
    SESSION_REDIS = redis.StrictRedis(host = REDIS_HOST,port = REDIS_PORT,db = REDIS_DB)
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # CSRF_ENABLED = True
    # SQLALCHEMY_ECHO = True

    #flask-mail设置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1014456378@qq.com'
    MAIL_PASSWORD = 'chazzkvxngzpbdba'
    MAIL_DEFAULT_SENDER = '1014456378@qq.com'

