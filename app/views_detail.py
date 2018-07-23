import functools

from flask import Blueprint, jsonify
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from app.models import User, Article, db

detail_blueprint = Blueprint('detail_b',__name__)
def yanzheng(fun):
    @functools.wraps(fun)
    def fun1(*args,**kwargs):
        return fun(*args,**kwargs)
    return fun1

@detail_blueprint.route('/detail/<int:text_id>')
def detail(text_id):
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    text = Article.query.get(text_id)
    return render_template('news/detail.html',text=text,title = '文章详情页')

@detail_blueprint.route('/collect',methods=['POST'])
def collect():
    flag = int(request.form.get('flag'))
    text_id = request.form.get('text_id')
    if 'user_id' not in session:
        return jsonify(result = 1)
    g.user = User.query.get(session['user_id'])
    collect_text = Article.query.get(text_id)
    if flag==1:
        if collect_text in g.user.collect:
            return jsonify(result = 2)
        g.user.collect.append(collect_text)
    else:
        if collect_text not in g.user.collect:
            return jsonify(result=2)
        g.user.collect.remove(collect_text)
    db.session.commit()
    return jsonify(result=0)
