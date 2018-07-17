from flask import Blueprint, jsonify
from flask import g
from flask import render_template
from flask import session

from app import models
from app.models import db, User

index_blueprint = Blueprint('index_b',__name__)

@index_blueprint.route('/')
def index():
    # articlee = models.Article(title='python之flask学习', content='我使用flask制作个人博客，这是第一篇文章')
    # db.session.add(articlee)
    # db.session.commit()
    if 'user_id' in session:
        g.user=User.query.get(session['user_id'])
    else:
        g.user=None
    article = models.Article.query.all()
    return render_template('news/index.html',article = article,title='博客首页')

@index_blueprint.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id')
    return jsonify(result=0)