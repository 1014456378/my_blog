from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseModel(object):
    isDelete = db.Column(db.Boolean,default=False)
#用户收藏：用户和文章多对多关系表
user_article_collect = db.Table(
    'user_article_collect',

    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
)
#用户表
class User(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64), index=True,default=email)
    #用户密码hash码
    pwd_hash = db.Column(db.String(200))
    #用户头像
    pic = db.Column(db.String(50),default='FqpDiGx81qkUNINriHHL9TqHADho')
    isMaster = db.Column(db.Boolean,default=False)
    #用户评论关系
    talk = db.relationship('Talk', backref='whotalk', lazy='dynamic')
    #用户收藏关系
    collect = db.relationship('Article',secondary = user_article_collect,lazy = 'dynamic')
    @property
    def password(self):
        pass
    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)
    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)
    @property
    def pic_url(self):
        return 'http://oyvzbpqij.bkt.clouddn.com/' + self.pic


class Talk(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime,default=datetime.now)
    #评论内容
    content = db.Column(db.String(50))
    #评论用户外键
    user = db.Column(db.Integer,db.ForeignKey('user.id',))
    #评论的文章外键
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    #评论自关联一对多
    parent_id = db.Column(db.Integer, db.ForeignKey("talk.id"))
    parent = db.relationship("Talk",lazy='dynamic')

class Article(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(20))
    content = db.Column(db.TEXT)
    #文章评论关系
    talk = db.relationship('Talk',backref = 'article',lazy = 'dynamic')



