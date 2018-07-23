from flask import Blueprint, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from app import models
from app.models import db, User, Article

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

    return render_template('news/index.html',title='博客首页')

@index_blueprint.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id')
    return jsonify(result=0)

@index_blueprint.route('/art/')
def art():
    page = int(request.args.get('page','1'))
    art = Article.query.order_by(Article.time.desc())
    art_list1 = art.paginate(page,6,False)
    total_page = art_list1.pages
    art_list = art_list1.items
    list1 = []
    for art_one in art_list:
        list1.append({
            'id':art_one.id,
            'title':art_one.title,
            'time':art_one.time
        })
    return jsonify(list = list1,total_page=total_page)